from celery import Celery
from kombu import Queue

celery_app = Celery("viewsonic")
celery_app.config_from_object("config.celeryconfig")
celery_app.conf.task_default_priority = 10
celery_app.conf.task_inherit_parent_priority = True

celery_app.conf.task_queues = [
    Queue("viewsonic_pq")
]
