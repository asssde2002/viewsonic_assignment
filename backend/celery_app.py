from celery import Celery

celery_app = Celery("viewsonic")
celery_app.config_from_object("config.celeryconfig")
celery_app.conf.task_default_priority = 10
celery_app.conf.task_inherit_parent_priority = True