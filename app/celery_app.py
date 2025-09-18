from .config import settings
from celery import Celery

broker = settings.get_redis_url()
backend = settings.get_redis_url()

celery_app = Celery(
    "sendport",
    broker = broker,          #Redis broker
    backend = backend          #Redis backend (for results)
)

celery_app.conf.update(
    task_routes={"app.tasks.*": {"queue": "emails"},},
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)