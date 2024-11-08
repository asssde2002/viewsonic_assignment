from sqlmodel import SQLModel, Field
import uuid
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    CANCELED = "canceled"
    COMPLETED = "completed"

class TaskRecord(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    status: str = Field(default=TaskStatus.PENDING)
    