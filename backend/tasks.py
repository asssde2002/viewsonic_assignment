from celery_app import celery_app
import time


@celery_app.task(queue="viewsonic_pq")
def sleep(x=3):
    time.sleep(x)

