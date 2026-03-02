import re
from fastapi import HTTPException

# UUID v4 pattern
UUID_PATTERN = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$', re.IGNORECASE)

def validate_stt_id(stt_id: str) -> str:
    """
    Validate that stt_id is a valid UUID to prevent path injection attacks.

    Args:
        stt_id: The STT identifier to validate

    Returns:
        The validated stt_id

    Raises:
        HTTPException: If stt_id is not a valid UUID
    """
    if not stt_id:
        raise HTTPException(status_code=400, detail="stt_id is required")

    # Check for path traversal attempts
    if '/' in stt_id or '\\' in stt_id or '..' in stt_id:
        raise HTTPException(status_code=400, detail="Invalid stt_id format")

    # Check for wildcard patterns
    if '*' in stt_id or '?' in stt_id:
        raise HTTPException(status_code=400, detail="Wildcard patterns not allowed in stt_id")

    # Validate UUID format
    if not UUID_PATTERN.match(stt_id):
        raise HTTPException(status_code=400, detail="stt_id must be a valid UUID")

    return stt_id
