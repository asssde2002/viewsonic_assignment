from celery import Celery
from kombu import Queue
from models import TaskStatus, TaskRecord
from database.utils import get_db
from datetime import datetime

celery_app = Celery("viewsonic")
celery_app.config_from_object("config.celeryconfig")
celery_app.conf.task_default_priority = 10
celery_app.conf.task_inherit_parent_priority = True

celery_app.conf.task_queues = [
    Queue("viewsonic_pq")
]

class BaseTask(celery_app.Task):
    def apply_async(self, *args, **kwargs):
        # Create task record in DB before task is dispatched
        task_id = self.id
        db = next(get_db())
        now = datetime.utcnow()
        task_record = TaskRecord(id=task_id, status=TaskStatus.PENDING, created_at=now, updated_at=now)
        db.add(task_record)
        db.commit()
        # task_id = task_record.id

        # Add task_id to kwargs and pass it to apply_async
        # kwargs['task_id'] = task_id
        return super().apply_async(*args, **kwargs)