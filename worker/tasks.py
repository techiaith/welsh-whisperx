import hashlib
import os
import gc
import sys
from pathlib import Path

import numpy as np
import torch
import whisperx
from celery import Celery
from celery.signals import worker_process_init, worker_shutdown
from lingua import Language

# Add shared directory to path for logger
sys.path.append('/app/shared')
from stt_logger import get_logger

from audio_utils import prepare_audio
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
)


@worker_process_init.connect
def preload_models(**kwargs):
    """Load ML models at worker startup so they're ready for tasks immediately."""
    import socket
    import redis

    SpeechToTextTask._ensure_models_loaded()

    # Signal readiness to Redis so the health endpoint can report model status
    try:
        r = redis.Redis(
            host=os.environ.get('REDIS_HOST', 'redis'),
            port=int(os.environ.get('REDIS_PORT', 6379)),
            db=1
        )
        hostname = socket.gethostname()
        r.set(f'worker:ready:{hostname}', '1', ex=600)
    except Exception:
        pass


@worker_shutdown.connect
def cleanup_ready_key(**kwargs):
    """Remove readiness key from Redis when worker shuts down."""
    import socket
    import redis

    try:
        r = redis.Redis(
            host=os.environ.get('REDIS_HOST', 'redis'),
            port=int(os.environ.get('REDIS_PORT', 6379)),
            db=1
        )
        hostname = socket.gethostname()
        r.delete(f'worker:ready:{hostname}')
    except Exception:
        pass


@app.task(name='speech_to_text',
          ignore_result=False,
          bind=True,
          base=SpeechToTextTask,
          serializer='json')
def speech_to_text(self, audio_file_path, task='transcribe'):
    sampling_rate = 16000

    # Initialize Welsh normalizer
    welsh_normalizer = WelshNormalizer()

    def generate_md5_hex(audio_segment):
        """Generate MD5 hash from audio segment data efficiently."""
        # Convert numpy array slice to bytes efficiently
        return hashlib.md5(audio_segment.tobytes()).hexdigest()

    def whisperx_transcribe(audio, lang='', task='transcribe'):
        # transcribe or translate
        whisper_result = self.model.transcribe(audio, batch_size=2, language=lang, task=task)

        if task == 'translate':
            # Skip alignment — Welsh wav2vec2 can't align English text
            return whisper_result

        # align
        return whisperx.align(whisper_result["segments"],
                              self.align_model,
                              self.align_metadata,
                              audio,
                              self.device,
                              return_char_alignments='words')  # False)

    #
    print("Task speech to text for %s received" % audio_file_path)

    #
    audio_id = Path(audio_file_path).stem
    logger = get_logger(audio_id)
    logger.info(f"[WORKER] Speech-to-text task received for {audio_file_path}, task mode: {task}")

    wav_audio_file_path = prepare_audio(audio_file_path)
    logger.info(f"[WORKER] Audio prepared: {wav_audio_file_path}")

    # loads audio file into numpy array
    logger.info(f"[WORKER] Loading audio file into numpy array")
    audio = whisperx.load_audio(wav_audio_file_path, sr=sampling_rate)

    logger.info(f"[WORKER] Starting WhisperX {task}")
    whisperx_result = whisperx_transcribe(audio, task=task)
    total_segments = len(whisperx_result.get('segments', []))
    logger.info(f"[WORKER] WhisperX {task} complete, {total_segments} segments found")

    # Translation: skip diarization (no alignment data, English output)
    # Transcription: full pipeline with diarization and speaker assignment
    diarize_segments = None
    if task == 'translate':
        logger.info(f"[WORKER] Translation mode — skipping diarization")
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

    logger.info(f"[WORKER] Processed {len(segments)} segments, saving output files")
    save_as_json(wav_audio_file_path, result, logger)
    save_as_text(wav_audio_file_path, result, logger)
    save_as_elan(wav_audio_file_path, result, logger)
    save_as_srt(wav_audio_file_path, result, language_code, logger)
    save_as_vtt(wav_audio_file_path, result, language_code, logger)

    logger.info(f"[WORKER] All output files saved successfully. Task complete.")

    # Return result before cleanup (caller needs segments)
    result_to_return = result.copy()

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
    """
    sampling_rate = 16000

    audio_id = Path(audio_file_path).stem
    logger = get_logger(audio_id)
    logger.info(f"[WORKER] Alignment task received for {audio_file_path}")

    wav_audio_file_path = prepare_audio(audio_file_path)
    logger.info(f"[WORKER] Audio prepared: {wav_audio_file_path}")

    logger.info(f"[WORKER] Loading audio file into numpy array")
    audio = whisperx.load_audio(wav_audio_file_path, sr=sampling_rate)
    duration = len(audio) / float(sampling_rate)
    logger.info(f"[WORKER] Audio loaded, duration: {duration:.2f}s")

    # Single segment: align the entire text against the full audio
    segments = [{"start": 0.0, "end": duration, "text": text}]

    logger.info(f"[WORKER] Starting wav2vec2 forced alignment")
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

    logger.info(f"[WORKER] Alignment task complete. Returning result.")

    # Cleanup
    del audio
    gc.collect()
    if self.device == "cuda" and torch.cuda.is_available():
        torch.cuda.empty_cache()

    return result
