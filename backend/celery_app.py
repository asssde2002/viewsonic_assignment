from celery import Celery

app = Celery("viewsonic")
app.config_from_object("config.celeryconfig")
app.conf.task_default_priority = 10
app.conf.task_inherit_parent_priority = True