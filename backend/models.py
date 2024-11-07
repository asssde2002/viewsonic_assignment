from sqlmodel import SQLModel, Field
import uuid


class TaskRecord(SQLModel, table=True):
    uuid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    status: str
    