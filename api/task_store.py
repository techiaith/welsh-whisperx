import redis
import os
from typing import Optional

class TaskStore:
    """
    Redis-based task store for persisting task IDs and statuses.
    Survives server restarts and includes automatic TTL-based cleanup.
    """
    def __init__(self, redis_host: str, redis_port: str, ttl_days: int = 7):
        """
        Initialize Redis connection for task storage.

        Args:
            redis_host: Redis server host
            redis_port: Redis server port
            ttl_days: Number of days to keep task data (default: 7)
        """
        self.redis_client = redis.Redis(
            host=redis_host,
            port=int(redis_port),
            db=1,  # Use db=1 to separate from Celery's db=0
            decode_responses=True
        )
        self.ttl_seconds = ttl_days * 24 * 60 * 60
        self.key_prefix = "stt:task:"
        self.param_prefix = "stt:param:"

    def set_task_id(self, stt_id: str, task_id: str) -> None:
        """
        Store task_id for a given stt_id with automatic expiration.

        Args:
            stt_id: The STT job identifier
            task_id: The Celery task identifier
        """
        key = f"{self.key_prefix}{stt_id}"
        self.redis_client.set(key, task_id, ex=self.ttl_seconds)

    def get_task_id(self, stt_id: str) -> Optional[str]:
        """
        Retrieve task_id for a given stt_id.

        Args:
            stt_id: The STT job identifier

        Returns:
            The Celery task_id or None if not found
        """
        key = f"{self.key_prefix}{stt_id}"
        return self.redis_client.get(key)

    def delete_task(self, stt_id: str) -> bool:
        """
        Delete task_id for a given stt_id.

        Args:
            stt_id: The STT job identifier

        Returns:
            True if deleted, False if not found
        """
        key = f"{self.key_prefix}{stt_id}"
        return bool(self.redis_client.delete(key))

    def set_task_param(self, stt_id: str, task_param: str) -> None:
        """
        Store task parameter (transcribe/translate) for a given stt_id with automatic expiration.

        Args:
            stt_id: The STT job identifier
            task_param: The task parameter ('transcribe' or 'translate')
        """
        key = f"{self.param_prefix}{stt_id}"
        self.redis_client.set(key, task_param, ex=self.ttl_seconds)

    def get_task_param(self, stt_id: str) -> str:
        """
        Retrieve task parameter for a given stt_id.

        Args:
            stt_id: The STT job identifier

        Returns:
            The task parameter or 'transcribe' as default if not found
        """
        key = f"{self.param_prefix}{stt_id}"
        param = self.redis_client.get(key)
        return param if param else 'transcribe'

    def exists(self, stt_id: str) -> bool:
        """
        Check if task_id exists for given stt_id.

        Args:
            stt_id: The STT job identifier

        Returns:
            True if exists, False otherwise
        """
        key = f"{self.key_prefix}{stt_id}"
        return bool(self.redis_client.exists(key))

    def extend_ttl(self, stt_id: str) -> bool:
        """
        Extend the TTL for a task (useful for long-running jobs).

        Args:
            stt_id: The STT job identifier

        Returns:
            True if TTL was extended, False if key doesn't exist
        """
        key = f"{self.key_prefix}{stt_id}"
        return bool(self.redis_client.expire(key, self.ttl_seconds))

    def get_all_tasks(self) -> dict:
        """
        Get all active tasks (useful for debugging/monitoring).

        Returns:
            Dictionary mapping stt_id -> task_id
        """
        pattern = f"{self.key_prefix}*"
        tasks = {}
        for key in self.redis_client.scan_iter(match=pattern):
            stt_id = key.replace(self.key_prefix, "")
            task_id = self.redis_client.get(key)
            if task_id:
                tasks[stt_id] = task_id
        return tasks

    def cleanup_expired(self) -> int:
        """
        Manual cleanup of expired tasks (normally handled automatically by Redis).
        This is mainly for monitoring purposes.

        Returns:
            Number of tasks still active
        """
        return len(self.get_all_tasks())


# Create singleton instance
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')
task_store = TaskStore(REDIS_HOST, REDIS_PORT, ttl_days=7)
