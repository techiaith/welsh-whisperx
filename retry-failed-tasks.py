"""Ail-anfon tasgau speech_to_text sydd wedi methu, gan ail-ddefnyddio'r stt_id gwreiddiol.
Re-dispatch failed speech_to_text tasks, reusing the original stt_id.

Rhedeg tu mewn i'r cynhwysydd `application` — mae'n rhannu'r un cyfluniad
Celery/Redis â'r API. Fe'i gelwir gan retry-failed-tasks.sh; nid yw wedi'i
fwriadu i'w redeg â llaw.

Runs inside the `application` container, which shares the API's Celery/Redis
config. Invoked by retry-failed-tasks.sh; not intended to be run by hand.

Usage: python retry-failed-tasks.py <priority> <stt_id>:<mode> [<stt_id>:<mode> ...]

Repointing the Redis stt_id -> task_id mapping is what makes the original id
keep working with /get_status/, /get_json/, /get_srt/ etc.
"""
import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, '/api')

from celery import Celery
from task_store import task_store

UPLOAD_DIR = os.environ.get('UPLOAD_DIR', '/recordings')
REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')
CONN_URI = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

# Matches api/main.py — priorities only work when the client declares the same
# max priority as the workers.
celery = Celery('tasks', broker=CONN_URI, backend=CONN_URI)
celery.conf.update(
    task_queue_max_priority=10,
    task_default_priority=5,
)

if len(sys.argv) < 3:
    print("Usage: python retry-failed-tasks.py <priority> <stt_id>:<mode> ...", file=sys.stderr)
    sys.exit(2)

priority = int(sys.argv[1])
jobs = [arg.split(':', 1) for arg in sys.argv[2:]]

sent = skipped = 0
for stt_id, mode in jobs:
    wav = Path(UPLOAD_DIR) / f"{stt_id}.wav"
    result_json = Path(UPLOAD_DIR) / f"{stt_id}.json"

    # Re-checked here as well as in the shell script: a job may have completed
    # in the gap between discovery and dispatch.
    if not wav.is_file():
        print(f"SKIP  {stt_id}  (no wav)")
        skipped += 1
        continue
    if result_json.is_file():
        print(f"SKIP  {stt_id}  (json already exists)")
        skipped += 1
        continue

    # Long-form endpoints dispatch to 'default'; the wav is passed directly
    # because the original upload is deleted once it has been converted.
    task = celery.send_task(
        'speech_to_text',
        args=(wav.as_posix(), mode),
        queue='default',
        priority=priority,
    )
    task_store.set_task_id(stt_id, task.task_id)
    task_store.set_task_param(stt_id, mode)

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]
    with open(Path(UPLOAD_DIR) / f"{stt_id}.log", 'a', encoding='utf-8') as log_file:
        log_file.write(f"{timestamp} - INFO - [RETRY] Re-queued after failure, mode: {mode}, "
                       f"queue 'default' priority {priority}, task_id: {task.task_id}\n")

    print(f"SENT  {stt_id}  ({mode}) -> {task.task_id}")
    sent += 1

print(f"\nRequeued: {sent}, skipped: {skipped}")
