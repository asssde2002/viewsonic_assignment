from sqlmodel import SQLModel, Field


class TaskRecord(SQLModel, table=True):
    id: int = Field(primary_key=True)
    status: str
    