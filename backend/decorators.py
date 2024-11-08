from celery import current_task
from models import TaskRecord, TaskStatus
from functools import wraps


def update_task_record(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        task_id = current_task.request.id
        TaskRecord.update_status(task_id, TaskStatus.PROCESSING)
        result = func(*args, **kwargs)
        TaskRecord.update_status(task_id, TaskStatus.COMPLETED)
        return result
    
    return wrapper
