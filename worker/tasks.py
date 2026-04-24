import builtins
import hashlib
import io
import os
import gc
import sys
from contextlib import contextmanager
from pathlib import Path

import numpy as np
import torch
import whisperx
import json
import socket

import threading
import redis as redis_lib
from celery import Celery
from celery.signals import worker_process_init, worker_shutdown
from lingua import Language

# Add shared directory to path for logger
sys.path.append('/app/shared')
from stt_logger import get_logger

@contextmanager
def _redirect_print_to_logger(logger):
    """Capture print() calls (e.g. WhisperX progress) and route them to the task logger."""
    original_print = builtins.print
    def _print_to_log(*args, **kwargs):
        msg = ' '.join(str(a) for a in args)
        if msg.strip():
            logger.info(f"[WORKER] {msg.strip()}")
        original_print(*args, **kwargs)
    builtins.print = _print_to_log
    try:
        yield
    finally:
        builtins.print = original_print


from audio_utils import prepare_audio, load_audio_fast
from persist import save_as_json, save_as_text, save_as_elan, save_as_srt, save_as_vtt, save_as_speakers
from speech_to_text_tasks import SpeechToTextTask
from normalization.welsh_normalizer import WelshNormalizer

# was 'redis://redis:6379/0'
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')
BACKEND_CONN_URI = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
BROKER_CONN_URI = BACKEND_CONN_URI

sampling_rate = 16000

#
app = Celery(
    'tasks',
    broker=BROKER_CONN_URI,
    backend=BACKEND_CONN_URI,
)

# Configure Celery result expiration to prevent Redis bloat
# Priority queues: 0 = highest (high), 5 = default (normal), 9 = lowest (low)
app.conf.update(
    result_expires=7 * 24 * 60 * 60,  # 7 days (matches task_store TTL)
    task_track_started=True,  # Track STARTED state for better status monitoring
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    task_queue_max_priority=10,  # Enable priority 0-9
    task_default_priority=5,     # Default to normal priority
    worker_prefetch_multiplier=1,  # Don't prefetch - ensures idle workers grab high-priority tasks immediately
    worker_proc_alive_timeout=300,  # 5 minutes - allow time for model loading and HF rate limit retries
    worker_max_tasks_per_child=int(os.environ.get('WORKER_MAX_TASKS_PER_CHILD', 0)) or None,  # 0 = never recycle (default), set to e.g. 500 to recycle periodically
)


# Redis connection for worker heartbeat (db=1, separate from Celery's db=0)
_heartbeat_redis = redis_lib.Redis(
    host=os.environ.get('REDIS_HOST', 'redis'),
    port=int(os.environ.get('REDIS_PORT', 6379)),
    db=1
)
_worker_hostname = socket.gethostname()

# Short TTL so stale keys from dead containers expire quickly.
# Refreshed on every task execution to keep alive.
_HEARTBEAT_TTL = 120  # seconds


def _refresh_worker_heartbeat():
    """Refresh worker readiness and device info keys in Redis.
    Called at startup and on every task execution to keep keys alive."""
    try:
        _heartbeat_redis.set(f'worker:ready:{_worker_hostname}', '1', ex=_HEARTBEAT_TTL)
        device_info = json.dumps({
            'device': SpeechToTextTask._device,
            'requested': SpeechToTextTask._requested_device,
            'degraded': SpeechToTextTask._gpu_degraded,
        })
        _heartbeat_redis.set(f'worker:device:{_worker_hostname}', device_info, ex=_HEARTBEAT_TTL)
    except Exception:
        pass


_heartbeat_timer = None


def _start_heartbeat_loop():
    """Run _refresh_worker_heartbeat periodically so Redis keys don't expire
    while a worker is idle (no tasks being processed)."""
    global _heartbeat_timer
    _refresh_worker_heartbeat()
    _heartbeat_timer = threading.Timer(_HEARTBEAT_TTL / 2, _start_heartbeat_loop)
    _heartbeat_timer.daemon = True
    _heartbeat_timer.start()


@worker_process_init.connect
def preload_models(**kwargs):
    """Load ML models at worker startup so they're ready for tasks immediately.
    If a GPU worker cannot access CUDA, exits immediately so Docker can restart
    the container with a fresh NVIDIA runtime connection."""
    import logging

    SpeechToTextTask._ensure_models_loaded()
    _start_heartbeat_loop()

    if SpeechToTextTask._gpu_degraded:
        logger = logging.getLogger(__name__)
        logger.critical(
            "GPU worker started but CUDA is unavailable (NVIDIA driver crashed). "
            "Stopping container so Docker can restart it with a fresh driver connection."
        )
        # sys.exit() would only kill this forked child process, not the
        # Celery main process. Send SIGTERM to PID 1 (the container's
        # entrypoint) to trigger a full container stop and restart.
        import os, signal
        os.kill(1, signal.SIGTERM)


@worker_shutdown.connect
def cleanup_ready_key(**kwargs):
    """Remove readiness and device keys from Redis when worker shuts down."""
    global _heartbeat_timer
    if _heartbeat_timer:
        _heartbeat_timer.cancel()
    try:
        _heartbeat_redis.delete(f'worker:ready:{_worker_hostname}')
        _heartbeat_redis.delete(f'worker:device:{_worker_hostname}')
    except Exception:
        pass


@app.task(name='speech_to_text',
          ignore_result=False,
          bind=True,
          base=SpeechToTextTask,
          serializer='json')
def speech_to_text(self, audio_file_path, task='transcribe', short_form=False):
    sampling_rate = 16000

    # Pre-task GPU health check — detect and recover from GPU degradation
    self.ensure_gpu_healthy()

    #
    print("Task speech to text for %s received" % audio_file_path)

    #
    audio_id = Path(audio_file_path).stem
    logger = get_logger(audio_id, log_to_file=not short_form)
    logger.info(f"[WORKER] Speech-to-text task received for {audio_file_path}, task mode: {task}")
    _refresh_worker_heartbeat()
    logger.info(f"[WORKER] Running on device: {self.device} (requested: {type(self)._requested_device})")

    try:
        return _speech_to_text_inner(self, audio_file_path, audio_id, task, short_form, sampling_rate, logger)
    except Exception as e:
        logger.error(f"[WORKER] Task failed with exception: {type(e).__name__}: {e}")
        raise


def _speech_to_text_inner(self, audio_file_path, audio_id, task, short_form, sampling_rate, logger):
    welsh_normalizer = WelshNormalizer()

    def generate_md5_hex(audio_segment):
        """Generate MD5 hash from audio segment data efficiently."""
        return hashlib.md5(audio_segment.tobytes()).hexdigest()

    def whisperx_transcribe(audio, lang='', task='transcribe', skip_alignment=False):
        with _redirect_print_to_logger(logger):
            whisper_result = self.model.transcribe(
                audio, batch_size=2, language=lang, task=task,
                print_progress=not short_form,
            )
        if task == 'translate':
            return whisper_result
        if skip_alignment:
            return whisper_result
        if type(self)._align_model is None:
            logger.info(f"[WORKER] Alignment model not loaded — skipping alignment")
            return whisper_result
        return whisperx.align(whisper_result["segments"],
                              self.align_model,
                              self.align_metadata,
                              audio,
                              self.device,
                              return_char_alignments='words')

    wav_audio_file_path, audio_is_pcm = prepare_audio(audio_file_path)
    logger.info(f"[WORKER] Audio prepared: {wav_audio_file_path} (pcm_compatible={audio_is_pcm})")

    # loads audio file into numpy array
    if audio_is_pcm:
        logger.info(f"[WORKER] Loading audio via fast PCM reader (no ffmpeg)")
        audio = load_audio_fast(wav_audio_file_path)
    else:
        logger.info(f"[WORKER] Loading audio via whisperx (ffmpeg)")
        audio = whisperx.load_audio(wav_audio_file_path, sr=sampling_rate)

    # Calculate duration for short audio optimizations (only applied to short_form requests)
    audio_duration_seconds = len(audio) / sampling_rate
    skip_alignment = False
    if short_form:
        align_min_duration = float(os.environ.get('ALIGN_MIN_DURATION_SECONDS', 30))
        skip_alignment = audio_duration_seconds < align_min_duration
        if skip_alignment:
            logger.info(f"[WORKER] Short-form: short audio ({audio_duration_seconds:.1f}s < {align_min_duration:.0f}s) — will skip alignment")

    logger.info(f"[WORKER] Starting WhisperX {task}")
    whisperx_result = whisperx_transcribe(audio, task=task, skip_alignment=skip_alignment)
    total_segments = len(whisperx_result.get('segments', []))
    logger.info(f"[WORKER] WhisperX {task} complete, {total_segments} segments found")

    # Translation: skip diarization (no alignment data, English output)
    # Transcription: full pipeline with diarization and speaker assignment
    # Short audio: skip diarization (configurable threshold)
    diarize_segments = None
    diarize_min_duration = float(os.environ.get('DIARIZE_MIN_DURATION_SECONDS', 30))
    skip_diarization = short_form and audio_duration_seconds < diarize_min_duration

    if task == 'translate':
        logger.info(f"[WORKER] Translation mode — skipping diarization")
        result = whisperx_result
    elif skip_diarization:
        logger.info(f"[WORKER] Short-form: short audio ({audio_duration_seconds:.1f}s < {diarize_min_duration:.0f}s) — skipping diarization")
        result = whisperx_result
    elif type(self)._diarize_model is None:
        logger.info(f"[WORKER] Diarization model not loaded — skipping diarization")
        result = whisperx_result
    else:
        logger.info(f"[WORKER] Starting speaker diarization")
        diarize_segments = self.diarize_model(audio)
        logger.info(f"[WORKER] Speaker diarization complete")

        logger.info(f"[WORKER] Assigning speakers to words")
        result = whisperx.assign_word_speakers(diarize_segments, whisperx_result)

        last_speaker = ""
        last_end = ""
        speaker_map = []
        sentence = {
            "speaker": "",
            "text": "",
            "start": "",
            "end": ""
        }

        for segment in result['segments']:
            for word in segment['words']:
                if 'speaker' in word:
                    speaker_id = word['speaker']
                    speaker_id = speaker_id.replace("SPEAKER", "SIARADWR")
                else:
                    speaker_id = "ANHYSBYS"
                if speaker_id != last_speaker:
                    if sentence["text"] != "":
                        sentence["end"] = last_end
                        speaker_map.append(sentence)
                    sentence = {
                        "speaker": speaker_id,
                        "text": word['word'],
                        "start": word['start'],
                    }
                else:
                    sentence["text"] += " " + word['word']
                last_speaker = speaker_id
                last_end = word['end']

        if sentence["text"] != "":
            sentence["end"] = last_end
            speaker_map.append(sentence)

        logger.info(f"[WORKER] Speaker mapping complete, {len(speaker_map)} speaker segments created")

        speakers = {
            'id': audio_id,
            'version': 2,
            'success': True,
            'segments': speaker_map
        }

        logger.info(f"[WORKER] Saving speakers JSON file")
        save_as_speakers(wav_audio_file_path, speakers, logger)

    # add an id to each segment, based on the audio data
    segments = list()
    total_result_segments = len(result['segments'])
    logger.info(f"[WORKER] Processing {total_result_segments} segments")

    for segment_idx, segment in enumerate(result['segments'], 1):
        #
        start_time = int(segment['start'] * 1000)
        end_time = int(segment['end'] * 1000)

        if start_time >= end_time:
            continue

        if segment['text'] is None:
            continue

        whisper_text = segment['text'].strip()

        # Log progress for each segment with duration
        segment_duration = segment['end'] - segment['start']
        logger.info(f"[WORKER] Processing segment {segment_idx}/{total_result_segments} (duration: {segment_duration:.2f}s): {whisper_text[:50]}{'...' if len(whisper_text) > 50 else ''}")

        # Generate MD5 from audio segment data for unique identification
        audio_segment_id = generate_md5_hex(audio[start_time:end_time])

        # Normalize text: Welsh normalization for transcription, skip for translation
        if task == 'translate':
            normalized_text = whisper_text
        else:
            normalized_text = welsh_normalizer.normalize(whisper_text)

        # Word scores: available after alignment (transcription), not for translation
        try:
            score = np.mean([word['score'] for word in segment.get('words', [])])
            if np.isnan(score):
                score = 0.0
        except (KeyError, ValueError, TypeError):
            score = 0.0

        segments.append(
            {
                'audio_id': audio_segment_id,
                'start': segment['start'],
                'end': segment['end'],
                'text': whisper_text,
                'normalized': normalized_text,
                'score': score,
                'words': segment.get('words', []),
                'chars': segment.get('chars', [])
            }
        )

    # Language detection
    if task == 'translate':
        # Translation output is always English
        language_code = 'en'
        logger.info(f"[WORKER] Translation mode — output language: en")
    else:
        # Extract language code from WhisperX result
        whisper_language = whisperx_result.get('language', 'en')
        logger.info(f"[WORKER] Whisper detected language: {whisper_language}")

        # Backup language detection from transcribed text using Lingua
        full_text = ' '.join([seg['text'] for seg in segments if seg['text']])

        if full_text.strip():
            detected_lang = self.lang_detector.detect_language_of(full_text)
            if detected_lang == Language.WELSH:
                text_based_language = 'cy'
            elif detected_lang == Language.ENGLISH:
                text_based_language = 'en'
            else:
                text_based_language = whisper_language
            logger.info(f"[WORKER] Text-based language detection: {text_based_language}")
        else:
            text_based_language = whisper_language
            logger.info(f"[WORKER] No text for language detection, using Whisper's result: {whisper_language}")

        language_code = text_based_language
        logger.info(f"[WORKER] Final language: {language_code}")

    result = {
        'id': audio_id,
        'version': 2,
        'success': True,
        'language': language_code,
        'segments': segments
    }

    logger.info(f"[WORKER] Processed {len(segments)} segments")

    if short_form:
        # Short-form: skip all file I/O — result is returned via Celery/Redis,
        # and the uploaded audio lives on tmpfs so will be cleaned up below.
        logger.info(f"[WORKER] Short-form: skipping file saves (result returned via Redis)")
    else:
        logger.info(f"[WORKER] Saving output files")
        save_as_json(wav_audio_file_path, result, logger)
        save_as_text(wav_audio_file_path, result, logger)
        save_as_elan(wav_audio_file_path, result, logger)
        save_as_srt(wav_audio_file_path, result, language_code, logger)
        save_as_vtt(wav_audio_file_path, result, language_code, logger)
        logger.info(f"[WORKER] Output files saved successfully")

    logger.info(f"[WORKER] Task complete.")

    # Return result before cleanup (caller needs segments)
    result_to_return = result.copy()

    # Short-form: delete the uploaded audio and log from tmpfs
    if short_form:
        recordings_dir = Path(wav_audio_file_path).parent
        for f in recordings_dir.glob(f"{audio_id}.*"):
            try:
                f.unlink()
            except OSError:
                pass

    # Cleanup to prevent memory leaks
    del audio
    del whisperx_result
    if diarize_segments is not None:
        del diarize_segments
    del segments

    # Force garbage collection for large arrays
    gc.collect()

    # Clear GPU cache if using CUDA
    if self.device == "cuda" and torch.cuda.is_available():
        torch.cuda.empty_cache()

    return result_to_return


@app.task(name='align_audio',
          ignore_result=False,
          bind=True,
          base=SpeechToTextTask,
          serializer='json')
def align_audio(self, audio_file_path, text):
    """Align user-provided text to audio using wav2vec2 forced alignment.

    Accepts a single text block and aligns it against the entire audio file,
    returning word-level timestamps and confidence scores.
    No transcription (Whisper) is needed — uses wav2vec2 CTC alignment directly.

    Runs on a dedicated CPU-only worker (alignment queue) to avoid CUDA OOM
    on long audio and to keep GPU workers free for transcription.
    """
    sampling_rate = 16000

    audio_id = Path(audio_file_path).stem
    logger = get_logger(audio_id)
    logger.info(f"[WORKER] Alignment task received for {audio_file_path}")
    _refresh_worker_heartbeat()
    logger.info(f"[WORKER] Running on device: {self.device} (requested: {type(self)._requested_device})")

    try:
        return _align_audio_inner(self, audio_file_path, audio_id, text, sampling_rate, logger)
    except Exception as e:
        logger.error(f"[WORKER] Alignment task failed with exception: {type(e).__name__}: {e}")
        raise


def _align_audio_inner(self, audio_file_path, audio_id, text, sampling_rate, logger):
    wav_audio_file_path, audio_is_pcm = prepare_audio(audio_file_path)
    logger.info(f"[WORKER] Audio prepared: {wav_audio_file_path} (pcm_compatible={audio_is_pcm})")

    if audio_is_pcm:
        logger.info(f"[WORKER] Loading audio via fast PCM reader (no ffmpeg)")
        audio = load_audio_fast(wav_audio_file_path)
    else:
        logger.info(f"[WORKER] Loading audio via whisperx (ffmpeg)")
        audio = whisperx.load_audio(wav_audio_file_path, sr=sampling_rate)
    duration = len(audio) / float(sampling_rate)
    logger.info(f"[WORKER] Audio loaded, duration: {duration:.2f}s")

    # Reject audio too short for wav2vec2 alignment (causes crashes under ~0.1s)
    min_duration = 0.1
    if duration < min_duration:
        logger.warning(
            f"[WORKER] Rejecting alignment: audio too short ({duration:.3f}s). "
            f"Minimum duration: {min_duration}s"
        )
        del audio
        gc.collect()
        error_result = {
            'id': audio_id,
            'version': 2,
            'success': False,
            'message': (
                f"Audio too short for alignment: {duration:.3f}s. "
                f"Minimum duration: {min_duration}s."
            )
        }
        save_as_json(wav_audio_file_path, error_result, logger)
        return error_result

    # Validate text-to-audio ratio to reject absurd jobs
    # (e.g. 3 words for 20 minutes of audio will hang the worker)
    word_count = len(text.split())
    min_words_per_second = 0.1  # At least 1 word per 10 seconds of audio
    if duration > 0 and word_count / duration < min_words_per_second:
        ratio = word_count / duration
        logger.warning(
            f"[WORKER] Rejecting alignment: text too short for audio duration. "
            f"{word_count} words / {duration:.1f}s = {ratio:.4f} words/sec "
            f"(minimum: {min_words_per_second})"
        )
        # Cleanup
        del audio
        gc.collect()
        error_result = {
            'id': audio_id,
            'version': 2,
            'success': False,
            'message': (
                f"Text too short for audio duration: {word_count} words for {duration:.0f}s of audio "
                f"({ratio:.4f} words/sec). Minimum ratio: {min_words_per_second} words/sec "
                f"(~1 word per 10 seconds). Please provide more text or shorter audio."
            )
        }
        save_as_json(wav_audio_file_path, error_result, logger)
        return error_result

    # Single segment: align the entire text against the full audio
    segments = [{"start": 0.0, "end": duration, "text": text}]

    logger.info(f"[WORKER] Starting wav2vec2 forced alignment on {self.device}")
    aligned = whisperx.align(
        segments,
        self.align_model,
        self.align_metadata,
        audio,
        self.device,
        return_char_alignments=True
    )
    logger.info(f"[WORKER] Alignment complete")

    # Build result
    aligned_segments = []
    for segment in aligned.get('segments', []):
        aligned_segments.append({
            'start': segment.get('start', 0.0),
            'end': segment.get('end', duration),
            'text': segment.get('text', text),
            'words': segment.get('words', []),
            'chars': segment.get('chars', [])
        })

    result = {
        'id': audio_id,
        'version': 2,
        'success': True,
        'language': os.environ.get("WHISPER_MODEL_LANGUAGE", "cy"),
        'segments': aligned_segments,
        'word_segments': aligned.get('word_segments', [])
    }

    logger.info(f"[WORKER] Alignment task complete. Saving result.")
    save_as_json(wav_audio_file_path, result, logger)

    # Cleanup
    del audio
    gc.collect()
    if self.device == "cuda" and torch.cuda.is_available():
        torch.cuda.empty_cache()

    return result
