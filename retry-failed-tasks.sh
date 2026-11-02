#!/bin/bash
# Finds long-form transcription/translation jobs in recordings/ whose worker log
# records a recoverable failure (GPU out of memory, or a worker that died
# mid-task) and re-queues them reusing their original stt_id — so /get_status/,
# /get_json/, /get_srt/ etc. keep working for clients that still hold the id.
#
# A job is retryable when the failure is the LAST line of its .log, its .wav is
# still present, and no .json result exists. Testing the last line rather than
# the whole file is what stops an already-requeued job being sent twice: once it
# is running again, progress lines sit after the old failure.
#
# Only long-form jobs write a .log, so short-form (/transcribe/, /keyboard/)
# requests never appear here.
# Alignment jobs are skipped: re-running them needs the caller's text, which
# isn't stored.
#
# Usage:
#   ./retry-failed-tasks.sh                 # dry run (default)
#   ./retry-failed-tasks.sh --requeue       # actually re-queue
#   ./retry-failed-tasks.sh --since 30      # look back 30 days (default 7)
#   ./retry-failed-tasks.sh --since 0       # scan every log (slow: ~20k files)
#   ./retry-failed-tasks.sh --priority 5    # normal priority (default 9 = low)
#   ./retry-failed-tasks.sh --pattern 'ffmpeg conversion failed'
#
# Default priority is 9 (low) so live user requests, which arrive at priority 5,
# are still served first — a backlog fills idle GPU time instead of competing
# with it.
#
# Default lookback is 7 days to match the task_store TTL, and because scanning
# the whole of recordings/ takes minutes.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
DIR="$ROOT/recordings"
DEVICE="$(cat "$ROOT/.device" 2>/dev/null || echo gpu)"
DOCKER_COMPOSE="docker compose -f $ROOT/docker-compose.${DEVICE}.yml --env-file $ROOT/.env --project-name whisperx-server"

REQUEUE=false
SINCE=7
PRIORITY=9
# Failures worth retrying: the task died for reasons unrelated to the audio
# itself, so the same input can succeed on a healthier GPU.
PATTERN='CUDA failed with error out of memory|CUDA out of memory|is no longer responding'

while [[ $# -gt 0 ]]; do
    case "$1" in
        --requeue)  REQUEUE=true; shift ;;
        --since)    SINCE="$2"; shift 2 ;;
        --priority) PRIORITY="$2"; shift 2 ;;
        --pattern)  PATTERN="$2"; shift 2 ;;
        --dry-run)  REQUEUE=false; shift ;;
        -h|--help)  sed -n '2,26p' "$0" | sed 's/^# \?//'; exit 0 ;;
        *)          echo "ERROR: unknown argument: $1" >&2; exit 1 ;;
    esac
done

if [[ ! -d "$DIR" ]]; then
    echo "ERROR: recordings directory not found: $DIR" >&2
    exit 1
fi

echo "Scanning:  $DIR"
echo "  pattern: $PATTERN"
if [[ "$SINCE" == "0" ]]; then
    echo "  window:  all logs"
    FIND_ARGS=()
else
    echo "  window:  last $SINCE day(s)"
    FIND_ARGS=(-mtime "-$SINCE")
fi
echo ""

# JOBS holds "<stt_id>:<mode>" pairs; the mode comes from the worker's own log
# line so a failed translation is re-queued as a translation.
JOBS=()
skipped_done=0
skipped_nowav=0
skipped_align=0
skipped_active=0

while IFS= read -r log_file; do
    stt_id="$(basename "$log_file" .log)"

    if grep -q 'Alignment task received' "$log_file"; then
        skipped_align=$((skipped_align + 1))
        continue
    fi
    if [[ -f "$DIR/$stt_id.json" ]]; then
        skipped_done=$((skipped_done + 1))
        continue
    fi
    if [[ ! -f "$DIR/$stt_id.wav" ]]; then
        skipped_nowav=$((skipped_nowav + 1))
        continue
    fi
    # Anything logged after the failure means the job has already been picked up
    # again — queued, running, or retried by hand.
    if ! tail -n 1 "$log_file" | grep -qE "$PATTERN"; then
        skipped_active=$((skipped_active + 1))
        continue
    fi

    mode="$(grep -o 'task mode: [a-z]*' "$log_file" | tail -1 | awk '{print $3}')"
    JOBS+=("$stt_id:${mode:-transcribe}")
done < <(find "$DIR" -maxdepth 1 -name '*.log' "${FIND_ARGS[@]}" -print0 \
         | xargs -0 --no-run-if-empty grep -lE "$PATTERN" \
         | sort)

echo "Retryable:      ${#JOBS[@]}"
echo "  skipped (already has .json): $skipped_done"
echo "  skipped (wav deleted):       $skipped_nowav"
echo "  skipped (alignment job):     $skipped_align"
echo "  skipped (already re-queued): $skipped_active"
echo ""

if [[ ${#JOBS[@]} -eq 0 ]]; then
    echo "Nothing to do."
    exit 0
fi

# Smallest first, so quick wins land before multi-hour files.
SORTED=()
while IFS= read -r line; do
    SORTED+=("${line#* }")
done < <(for job in "${JOBS[@]}"; do
             echo "$(stat -c%s "$DIR/${job%%:*}.wav") $job"
         done | sort -n)

if ! $REQUEUE; then
    total=0
    for job in "${SORTED[@]}"; do
        size=$(stat -c%s "$DIR/${job%%:*}.wav")
        total=$((total + size))
        printf 'WOULD %s (%s) %.1f MB\n' "${job%%:*}" "${job##*:}" "$(echo "$size" | awk '{print $1/1000000}')"
    done
    echo ""
    # 16kHz mono pcm_s16le = 32000 bytes per second of audio.
    echo "$total" | awk -v n="${#SORTED[@]}" '{
        seconds = $1 / 32000
        if (seconds < 3600) duration = sprintf("%.0f minutes", seconds / 60)
        else                duration = sprintf("%.1f hours", seconds / 3600)
        printf "Would re-queue %d job(s), %.1f MB of 16kHz mono WAV (~%s of audio).\n", n, $1/1000000, duration
    }'
    echo "Run with --requeue to proceed."
    exit 0
fi

CONTAINER="$($DOCKER_COMPOSE ps -q application)"
if [[ -z "$CONTAINER" ]]; then
    echo "ERROR: the 'application' container is not running — start it with 'make up-${DEVICE}'" >&2
    exit 1
fi

docker cp "$ROOT/retry-failed-tasks.py" "$CONTAINER:/tmp/retry-failed-tasks.py"
docker exec "$CONTAINER" python /tmp/retry-failed-tasks.py "$PRIORITY" "${SORTED[@]}"

echo ""
echo "Track progress with:  curl -s 'http://localhost:5511/get_status/?stt_id=<stt_id>'"
