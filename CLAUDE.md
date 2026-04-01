# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Welsh speech-to-text server built on WhisperX with Welsh language optimizations. Provides transcription, translation (Welsh→English), and forced text-audio alignment via a REST API. Runs as Docker containers with GPU or CPU support.

## Commands

```bash
# First-time setup
make setup                    # Generate .env from config.env + .env.secrets

# Build and run
make build-gpu                # Build and start with GPU (production)
make build-cpu                # Build and start with CPU (development)

# Daily operations
make up-gpu / make up-cpu     # Start without rebuilding
make down                     # Stop all containers
make logs                     # Follow container logs
make status                   # Show running containers
make health                   # Check API health + queue status
make ready                    # Wait for models to finish loading (polls /health/)

# Scaling workers independently
make scale-high-gpu N=2       # Scale high-priority GPU workers
make scale-default-gpu N=3    # Scale default GPU workers
make scale-high-cpu N=2
make scale-default-cpu N=2

# Test API (requires speech.wav in project root)
make test

# Cleanup
make clean                    # Remove containers and images
make purge                    # Remove containers, images, and volumes (destructive)
```

The `make build` command runs `copy-shared.sh` to copy `shared/` into `api/shared/` and `worker/shared/` before building — this is why `api/shared/` and `worker/shared/` exist as duplicates.

## Architecture

```
FastAPI (port 5511) → Redis broker (port 6379) → Celery workers
```

**Services** (defined in `docker-compose.gpu.yml` / `docker-compose.cpu.yml`):
- `application` — FastAPI app (`api/`), handles HTTP requests, dispatches Celery tasks
- `worker-high` — GPU worker on GPU 1, consumes `high_priority` queue (`/transcribe/`, `/keyboard/`, `/translate/`)
- `worker-high-2` — GPU worker on GPU 0, consumes `high_priority` queue (dedicated GPU, overflow)
- `worker-default` — GPU worker on GPU 1, consumes `default` queue (`/transcribe_long_form/`, `/translate_long_form/`)
- `worker-alignment` — CPU worker ×2, consumes `alignment` queue (`/align/`, `/align_long_form/`)
- `redis` — Message broker and result backend; also used in db=1 for worker readiness signals

**Two-level priority system**: queue routing (which worker handles it) + numeric priorities within a queue (0=urgent, 5=normal). `worker_prefetch_multiplier=1` ensures idle workers pick up high-priority tasks immediately.

**Short audio optimisations** (thresholds configurable via env vars):
- `ALIGN_MIN_DURATION_SECONDS` — skips wav2vec2 alignment for short clips
- `DIARIZE_MIN_DURATION_SECONDS` — skips speaker diarization for short clips
- `SAVE_FILES_MIN_DURATION_SECONDS` — skips saving txt/srt/vtt/elan for short clips

## Key Files

| File | Purpose |
|------|---------|
| `api/main.py` | All API endpoints; Celery client config; task dispatch |
| `worker/tasks.py` | `speech_to_text` and `align_audio` Celery tasks; pipeline logic |
| `worker/speech_to_text_tasks.py` | `SpeechToTextTask` base class; ML model loading (Whisper, wav2vec2, pyannote diarization, Lingua) |
| `worker/normalization/welsh_normalizer.py` | Welsh text normalizer applied to every transcription segment |
| `worker/normalization/welsh_data.py` | Linguistic lookup tables (pronouns, contractions, dialectal forms, spelling) |
| `worker/persist.py` | Saves output files: `.json`, `.txt`, `.srt`, `.vtt`, `.eaf`, `.speakers.json` |
| `worker/audio_utils.py` | Converts uploaded audio to 16kHz mono WAV |
| `api/task_store.py` | Redis-backed mapping of `stt_id` (UUID) → Celery `task_id` (survives restarts) |
| `api/health.py` | `/health/`, `/health/ready/`, `/health/live/` logic |
| `api/cleanup_scheduler.py` | APScheduler cron job to delete old files from `recordings/` |
| `config.env` | Non-secret config committed to git (model names, Redis settings, cleanup schedule) |
| `.env.secrets` | HuggingFace token — gitignored, create from `.env.secrets.example` |

## ML Models

All models load at worker startup (`worker_process_init` signal → `SpeechToTextTask._ensure_models_loaded()`), shared as class-level attributes across all task instances in the same worker process.

- **Whisper** (`WHISPER_MODEL_NAME`): Welsh fine-tuned CTranslate2 model from Techiaith/DewiBrynJones
- **wav2vec2** (`WAV2VEC2_MODEL`): Welsh alignment model from Techiaith — used for forced alignment; alignment workers run on CPU to avoid CUDA OOM on long audio
- **pyannote diarization**: Speaker diarization pipeline (requires HF token for private model access)
- **Lingua**: Welsh/English language detector applied after Whisper transcription

Each GPU worker needs ~6GB VRAM. A 24GB GPU supports max 4 GPU workers total.

## Output Files

All files stored in `recordings/` (Docker volume), named by `stt_id`:
- `<stt_id>.wav` — converted audio (16kHz mono)
- `<stt_id>.json` — full result with segments, word timestamps, scores, normalized text
- `<stt_id>.srt` / `.vtt` — subtitle files
- `<stt_id>.eaf` — ELAN annotation file
- `<stt_id>.txt` — plain text
- `<stt_id>.speakers.json` — speaker diarization result
- `<stt_id>.log` — per-task log (readable via `/get_status/`)

## Welsh Normalizer

`worker/normalization/` normalizes verbatim Welsh speech to standard written Welsh. Each transcription segment gets both `text` (original) and `normalized` fields. Translation output bypasses normalization.

Can be used standalone:
```bash
python -m normalization.welsh_normalizer --text "bo' nw'n gwbod"
python -m normalization.welsh_normalizer --srt input.srt --output output.srt
```

## Environment Configuration

```bash
# config.env (committed)
WHISPER_MODEL_NAME=DewiBrynJones/whisper-large-v2-ft-btb-cv-cvad-ca-wlga-cy-ct2-2511
WHISPER_MODEL_LANGUAGE=cy
WAV2VEC2_MODEL=techiaith/wav2vec2-btb-cv-ft-cv-cy
CLEANUP_ENABLED=true
FILE_RETENTION_DAYS=14

# .env.secrets (gitignored)
HF_AUTH_TOKEN=your_token_here
```

After editing either file, run `make setup` to regenerate `.env`.
