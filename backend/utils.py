from celery_app import celery_app


def revoke_task(task_id):
    celery_app.control.revoke(task_id, terminate=True)
