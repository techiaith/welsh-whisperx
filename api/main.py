import os
import sys
import json
import uuid
import httpx

import aiofiles
import traceback

from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, UploadFile, File, Request, Form, Depends, HTTPException
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware

from celery import Celery
from celery.result import AsyncResult

# Add shared directory to path for logger
sys.path.append('/app/shared')
from stt_logger import get_logger

from files_store import get_if_exists_file_path, save_sound_file, delete_all_files
from task_store import task_store
from validation import validate_stt_id
from health import get_comprehensive_health, check_readiness, check_liveness
from queue_inspector import get_queue_status
from cleanup_scheduler import start_cleanup_scheduler, stop_cleanup_scheduler, run_cleanup_now


UPLOAD_DIR = "/recordings"

REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')
BACKEND_CONN_URI = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
BROKER_CONN_URI=BACKEND_CONN_URI

# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize cleanup scheduler
    logger = get_logger('startup')
    logger.info("Starting WhisperX API server")
    scheduler = start_cleanup_scheduler(app)

    # Store scheduler in app state for access in endpoints
    app.state.cleanup_scheduler = scheduler

    yield

    # Shutdown: Stop cleanup scheduler
    logger.info("Shutting down WhisperX API server")
    if scheduler:
        stop_cleanup_scheduler(scheduler)

tags_metadata = [
    {"name": "Trawsgrifio / Transcription", "description": "Lleferydd Cymraeg i destun Cymraeg / Welsh speech to Welsh text"},
    {"name": "Cyfieithu / Translation", "description": "Lleferydd Cymraeg i destun Saesneg / Welsh speech to English text"},
    {"name": "Alinio / Alignment", "description": "Alinio testun i sain gan ddefnyddio wav2vec2 / Align text to audio using wav2vec2"},
    {"name": "Canlyniadau / Results", "description": "Lawrlwytho canlyniadau trawsgrifio / Download transcription results"},
]

app = FastAPI(
    title="WhisperX STT API",
    description="API adnabod lleferydd Cymraeg / Welsh speech recognition API. "
                "Trawsgrifio, cyfieithu ac alinio lleferydd Cymraeg / "
                "Transcribe, translate and align Welsh speech.",
    version="2.0",
    openapi_tags=tags_metadata,
    lifespan=lifespan,
)

# Configure CORS to allow browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins - restrict in production if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

celery = Celery('tasks', broker=BROKER_CONN_URI, backend=BACKEND_CONN_URI)

# Configure Celery with both named queues AND numeric priorities
#
# Queue routing (processed in order):
#   1. high_priority: Keyboard/real-time (checked first)
#   2. default: Normal batch (checked second)
#
# Within each queue, numeric priorities apply:
#   0 = urgent, 5 = normal, 9 = low
#
# Example: high_priority[priority=9] still beats default[priority=0]
celery.conf.update(
    result_expires=7 * 24 * 60 * 60,  # 7 days (matches task_store TTL)
    task_track_started=True,  # Track STARTED state for better status monitoring
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    task_default_queue='default',  # Default to normal queue
    task_routes={
        'speech_to_text': {'queue': 'default'},  # Can be overridden at send time
        'align_audio': {'queue': 'default'},      # Can be overridden at send time
    },
    task_queue_max_priority=10,      # Enable priorities 0-9 within each queue
    task_default_priority=5,         # Default to normal priority
    worker_prefetch_multiplier=1,    # Check queue after each task (enables priorities)
)


@app.get('/version/', include_in_schema=False)
async def version():
    """Fersiwn yr API / API version number."""
    return {
        'version': 2
    }


@app.get('/get_status/', tags=["Canlyniadau / Results"])
async def get_status(stt_id: str = Depends(validate_stt_id)):
    """Gwirio statws tasg trawsgrifio (PENDING, STARTED, SUCCESS, FAILURE).
    Dychwelyd logiau'r gweithiwr hefyd.

    Check transcription task status (PENDING, STARTED, SUCCESS, FAILURE).
    Also returns worker logs for the task."""
    # Retrieve task_id from Redis - survives server restarts
    task_status = "UNKNOWN"
    task_id = task_store.get_task_id(stt_id)
    if task_id:
        task_result = AsyncResult(task_id)
        task_status = task_result.status
    
    # Read the log file if it exists
    log_content = []
    log_file_path = os.path.join(UPLOAD_DIR, f"{stt_id}.log")
    if Path(log_file_path).is_file():
        try:
            async with aiofiles.open(log_file_path, 'r', encoding='utf-8') as log_file:
                log_content = await log_file.readlines()
                # Strip newlines and keep only non-empty lines
                log_content = [line.strip() for line in log_content if line.strip()]
        except Exception as e:
            log_content = [f"Error reading log file: {str(e)}"]

    #
    result = {
        'version': 2,
        'status': task_status,
        'log': log_content
    }

    #
    return result


@app.post('/transcribe/', tags=["Trawsgrifio / Transcription"])
async def transcribe(
    soundfile: UploadFile = File(..., description="Ffeil sain / Audio file (wav, mp3, ogg, etc.)"),
    priority: str = Form('high', description="Blaenoriaeth / Priority: 'high' neu/or 'normal'")
):
    """Trawsgrifio sain byr yn gydamserol. Uchafswm maint: 480KB.
    Dychwelyd y canlyniad yn syth ar ffurf data JSON.

    Transcribe short audio synchronously. Max file size: 480KB.
    Returns the result directly in the response as JSON data."""
    stt_id = str(uuid.uuid4())
    logger = get_logger(stt_id)
    logger.info(f"[API] New transcription request - endpoint: /transcribe/, stt_id: {stt_id}, priority: {priority}")

    #
    audio_file_path, audio_file_size = await save_sound_file(stt_id, soundfile)
    logger.info(f"[API] Audio file saved: {audio_file_path}, size: {audio_file_size} bytes")

    #
    if audio_file_size < 480000:
        # /transcribe/ always routes to high_priority queue
        # (synchronous endpoint - user is waiting for response)
        task_priority = 0 if priority == 'high' else 5

        logger.info(f"[API] Sending task to queue 'high_priority' with priority {task_priority} ({priority}) for processing")
        transcription_task = celery.send_task(
            'speech_to_text',
            args=(audio_file_path, 'transcribe'),
            queue='high_priority',
            priority=task_priority
        )
        task_result = transcription_task.get(timeout=60.0)
        result = task_result
        logger.info(f"[API] Transcription completed successfully")
    else:
        logger.warning(f"[API] Audio file too large ({audio_file_size} bytes)")
        result = {
            'id': stt_id,
            'version':2,
            'success':False,
            'message':"The soundfile was too large. Use 'transcribe_long_form' for longer audio."
        }

    return result


@app.post('/keyboard/', response_class=PlainTextResponse, tags=["Trawsgrifio / Transcription"])
async def transcribe_for_keyboard(
    audio_file: UploadFile = File(..., description="Ffeil sain / Audio file (wav, mp3, ogg, etc.)"),
):
    """Trawsgrifio ar gyfer bysellfwrdd — dychwelyd testun plaen.
    Blaenoriaeth uchel, uchafswm maint: 480KB.

    Transcribe for keyboard input — returns a plain text.
    High priority, max file size: 480KB."""
    stt_id = str(uuid.uuid4())
    logger = get_logger(stt_id)
    logger.info(f"[API] New transcription request - endpoint: /keyboard/, stt_id: {stt_id}")

    audio_file_path, audio_file_size = await save_sound_file(stt_id, audio_file)
    logger.info(f"[API] Audio file saved: {audio_file_path}, size: {audio_file_size} bytes")

    if audio_file_size < 480000:
        # /keyboard/ always routes to high_priority queue with urgent priority
        # (real-time use case - user is typing and waiting)
        logger.info(f"[API] Sending task to queue 'high_priority' with priority 0 (high) for processing")
        transcription_task = celery.send_task(
            'speech_to_text',
            args=(audio_file_path, 'transcribe'),
            queue='high_priority',
            priority=0
        )
        task_result = transcription_task.get(timeout=60.0)

        # Extract text directly from task result (no file dependency)
        text = ''
        for segment in task_result.get('segments', []):
            text = text + segment.get('text', '').strip()
            if text.endswith('.'):
                text = text + ' '
        text = text.strip()

        logger.info(f"[API] Transcription completed successfully")
        return text
    else:
        logger.warning(f"[API] Audio file too large ({audio_file_size} bytes)")
        return ""
    

@app.post('/transcribe_long_form/', tags=["Trawsgrifio / Transcription"])
async def transcribe_long_form(
    request: Request,
    soundfile: UploadFile = File(..., description="Ffeil sain / Audio file (unrhyw faint / any size)"),
    priority: str = Form('normal', description="Blaenoriaeth / Priority: 'normal' neu/or 'low' (mae 'high' yn cael ei israddio / 'high' is demoted to 'normal')")
):
    """Trawsgrifio sain hir yn anghydamserol. Dim terfyn maint.
    Dychwelyd ID ar unwaith — defnyddiwch /get_json/, /get_srt/ ayb i nôl canlyniadau.

    Transcribe long audio asynchronously. No file size limit.
    Returns an ID immediately — use /get_json/, /get_srt/ etc. to retrieve results."""
    #
    stt_id = str(uuid.uuid4())
    logger = get_logger(stt_id)

    # Cap priority at 'normal' - demote 'high' requests
    if priority == 'high':
        priority = 'normal'
        logger.info(f"[API] New transcription request - endpoint: /transcribe_long_form/, stt_id: {stt_id}, priority: {priority} (demoted from high)")
    else:
        logger.info(f"[API] New transcription request - endpoint: /transcribe_long_form/, stt_id: {stt_id}, priority: {priority}")

    audio_file_path, audio_file_size = await save_sound_file(stt_id, soundfile)
    logger.info(f"[API] Audio file saved: {audio_file_path}, size: {audio_file_size} bytes")

    # /transcribe_long_form/ always routes to default queue
    # Maximum priority is 'normal' (5) - 'high' is demoted above
    task_priority = 9 if priority == 'low' else 5

    logger.info(f"[API] Sending task to queue 'default' with priority {task_priority} ({priority}) for processing")
    transcription_task = celery.send_task(
        'speech_to_text',
        args=(audio_file_path, 'transcribe'),
        queue='default',
        priority=task_priority
    )
    task_store.set_task_id(stt_id, transcription_task.task_id)
    logger.info(f"[API] Task sent to Celery, task_id: {transcription_task.task_id}")

    return {
        'id':stt_id,
        'version':2,
        'success':True
    }


@app.post('/translate/', tags=["Cyfieithu / Translation"])
async def translate(
    soundfile: UploadFile = File(..., description="Ffeil sain Cymraeg / Welsh audio file"),
    priority: str = Form('high', description="Blaenoriaeth / Priority: 'high' neu/or 'normal'")
):
    """Cyfieithu sain Cymraeg byr i destun Saesneg yn gydamserol. Uchafswm maint: 480KB.

    Translate short Welsh audio to English text synchronously. Max file size: 480KB."""
    stt_id = str(uuid.uuid4())
    logger = get_logger(stt_id)
    logger.info(f"[API] New translation request - endpoint: /translate/, stt_id: {stt_id}, priority: {priority}")

    audio_file_path, audio_file_size = await save_sound_file(stt_id, soundfile)
    logger.info(f"[API] Audio file saved: {audio_file_path}, size: {audio_file_size} bytes")

    if audio_file_size < 480000:
        task_priority = 0 if priority == 'high' else 5

        logger.info(f"[API] Sending translate task to queue 'high_priority' with priority {task_priority} ({priority})")
        translation_task = celery.send_task(
            'speech_to_text',
            args=(audio_file_path, 'translate'),
            queue='high_priority',
            priority=task_priority
        )
        task_result = translation_task.get(timeout=60.0)
        result = task_result
        logger.info(f"[API] Translation completed successfully")
    else:
        logger.warning(f"[API] Audio file too large ({audio_file_size} bytes)")
        result = {
            'id': stt_id,
            'version': 2,
            'success': False,
            'message': "The soundfile was too large. Use 'translate_long_form' for longer audio."
        }

    return result


@app.post('/translate_long_form/', tags=["Cyfieithu / Translation"])
async def translate_long_form(
    request: Request,
    soundfile: UploadFile = File(..., description="Ffeil sain Cymraeg / Welsh audio file (unrhyw faint / any size)"),
    priority: str = Form('normal', description="Blaenoriaeth / Priority: 'normal' neu/or 'low' (mae 'high' yn cael ei israddio / 'high' is demoted to 'normal')")
):
    """Cyfieithu sain Cymraeg hir i destun Saesneg yn anghydamserol. Dim terfyn maint.
    Dychwelyd ID ar unwaith — defnyddiwch /get_json/, /get_srt/ ayb i nôl canlyniadau.

    Translate long Welsh audio to English text asynchronously. No file size limit.
    Returns an ID immediately — use /get_json/, /get_srt/ etc. to retrieve results."""
    stt_id = str(uuid.uuid4())
    logger = get_logger(stt_id)

    # Cap priority at 'normal' — demote 'high' requests
    if priority == 'high':
        priority = 'normal'
        logger.info(f"[API] New translation request - endpoint: /translate_long_form/, stt_id: {stt_id}, priority: {priority} (demoted from high)")
    else:
        logger.info(f"[API] New translation request - endpoint: /translate_long_form/, stt_id: {stt_id}, priority: {priority}")

    audio_file_path, audio_file_size = await save_sound_file(stt_id, soundfile)
    logger.info(f"[API] Audio file saved: {audio_file_path}, size: {audio_file_size} bytes")

    task_priority = 9 if priority == 'low' else 5

    logger.info(f"[API] Sending translate task to queue 'default' with priority {task_priority} ({priority})")
    translation_task = celery.send_task(
        'speech_to_text',
        args=(audio_file_path, 'translate'),
        queue='default',
        priority=task_priority
    )
    task_store.set_task_id(stt_id, translation_task.task_id)
    logger.info(f"[API] Task sent to Celery, task_id: {translation_task.task_id}")

    return {
        'id': stt_id,
        'version': 2,
        'success': True
    }


@app.post('/align/', tags=["Alinio / Alignment"])
async def align_audio_endpoint(
    soundfile: UploadFile = File(..., description="Ffeil sain / Audio file"),
    text: str = Form(..., description="Y testun i'w alinio â'r sain / Text to align against the audio"),
):
    """Alinio testun â sain gan ddefnyddio wav2vec2 forced alignment.
    Dychwelyd stampiau amser ar lefel geiriau a chymeriadau.
    Uchafswm maint: 480KB. Dim trawsgrifio — alinio'n unig.

    Align text to audio using wav2vec2 forced alignment.
    Returns word-level and character-level timestamps with confidence scores.
    Max file size: 480KB. No transcription — alignment only."""
    stt_id = str(uuid.uuid4())
    logger = get_logger(stt_id)
    logger.info(f"[API] New alignment request - endpoint: /align/, stt_id: {stt_id}, text length: {len(text)} chars")

    audio_file_path, audio_file_size = await save_sound_file(stt_id, soundfile)
    logger.info(f"[API] Audio file saved: {audio_file_path}, size: {audio_file_size} bytes")

    if audio_file_size < 480000:
        logger.info(f"[API] Sending align task to queue 'high_priority' with priority 0 (urgent)")
        align_task = celery.send_task(
            'align_audio',
            args=(audio_file_path, text),
            queue='high_priority',
            priority=0
        )
        task_result = align_task.get(timeout=60.0)
        result = task_result
        logger.info(f"[API] Alignment completed successfully")
    else:
        logger.warning(f"[API] Audio file too large ({audio_file_size} bytes)")
        result = {
            'id': stt_id,
            'version': 2,
            'success': False,
            'message': "The soundfile was too large for alignment. Maximum size: 480KB."
        }

    return result


@app.get('/get_speakers/', response_class=FileResponse, tags=["Canlyniadau / Results"])
async def get_speakers(stt_id: str = Depends(validate_stt_id)):
    """Lawrlwytho canlyniad diarization siaradwyr (JSON).

    Download speaker diarization result (JSON)."""
    json_file_path = Path(os.path.join(UPLOAD_DIR, stt_id + ".speakers.json"))

    if not json_file_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Speaker diarization file not found. Check transcription status with /get_status/?stt_id={stt_id}"
        )

    return json_file_path


@app.get('/get_json/', response_class=FileResponse, tags=["Canlyniadau / Results"])
async def get_json(stt_id: str = Depends(validate_stt_id)):
    """Lawrlwytho canlyniad trawsgrifio/cyfieithu llawn (JSON gyda segmentau, geiriau, sgoriau).

    Download full transcription/translation result (JSON with segments, words, scores)."""
    json_file_path = Path(os.path.join(UPLOAD_DIR, stt_id + ".json"))

    if not json_file_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Transcription file not found. Check status with /get_status/?stt_id={stt_id}"
        )

    return json_file_path


@app.get('/get_elan/', response_class=FileResponse, tags=["Canlyniadau / Results"])
async def get_elan(stt_id: str = Depends(validate_stt_id)):
    """Lawrlwytho ffeil anodi ELAN (.eaf) ar gyfer dadansoddi ieithyddol.

    Download ELAN annotation file (.eaf) for linguistic analysis."""
    eaf_file_path = Path(os.path.join(UPLOAD_DIR, stt_id + ".eaf"))

    if not eaf_file_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"ELAN annotation file not found. Check transcription status with /get_status/?stt_id={stt_id}"
        )

    return eaf_file_path


@app.get('/get_srt/', response_class=FileResponse, tags=["Canlyniadau / Results"])
async def get_srt(stt_id: str = Depends(validate_stt_id)):
    """Lawrlwytho ffeil isdeitlau SRT.

    Download SRT subtitle file."""
    srt_file_path = Path(os.path.join(UPLOAD_DIR, stt_id + ".srt"))

    if not srt_file_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"SRT subtitle file not found. Check transcription status with /get_status/?stt_id={stt_id}"
        )

    return srt_file_path


@app.get('/get_vtt/', response_class=FileResponse, tags=["Canlyniadau / Results"])
async def get_vtt(stt_id: str = Depends(validate_stt_id)):
    """Lawrlwytho ffeil isdeitlau WebVTT.

    Download WebVTT subtitle file."""
    vtt_file_path = Path(os.path.join(UPLOAD_DIR, stt_id + ".vtt"))

    if not vtt_file_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"VTT subtitle file not found. Check transcription status with /get_status/?stt_id={stt_id}"
        )

    return vtt_file_path


@app.get('/get_wav/', response_class=FileResponse, tags=["Canlyniadau / Results"])
async def get_wav(stt_id: str = Depends(validate_stt_id)):
    """Lawrlwytho'r ffeil sain WAV gwreiddiol (wedi'i drawsnewid i 16kHz mono).

    Download the original WAV audio file (converted to 16kHz mono)."""
    wav_file_path = Path(os.path.join(UPLOAD_DIR, stt_id + ".wav"))

    if not wav_file_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Audio file not found. Check transcription status with /get_status/?stt_id={stt_id}"
        )

    return wav_file_path


@app.get("/delete/", tags=["Canlyniadau / Results"])
async def delete(stt_id: str = Depends(validate_stt_id)):
    """Dileu pob ffeil sy'n gysylltiedig â thasg trawsgrifio.
    Yn dileu ffeiliau sain, canlyniadau a logiau.

    Delete all files associated with a transcription job.
    Removes audio files, transcription results, and logs."""
    result = True
    error_message = ""

    # delete files
    try:
        await delete_all_files(stt_id=stt_id)
    except Exception as e:
        result = False
        error_message = f"Failed to delete files: {str(e)}"
        traceback.print_exc()

    #
    response = {
        'id':stt_id,
        'version':2,
        'success':result
    }

    if error_message:
        response['message'] = error_message

    return response


@app.get('/health/', include_in_schema=False)
async def health():
    """Gwiriad iechyd cynhwysfawr — Redis, gweithwyr Celery, a statws modelau.

    Comprehensive health check — Redis, Celery workers, and model loading status."""
    return await get_comprehensive_health(celery)


@app.get('/health/ready/', include_in_schema=False)
async def readiness():
    """Prawf parodrwydd ar gyfer llwyth-gydbwysyddion. 200 os yn barod, 503 fel arall.

    Readiness probe for load balancers. Returns 200 if ready, 503 otherwise."""
    try:
        return await check_readiness()
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f'Service not ready: {str(e)}'
        )


@app.get('/health/live/', include_in_schema=False)
async def liveness():
    """Prawf bywiogrwydd — 200 os yw'r broses API yn fyw ac yn ymateb.

    Liveness probe — returns 200 if the API process is alive and responding."""
    return await check_liveness()


@app.get('/queue/status/', include_in_schema=False)
async def queue_status():
    """Archwilio statws ciwiau Celery — tasgau gweithredol, wedi'u trefnu a chadw.

    Inspect Celery queue status — active, scheduled and reserved tasks."""
    return await get_queue_status(celery)


@app.post('/cleanup/run/', include_in_schema=False)
async def cleanup_run():
    """Sbarduno glanhau ffeiliau hen â llaw.

    Manually trigger cleanup of files older than the retention period."""
    return await run_cleanup_now()


@app.get('/cleanup/status/', include_in_schema=False)
async def cleanup_status(request: Request):
    """Statws a chyfluniad y trefnydd glanhau.

    Cleanup scheduler status and configuration. Shows next run time and retention settings."""
    import os
    from datetime import datetime

    cleanup_enabled = os.environ.get('CLEANUP_ENABLED', 'true').lower() == 'true'
    retention_days = int(os.environ.get('FILE_RETENTION_DAYS', '14'))
    cleanup_schedule = os.environ.get('CLEANUP_SCHEDULE', '0 2 * * *')

    result = {
        'enabled': cleanup_enabled,
        'retention_days': retention_days,
        'schedule': cleanup_schedule,
        'next_run': None
    }

    # Get next run time from scheduler if available
    scheduler = getattr(request.app.state, 'cleanup_scheduler', None)
    if scheduler:
        job = scheduler.get_job('cleanup_old_files')
        if job:
            result['next_run'] = job.next_run_time.isoformat() if job.next_run_time else None

    return result

