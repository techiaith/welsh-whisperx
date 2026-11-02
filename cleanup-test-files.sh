#!/bin/bash
# Finds UUID files in recordings/ that are copies of speech.wav (by md5 checksum)
# and deletes them along with all associated output files (.wav, .json, .txt, .log, etc.)
#
# Usage:
#   ./cleanup-test-files.sh          # dry run (default)
#   ./cleanup-test-files.sh --delete # actually delete

set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)/recordings"
REFERENCE="$(cd "$(dirname "$0")" && pwd)/speech.wav"
DELETE=false

if [[ "${1:-}" == "--delete" ]]; then
    DELETE=true
fi

if [[ ! -f "$REFERENCE" ]]; then
    echo "ERROR: Reference file not found: $REFERENCE"
    exit 1
fi

REF_SIZE=$(stat -c%s "$REFERENCE")
REF_MD5=$(md5sum "$REFERENCE" | awk '{print $1}')

echo "Reference: $REFERENCE"
echo "  Size: $REF_SIZE bytes"
echo "  MD5:  $REF_MD5"
echo ""

# Find .wav files matching the reference size, then verify by checksum
UUIDS=()
while IFS= read -r wav_file; do
    file_md5=$(md5sum "$wav_file" | awk '{print $1}')
    if [[ "$file_md5" == "$REF_MD5" ]]; then
        uuid=$(basename "$wav_file" .wav)
        UUIDS+=("$uuid")
    fi
done < <(find "$DIR" -maxdepth 1 -size "${REF_SIZE}c" -name "*.wav")

echo "Found ${#UUIDS[@]} matching UUIDs"
echo ""

if [[ ${#UUIDS[@]} -eq 0 ]]; then
    echo "Nothing to do."
    exit 0
fi

total_files=0
for uuid in "${UUIDS[@]}"; do
    files=("$DIR/$uuid"*)
    count=${#files[@]}
    total_files=$((total_files + count))

    if $DELETE; then
        rm -f "${files[@]}"
        echo "Deleted $count files for $uuid"
    else
        echo "[$uuid] $count files"
    fi
done

echo ""
if $DELETE; then
    echo "Deleted $total_files files across ${#UUIDS[@]} UUIDs."
else
    echo "Would delete $total_files files across ${#UUIDS[@]} UUIDs."
    echo "Run with --delete to proceed."
fi
