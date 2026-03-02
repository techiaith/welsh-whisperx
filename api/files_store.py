import os
import glob
import traceback

import aiofiles

from pathlib import Path

#
UPLOAD_DIR = "/recordings"

def get_audio_file_path(stt_id):
    return os.path.join(UPLOAD_DIR, stt_id)

def get_file_path(stt_id, extension):
    return os.path.join(UPLOAD_DIR, stt_id + "." + extension)

def get_if_exists_file_path(stt_id, extension):
    p=os.path.join(UPLOAD_DIR, stt_id + "." + extension)
    if not Path(p).is_file():
        return ""
    return p


async def save_sound_file(stt_id, soundfile):
    audio_file_path = get_audio_file_path(stt_id)
    try:
        # Stream file in chunks to avoid loading entire file into memory
        chunk_size = 1024 * 1024  # 1MB chunks
        async with aiofiles.open(audio_file_path, 'wb') as f:
            while chunk := await soundfile.read(chunk_size):
                await f.write(chunk)
    except Exception as exc:
        traceback.print_exc()
        raise  # Re-raise exception so caller knows it failed

    return audio_file_path, os.path.getsize(audio_file_path)


async def append_data_chunk(stt_id, data):
    audio_file_path = get_audio_file_path(stt_id)
    if Path(audio_file_path).is_file():
        async with aiofiles.open(audio_file_path, 'ab') as f:
            await f.write(data)
    else:
        async with aiofiles.open(audio_file_path, 'wb') as f:
            await f.write(data)


async def delete_all_files(stt_id):
    for f in glob.glob(os.path.join(UPLOAD_DIR, stt_id + "*")):
        await aiofiles.os.remove(f)
