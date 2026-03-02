"""
Scheduled cleanup of old transcription files.
Automatically deletes files older than a configurable retention period.
"""
import os
import glob
import asyncio
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Tuple

import aiofiles.os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

# Add shared directory to path for logger
import sys
sys.path.append('/app/shared')
from stt_logger import get_logger

# Configuration from environment variables
UPLOAD_DIR = os.environ.get('RECORDINGS_DIR', '/recordings')
RETENTION_DAYS = int(os.environ.get('FILE_RETENTION_DAYS', '14'))  # Default: 2 weeks
CLEANUP_ENABLED = os.environ.get('CLEANUP_ENABLED', 'true').lower() == 'true'
CLEANUP_SCHEDULE = os.environ.get('CLEANUP_SCHEDULE', '0 2 * * *')  # Default: 2 AM daily

logger = get_logger('cleanup')


async def cleanup_old_files() -> Tuple[int, int, List[str]]:
    """
    Delete files older than RETENTION_DAYS from the recordings directory.

    Returns:
        Tuple of (files_deleted, bytes_freed, errors)
    """
    logger.info(f"Starting cleanup task - retention period: {RETENTION_DAYS} days")

    cutoff_time = datetime.now() - timedelta(days=RETENTION_DAYS)
    cutoff_timestamp = cutoff_time.timestamp()

    files_deleted = 0
    bytes_freed = 0
    errors = []

    try:
        # Get all files in the recordings directory
        pattern = os.path.join(UPLOAD_DIR, '*')
        all_files = glob.glob(pattern)

        logger.info(f"Found {len(all_files)} total files in {UPLOAD_DIR}")

        for file_path in all_files:
            try:
                # Skip if not a file (e.g., subdirectory)
                if not os.path.isfile(file_path):
                    continue

                # Get file modification time
                file_stat = await aiofiles.os.stat(file_path)
                file_mtime = file_stat.st_mtime

                # Check if file is older than retention period
                if file_mtime < cutoff_timestamp:
                    file_size = file_stat.st_size
                    file_age_days = (datetime.now().timestamp() - file_mtime) / (24 * 3600)

                    logger.info(
                        f"Deleting old file: {os.path.basename(file_path)} "
                        f"(age: {file_age_days:.1f} days, size: {file_size} bytes)"
                    )

                    await aiofiles.os.remove(file_path)
                    files_deleted += 1
                    bytes_freed += file_size

            except Exception as e:
                error_msg = f"Error deleting {file_path}: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)

        # Log summary
        mb_freed = bytes_freed / (1024 * 1024)
        logger.info(
            f"Cleanup completed: {files_deleted} files deleted, "
            f"{mb_freed:.2f} MB freed"
        )

        if errors:
            logger.warning(f"Cleanup had {len(errors)} errors")

    except Exception as e:
        error_msg = f"Fatal error during cleanup: {str(e)}"
        logger.error(error_msg)
        errors.append(error_msg)

    return files_deleted, bytes_freed, errors


def start_cleanup_scheduler(app) -> AsyncIOScheduler:
    """
    Start the background scheduler for file cleanup.

    Args:
        app: FastAPI application instance (for lifespan management)

    Returns:
        AsyncIOScheduler instance
    """
    if not CLEANUP_ENABLED:
        logger.info("Cleanup scheduler is disabled (CLEANUP_ENABLED=false)")
        return None

    logger.info(f"Initializing cleanup scheduler with schedule: {CLEANUP_SCHEDULE}")
    logger.info(f"Retention period: {RETENTION_DAYS} days")
    logger.info(f"Target directory: {UPLOAD_DIR}")

    scheduler = AsyncIOScheduler()

    # Parse cron schedule (format: minute hour day month day_of_week)
    # Default "0 2 * * *" means 2:00 AM every day
    try:
        scheduler.add_job(
            cleanup_old_files,
            trigger=CronTrigger.from_crontab(CLEANUP_SCHEDULE),
            id='cleanup_old_files',
            name='Delete old transcription files',
            replace_existing=True,
            max_instances=1,  # Prevent overlapping cleanup runs
        )

        scheduler.start()
        logger.info(f"Cleanup scheduler started successfully")

        # Log next scheduled run
        next_run = scheduler.get_job('cleanup_old_files').next_run_time
        logger.info(f"Next cleanup scheduled for: {next_run}")

    except Exception as e:
        logger.error(f"Failed to start cleanup scheduler: {str(e)}")
        raise

    return scheduler


def stop_cleanup_scheduler(scheduler: AsyncIOScheduler):
    """Stop the cleanup scheduler gracefully."""
    if scheduler:
        logger.info("Stopping cleanup scheduler")
        scheduler.shutdown(wait=True)
        logger.info("Cleanup scheduler stopped")


async def run_cleanup_now() -> dict:
    """
    Manually trigger cleanup (useful for testing or API endpoint).

    Returns:
        Dictionary with cleanup results
    """
    logger.info("Manual cleanup triggered")
    files_deleted, bytes_freed, errors = await cleanup_old_files()

    return {
        'success': len(errors) == 0,
        'files_deleted': files_deleted,
        'bytes_freed': bytes_freed,
        'mb_freed': round(bytes_freed / (1024 * 1024), 2),
        'errors': errors,
        'retention_days': RETENTION_DAYS,
        'timestamp': datetime.now().isoformat()
    }
