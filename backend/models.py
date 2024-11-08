from sqlmodel import SQLModel, Field, Column, DateTime, update
import uuid
from enum import Enum
from datetime import datetime
from database.utils import get_db


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
        session = next(get_db())
        session.execute(update(TaskRecord).where(TaskRecord.id == task_id).values(status=status))
        session.commit()
