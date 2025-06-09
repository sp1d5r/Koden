from celery import Celery
from app.core.config import settings
from app.core.logging import logger

celery_app = Celery(
    "koden",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks.github"]
)

# Optional configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,  # Track when tasks are started
    task_time_limit=3600,    # 1 hour timeout
    worker_prefetch_multiplier=1,  # Process one task at a time
    task_acks_late=True,     # Only acknowledge task after it's completed
    task_reject_on_worker_lost=True,  # Requeue task if worker dies
    task_default_queue='default',  # Explicitly set default queue
    task_queues={
        'default': {
            'exchange': 'default',
            'routing_key': 'default',
        },
    },
    task_routes={
        'download_github_repo': {
            'queue': 'default',
            'routing_key': 'default',
        },
    },
    worker_send_task_events=True,
    task_send_sent_event=True,
)

# Make sure tasks are registered
celery_app.autodiscover_tasks(['app.tasks'])

# Log registered tasks
logger.info(f"Registered tasks: {celery_app.tasks.keys()}") 