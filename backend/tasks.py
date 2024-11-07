from celery_app import celery_app
import time

@celery_app.task
def sleep(x=3):
    time.sleep(x)

