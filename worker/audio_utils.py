import json
import logging
import shlex
import subprocess

import numpy as np

from pathlib import Path

logger = logging.getLogger(__name__)

# Target format that whisperx.load_audio expects
TARGET_SR = 16000
TARGET_CHANNELS = 1
TARGET_CODEC = "pcm_s16le"
TARGET_FORMAT = "wav"


def prepare_audio(audio_file_path):
    """
    Prepare an audio file for WhisperX transcription.

    If the file is already 16kHz mono PCM WAV, return it as-is.
    Otherwise, convert and loudness-normalize in a single ffmpeg pass.

    Returns (wav_file_path, is_compatible) — when is_compatible is True,
    callers can use load_audio_fast() instead of whisperx.load_audio()
    to avoid spawning another ffmpeg subprocess.
    """
    audio_file_path = Path(audio_file_path)
    wav_file_path = audio_file_path.with_suffix(".wav")

    if _is_compatible(audio_file_path):
        logger.info(f"Audio already compatible (16kHz mono PCM WAV), skipping conversion: {audio_file_path}")
        # Ensure it has .wav extension for downstream code
        if audio_file_path.suffix.lower() != ".wav":
            audio_file_path.rename(wav_file_path)
            return wav_file_path.as_posix(), True
        return audio_file_path.as_posix(), True

    logger.info(f"Converting audio to 16kHz mono PCM WAV with loudness normalization: {audio_file_path}")
    # After conversion the output is guaranteed to be compatible PCM WAV
    return _convert_and_normalize(audio_file_path, wav_file_path), True


def _is_compatible(audio_file_path):
    """
    Check if an audio file is already 16kHz mono PCM WAV using ffprobe.
    Returns True if no conversion is needed.
    """
    try:
        probe_cmd = (
            f"ffprobe -v quiet -print_format json -show_streams "
            f"-show_format {shlex.quote(str(audio_file_path))}"
        )
        result = subprocess.run(
            shlex.split(probe_cmd),
            capture_output=True, timeout=10
        )
        if result.returncode != 0:
            return False

        info = json.loads(result.stdout)

        # Check format is WAV
        fmt = info.get("format", {}).get("format_name", "")
        if "wav" not in fmt:
            return False

        # Find the audio stream
        for stream in info.get("streams", []):
            if stream.get("codec_type") != "audio":
                continue
            codec = stream.get("codec_name", "")
            sample_rate = int(stream.get("sample_rate", 0))
            channels = int(stream.get("channels", 0))

            if codec == "pcm_s16le" and sample_rate == TARGET_SR and channels == TARGET_CHANNELS:
                return True

        return False
    except Exception as e:
        logger.debug(f"ffprobe check failed, will convert: {e}")
        return False


def _convert_and_normalize(audio_file_path, wav_file_path):
    """
    Single-pass ffmpeg: decode, resample to 16kHz mono, loudness-normalize, encode as PCM WAV.
    """
    convert_cmd = (
        f"ffmpeg -y -i {shlex.quote(str(audio_file_path))} "
        f"-vn -af loudnorm "
        f"-acodec {TARGET_CODEC} -ar {TARGET_SR} -ac {TARGET_CHANNELS} "
        f"{shlex.quote(str(wav_file_path))}"
    )

    result = subprocess.run(
        shlex.split(convert_cmd),
        capture_output=True, timeout=120
    )

    if result.returncode != 0:
        stderr = result.stderr.decode(errors="replace")
        logger.error(f"ffmpeg conversion failed: {stderr}")
        raise RuntimeError(f"ffmpeg conversion failed for {audio_file_path}: {stderr}")

    # Clean up original if it's a different file
    if audio_file_path.resolve() != wav_file_path.resolve():
        audio_file_path.unlink(missing_ok=True)

    logger.info(f"Audio prepared: {wav_file_path}")
    return wav_file_path.as_posix()


def load_audio_fast(wav_file_path):
    """
    Load a 16kHz mono PCM s16le WAV file directly into a numpy array,
    bypassing ffmpeg. Only safe to call on files already verified as compatible
    (i.e. output of prepare_audio).

    Returns a float32 numpy array normalized to [-1.0, 1.0], matching
    the output format of whisperx.load_audio().
    """
    raw = Path(wav_file_path).read_bytes()
    # Standard WAV header is 44 bytes; skip it to get raw PCM data
    # For robustness, find the 'data' chunk
    data_offset = raw.find(b'data')
    if data_offset == -1:
        raise RuntimeError(f"No 'data' chunk found in WAV file: {wav_file_path}")
    # 4 bytes after 'data' marker = chunk size, then PCM data starts
    pcm_start = data_offset + 8
    return np.frombuffer(raw[pcm_start:], dtype=np.int16).astype(np.float32) / 32768.0
