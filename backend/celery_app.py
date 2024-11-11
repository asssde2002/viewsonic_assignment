from celery import Celery
from kombu import Queue
from models import TaskStatus, TaskRecord
from database.utils import get_session
from datetime import datetime, timezone

celery_app = Celery("viewsonic")
celery_app.config_from_object("config.celeryconfig")
celery_app.conf.task_default_priority = 10
celery_app.conf.task_inherit_parent_priority = True

celery_app.conf.task_queues = [
    Queue("viewsonic_pq")
]

class BaseTask(celery_app.Task):
    def apply_async(self, *args, **kwargs):
        result = super().apply_async(*args, **kwargs)
        task_id = result.id
        now = datetime.now(timezone.utc)
        task_record = TaskRecord(id=task_id, status=TaskStatus.PENDING, created_at=now, updated_at=now)
        with get_session() as session:
            session.add(task_record)
            session.commit()
        TaskRecord.delete_list_task_records()
        return result