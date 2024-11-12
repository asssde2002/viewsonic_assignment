import pickle
from models import TaskRecord

class BasePollingAPICacheController:
    def __init__(self, timeout=60):
        self.timeout = timeout

    def judge_to_use_cache(self):
        raise NotImplementedError

    async def get_cache(self):
        raise NotImplementedError

    async def save_cache(self, payload):
        raise NotImplementedError


class ListTaskRecordCacheController(BasePollingAPICacheController):
    def judge_to_use_cache(self):
        return True

    async def get_cache(self):
        payload = None
        cached_task_records = await TaskRecord.async_get_list_task_records()
        if cached_task_records:
            payload = pickle.loads(cached_task_records)

        return payload

    async def save_cache(self, payload):
        cached_task_records = pickle.dumps(payload)
        await TaskRecord.async_save_list_task_records(cached_task_records, self.timeout)
