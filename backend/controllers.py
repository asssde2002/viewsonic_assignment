import pickle
from models import TaskRecord

class BasePollingAPICacheController:
    def __init__(self, timeout=60):
        self.timeout = timeout

    def judge_to_use_cache(self):
        raise NotImplementedError

    def get_cache(self):
        raise NotImplementedError

    def save_cache(self, payload):
        raise NotImplementedError
    

class ListTaskRecordCacheController(BasePollingAPICacheController):
    def judge_to_use_cache(self):
        return True

    def get_cache(self):
        payload = None
        cached_task_records = TaskRecord.get_list_task_records()
        if cached_task_records:
            payload = pickle.loads(cached_task_records)

        return payload

    def save_cache(self, payload):
        cached_task_records = pickle.dumps(payload)
        TaskRecord.save_list_task_records(cached_task_records, self.timeout)
