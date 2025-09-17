from celery import Celery

celery_app = Celery(
    "sendport",

    broker="redis://localhost:6379/0",          #Redis broker
    backend="redis://localhost:6379/0"          #Redis backend (for results)
)

celery_app.conf.update(
    task_routes={
        "app.tasks.*": {"queue": "emails"},
    },
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)