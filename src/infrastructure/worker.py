from celery_app import process_task
from src.application.interfaces import TasksWorker


class CeleryTasksWorker(TasksWorker):
    def add(self, task_id: int):
        process_task.delay(task_id)
