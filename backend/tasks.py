from celery_app import celery_app, BaseTask
import time
from decorators import update_task_record


@celery_app.task(queue="viewsonic_pq", base=BaseTask)
@update_task_record
def do_something(x=3):
    time.sleep(x)
