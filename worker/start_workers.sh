#!/bin/bash

# Generate unique worker name using hostname for scalability
WORKER_NAME="whisper_stt_worker_${HOSTNAME:-$(hostname)}"

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

echo "Starting worker '${WORKER_NAME}' listening on queues: ${QUEUES}"

celery -A tasks worker \
  --pool prefork \
  --concurrency 1 \
  --max-tasks-per-child 10 \
  --loglevel info \
  --queues "${QUEUES}" \
  -n "${WORKER_NAME}"
