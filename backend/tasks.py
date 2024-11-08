from celery_app import celery_app
import time
from sqlmodel import update
from models import TaskRecord, TaskStatus
from database.utils import get_db


@celery_app.task(queue="viewsonic_pq")
def do_something(x=3):
    task_id = do_something.request.id
    session = get_db()
    session.execute(update(TaskRecord).where(TaskRecord.id == task_id).values(status=TaskStatus.PROCESSING))
    session.commit()
    print(f"Task ID: {task_id}")
    time.sleep(x)

