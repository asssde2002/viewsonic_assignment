from celery import current_task
from models import TaskRecord, TaskStatus
from controllers import BasePollingAPICacheController
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


class RedisCachePollingAPI:
    def __init__(self, controller_class, timeout=60):
        self.controller_class = controller_class
        self.timeout = timeout
        if not issubclass(self.controller_class, BasePollingAPICacheController):
            raise Exception("Not the subclass of BasePollingAPICacheController")

    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            controller = self.controller_class(self.timeout)
            use_cache = controller.judge_to_use_cache()
            payload = await controller.get_cache() if use_cache else None
            if payload is None:
                payload = await func(*args, **kwargs)
                if use_cache:
                    await controller.save_cache(payload)

            return payload

        return wrapper