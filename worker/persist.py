import json
import pympi

from pathlib import Path

import xml.etree.ElementTree as et

from whisperx.SubtitlesProcessor import SubtitlesProcessor


def save_as_speakers(audio_file_path, transcription, logger=None):
    json_str = json.dumps(transcription)
    json_file_path = Path(audio_file_path).with_suffix(".speakers.json")
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json_file.write(json_str)
    if logger:
        logger.info(f"[WORKER] Saved speakers file: {json_file_path}")
    return json_file_path


def save_as_json(audio_file_path, transcription, logger=None):
    json_str = json.dumps(transcription)
    json_file_path = Path(audio_file_path).with_suffix(".json")
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json_file.write(json_str)
    if logger:
        logger.info(f"[WORKER] Saved JSON file: {json_file_path}")
    return json_file_path


def save_as_text(audio_file_path, transcription, logger=None):
    text = ''

    for transcript in transcription["segments"]:
        text = text + transcript["text"].strip()
        if text.endswith("."):
            text = text + " "

    text = text.strip()

    text_file_path = Path(audio_file_path).with_suffix(".txt")
    with open(text_file_path, 'w', encoding='utf-8') as text_file:
        text_file.write(text)

    if logger:
        logger.info(f"[WORKER] Saved text file: {text_file_path}")

    return text_file_path


def save_as_srt(audio_file_path, transcription, language_code='en', logger=None):
    """
    Save transcription as SRT subtitle file with advanced line splitting.
    Uses WhisperX SubtitlesProcessor for intelligent segmentation of long lines.

    Args:
        audio_file_path: Path to audio file (used to determine output filename)
        transcription: Transcription dict with 'segments' containing timing and text
        language_code: Two-letter language code (e.g., 'en', 'cy', 'es')
        logger: Optional logger instance
    """
    srt_file_path = Path(audio_file_path).with_suffix(".srt")

    # Extract segments from transcription
    segments = transcription.get("segments", [])

    if not segments:
        # Create empty SRT file if no segments
        with open(srt_file_path, 'w', encoding='utf-8') as srt_file:
            srt_file.write("")
        if logger:
            logger.warning(f"[WORKER] No segments found, created empty SRT file: {srt_file_path}")
        return srt_file_path

    # Use WhisperX SubtitlesProcessor for advanced splitting
    subtitles_processor = SubtitlesProcessor(
        segments,
        language_code,
        max_line_length=100,  # Optimal for readability
        min_char_length_splitter=70,  # Prevents over-splitting
        is_vtt=False  # Output SRT format
    )

    # Save with advanced splitting enabled
    subtitles_processor.save(str(srt_file_path), advanced_splitting=True)

    if logger:
        logger.info(f"[WORKER] Saved SRT file with advanced splitting: {srt_file_path}")
    else:
        print(f"SRT file of transcription saved to {srt_file_path}")

    return srt_file_path


def save_as_elan(audio_file_path, transcription, logger=None):
    i = 0

    #
    output_eaf = pympi.Elan.Eaf()

    audio_file = Path(audio_file_path)
    output_eaf.add_linked_file("get_audio?stt_id=" + audio_file.stem, mimetype="wav")

    output_eaf.add_tier('EDU')
    output_eaf.add_tier('EDU_W2V2')

    output_eaf.add_tier('Text')
    output_eaf.add_tier('Wav2Vec2')
    #
    for transcript in transcription["segments"]:
        i = i + 1
        if "start" in transcript and "end" in transcript:
            time_start = int(transcript["start"] * 1000)
            time_end = int(transcript["end"] * 1000)

            # ELAN.py raises ValueError exception if the segment is of length zero
            if time_start == time_end:
                continue

            if time_start > time_end:
                continue

            text = transcript["text"]
            output_eaf.insert_annotation('EDU', time_start, time_end, value=str(i))
            output_eaf.insert_ref_annotation('Text', 'EDU', time=time_start, value=text)

    #
    eaf_file_path = Path(audio_file_path).with_suffix(".eaf")
    output_eaf.to_file(eaf_file_path)

    # pympi deesn't note that timings are in milliseconds in the HEADER.
    eaf_xml = et.parse(eaf_file_path)
    eaf_xml = eaf_xml.getroot()
    h = eaf_xml.find(".//HEADER")
    h.set('TIME_UNITS', 'milliseconds')
    with open(eaf_file_path, 'wb') as eaf_file:
        eaf_file.write(et.tostring(eaf_xml))

    if logger:
        logger.info(f"[WORKER] Saved ELAN file: {eaf_file_path}")


def save_as_vtt(audio_file_path, transcription, language_code='en', logger=None):
    """
    Save transcription as VTT subtitle file with advanced line splitting.
    Uses WhisperX SubtitlesProcessor for intelligent segmentation of long lines.

    Args:
        audio_file_path: Path to audio file (used to determine output filename)
        transcription: Transcription dict with 'segments' containing timing and text
        language_code: Two-letter language code (e.g., 'en', 'cy', 'es')
        logger: Optional logger instance
    """
    vtt_file_path = Path(audio_file_path).with_suffix(".vtt")

    # Extract segments from transcription
    segments = transcription.get("segments", [])

    if not segments:
        # Create empty VTT file if no segments
        with open(vtt_file_path, 'w', encoding='utf-8') as vtt_file:
            vtt_file.write("WEBVTT\n\n")
        if logger:
            logger.warning(f"[WORKER] No segments found, created empty VTT file: {vtt_file_path}")
        return vtt_file_path

    # Use WhisperX SubtitlesProcessor for advanced splitting
    subtitles_processor = SubtitlesProcessor(
        segments,
        language_code,
        max_line_length=100,  # Optimal for readability
        min_char_length_splitter=70,  # Prevents over-splitting
        is_vtt=True  # Output VTT format
    )

    # Save with advanced splitting enabled
    subtitles_processor.save(str(vtt_file_path), advanced_splitting=True)

    if logger:
        logger.info(f"[WORKER] Saved VTT file with advanced splitting: {vtt_file_path}")
    else:
        print(f"VTT file of transcription saved to {vtt_file_path}")

    return vtt_file_path
