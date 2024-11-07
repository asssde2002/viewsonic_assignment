from sqlmodel import SQLModel, Field

class Task(SQLModel, table=True):
    id: int = Field(primary_key=True)
    status: str
    