from sqlmodel import SQLModel, Field, Column, DateTime, update, Session
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from enum import Enum
from datetime import datetime, timezone
from database.utils import async_engine, sync_engine, get_redis_client


class TaskStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    CANCELED = "canceled"
    COMPLETED = "completed"


class TaskRecord(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    status: str = Field(default=TaskStatus.PENDING, )
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), nullable=False))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), nullable=False, onupdate=lambda: datetime.now(timezone.utc)))

    @staticmethod
    async def create(task_id: str, session):
        now = datetime.now(timezone.utc)
        task_record = TaskRecord(id=task_id, status=TaskStatus.PENDING, created_at=now, updated_at=now)
        session.add(task_record)
        await session.commit()
        await TaskRecord.async_delete_list_task_records()

    @staticmethod
    def update_status(task_id: str, status: str):
        with Session(sync_engine) as session:
            session.execute(update(TaskRecord).where(TaskRecord.id == task_id).values(status=status))
            session.commit()
        TaskRecord.delete_list_task_records()

    @staticmethod
    async def async_update_status(task_id: str, status: str, session):
        await session.execute(update(TaskRecord).where(TaskRecord.id == task_id).values(status=status))
        await session.commit()
        await TaskRecord.async_delete_list_task_records()

    @staticmethod
    def get_cache_key():
        return "task-records"

    @staticmethod
    async def async_get_list_task_records():
        cache_key = TaskRecord.get_cache_key()
        async with get_redis_client() as redis_client:
            return await redis_client.get(cache_key)

    @staticmethod
    async def async_save_list_task_records(task_records, timeout=60):
        cache_key = TaskRecord.get_cache_key()
        async with get_redis_client() as redis_client:
            await redis_client.set(cache_key, task_records, timeout)

    @staticmethod
    async def async_delete_list_task_records():
        cache_key = TaskRecord.get_cache_key()
        async with get_redis_client() as redis_client:
            await redis_client.delete(cache_key)

    @staticmethod
    def delete_list_task_records():
        cache_key = TaskRecord.get_cache_key()
        with get_redis_client(async_mode=False) as redis_client:
            redis_client.delete(cache_key)

