"""
Celery queue inspection utilities for monitoring task processing.
"""

from celery import Celery


async def get_queue_status(celery: Celery) -> dict:
    """
    Inspect Celery queue status - shows active, scheduled, and reserved tasks.
    Useful for monitoring queue depth and worker utilization.

    Returns:
        dict: Queue status including worker info and active tasks
    """
    try:
        inspect = celery.control.inspect()

        # Get active tasks (currently being processed)
        active_tasks = inspect.active()

        # Get scheduled tasks (waiting for execution time)
        scheduled_tasks = inspect.scheduled()

        # Get reserved tasks (claimed by worker but not started yet)
        reserved_tasks = inspect.reserved()

        # Get worker stats
        stats = inspect.stats()

        # Process active tasks to extract useful info
        active_summary = []
        if active_tasks:
            for worker_name, tasks in active_tasks.items():
                for task in tasks:
                    active_summary.append({
                        'worker': worker_name,
                        'task_id': task.get('id'),
                        'task_name': task.get('name'),
                        'args': task.get('args', []),
                        'time_start': task.get('time_start')
                    })

        # Process reserved tasks (tasks in queue, claimed by worker)
        reserved_summary = []
        if reserved_tasks:
            for worker_name, tasks in reserved_tasks.items():
                for task in tasks:
                    reserved_summary.append({
                        'worker': worker_name,
                        'task_id': task.get('id'),
                        'task_name': task.get('name'),
                        'args': task.get('args', [])
                    })

        # Calculate totals
        total_active = len(active_summary)
        total_reserved = len(reserved_summary)
        total_scheduled = 0
        if scheduled_tasks:
            for worker_tasks in scheduled_tasks.values():
                total_scheduled += len(worker_tasks)

        # Worker information
        workers_info = []
        if stats:
            for worker_name, worker_stats in stats.items():
                workers_info.append({
                    'name': worker_name,
                    'pool': worker_stats.get('pool', {}).get('implementation'),
                    'max_concurrency': worker_stats.get('pool', {}).get('max-concurrency'),
                    'total_tasks_executed': worker_stats.get('total', {})
                })

        return {
            'version': 2,
            'success': True,
            'summary': {
                'active_tasks': total_active,
                'reserved_tasks': total_reserved,
                'scheduled_tasks': total_scheduled,
                'total_in_progress': total_active + total_reserved + total_scheduled,
                'workers_available': len(workers_info)
            },
            'workers': workers_info,
            'active_tasks': active_summary,
            'reserved_tasks': reserved_summary
        }

    except Exception as e:
        return {
            'version': 2,
            'success': False,
            'error': str(e),
            'message': 'Failed to inspect Celery queue. Ensure workers are running.'
        }
