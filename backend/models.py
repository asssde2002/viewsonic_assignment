from sqlmodel import SQLModel, Field, Column, DateTime, update
import uuid
from enum import Enum
from datetime import datetime
from database.utils import get_session, get_redis_client


class TaskStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    CANCELED = "canceled"
    COMPLETED = "completed"


class TaskRecord(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    status: str = Field(default=TaskStatus.PENDING, )
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True), nullable=False))
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True), nullable=False, onupdate=datetime.utcnow))

    @staticmethod
    def update_status(task_id, status):
        session = next(get_session())
        session.execute(update(TaskRecord).where(TaskRecord.id == task_id).values(status=status))
        session.commit()
        TaskRecord.delete_list_task_records()

    @staticmethod
    def get_cache_key():
        return "task-records"

    @staticmethod
    def get_list_task_records():
        cache_key = TaskRecord.get_cache_key()
        redis = next(get_redis_client())
        return redis.get(cache_key)
        
    @staticmethod
    def save_list_task_records(task_records, timeout=60):
        cache_key = TaskRecord.get_cache_key()
        redis = next(get_redis_client())
        redis.set(cache_key, task_records, timeout)

    @staticmethod
    def delete_list_task_records():
        cache_key = TaskRecord.get_cache_key()
        redis = next(get_redis_client())
        redis.delete(cache_key)

        