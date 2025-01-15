import time

from celery import Celery

from config import settings
from dependencies import postgres_connection
from src.application.dto import TastStatus

celery_app = Celery("tasks", broker=settings.CELERY_BROKER)


@celery_app.task(name="process_task", ignore_result=True)
def process_task(task_id: int):
    conn = postgres_connection
    conn.autocommit = True
    time.sleep(10)

    with conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE tasks SET status = %s WHERE id = %s;",
                (TastStatus.DONE.value, task_id),
            )
