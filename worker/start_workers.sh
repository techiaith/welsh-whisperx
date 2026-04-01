#!/bin/bash

# Queue assignment via environment variable WORKER_QUEUES
# Controls which queues this worker listens to.
#
# Examples:
#   WORKER_QUEUES=high_priority         → Only high-priority tasks
#   WORKER_QUEUES=default               → Only normal/low-priority tasks
#   WORKER_QUEUES=high_priority,default → Both queues (high_priority checked first)
#
# Default: high_priority,default (listens to both)
QUEUES="${WORKER_QUEUES:-high_priority,default}"

# Build a meaningful worker name: queue name + short container ID
# e.g. "worker_high_priority_a1b2c3d4" instead of "whisper_stt_worker_a1b2c3d4e5f6"
SHORT_HOST="$(echo "${HOSTNAME:-$(hostname)}" | cut -c1-8)"
QUEUE_LABEL="$(echo "${QUEUES}" | tr ',' '_')"
WORKER_NAME="worker_${QUEUE_LABEL}_${SHORT_HOST}"

echo "Starting worker '${WORKER_NAME}' listening on queues: ${QUEUES}"

# Use exec so celery replaces this shell process (becomes PID 1).
# This ensures SIGTERM from Docker or os.kill(1, SIGTERM) goes
# directly to Celery and triggers a clean shutdown + container restart.
MAX_TASKS="${WORKER_MAX_TASKS_PER_CHILD:-0}"

MAXTASKS_ARG=""
if [ "$MAX_TASKS" -gt 0 ] 2>/dev/null; then
  MAXTASKS_ARG="--max-tasks-per-child ${MAX_TASKS}"
  echo "Worker will recycle after ${MAX_TASKS} tasks"
else
  echo "Worker will not recycle (max-tasks-per-child disabled)"
fi

exec celery -A tasks worker \
  --pool prefork \
  --concurrency 1 \
  ${MAXTASKS_ARG} \
  --loglevel info \
  --queues "${QUEUES}" \
  -n "${WORKER_NAME}"
