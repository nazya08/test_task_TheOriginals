from celery import Celery
from src.main.config import settings


celery_app = Celery(
    main=settings.SERVER_NAME,
    broker=settings.BROKER_URL
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

celery_app.autodiscover_tasks(["src.main.utils"])
