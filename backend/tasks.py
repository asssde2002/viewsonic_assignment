from celery_app import celery_app, BaseTask
import time
from sqlmodel import update
from models import TaskRecord, TaskStatus
from database.utils import get_db


@celery_app.task(queue="viewsonic_pq", base=BaseTask)
def do_something(x=3):
    task_id = do_something.request.id
    session = next(get_db())
    session.execute(update(TaskRecord).where(TaskRecord.id == task_id).values(status=TaskStatus.PROCESSING))
    session.commit()
    time.sleep(x)

