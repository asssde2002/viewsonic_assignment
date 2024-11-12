import time

from celery_app import celery_app
from decorators import update_task_record


@celery_app.task(queue="viewsonic_pq")
@update_task_record
def do_something(x=3):
    time.sleep(x)
