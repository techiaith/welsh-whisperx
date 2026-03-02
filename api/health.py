"""
Health check endpoints for monitoring service availability and dependencies.
"""

from celery import Celery
from task_store import task_store


async def get_comprehensive_health(celery: Celery) -> dict:
    """
    Comprehensive health check including Redis and Celery workers.
    Returns overall system health status.
    """
    health_status = {
        'status': 'healthy',
        'version': 2,
        'checks': {}
    }

    # Check Redis connectivity
    try:
        task_store.redis_client.ping()
        health_status['checks']['redis'] = 'healthy'
    except Exception as e:
        health_status['checks']['redis'] = f'unhealthy: {str(e)}'
        health_status['status'] = 'degraded'

    # Check Celery workers
    try:
        inspect = celery.control.inspect()
        active_workers = inspect.active()

        if active_workers is None:
            worker_count = 0
            health_status['checks']['workers'] = 'no workers available'
            health_status['status'] = 'degraded'
        else:
            worker_count = len(active_workers)
            health_status['checks']['workers'] = f'{worker_count} worker(s) available'

            if worker_count == 0:
                health_status['status'] = 'degraded'
    except Exception as e:
        health_status['checks']['workers'] = f'error: {str(e)}'
        health_status['status'] = 'degraded'

    # Check model readiness (workers set worker:ready:<hostname> after loading models)
    try:
        ready_keys = list(task_store.redis_client.scan_iter(match='worker:ready:*'))
        ready_count = len(ready_keys)
        health_status['checks']['models'] = f'{ready_count} worker(s) with models loaded'

        if ready_count == 0:
            health_status['status'] = 'degraded'
    except Exception as e:
        health_status['checks']['models'] = f'error: {str(e)}'

    return health_status


async def check_readiness() -> dict:
    """
    Readiness probe - checks if service is ready to accept traffic.
    Returns ready status or raises exception if Redis is unavailable.
    """
    # Check if Redis is accessible
    task_store.redis_client.ping()
    return {'ready': True, 'version': 2}


async def check_liveness() -> dict:
    """
    Liveness probe - checks if API process is alive and responding.
    Always returns success if called (process is running).
    """
    return {'alive': True, 'version': 2}
