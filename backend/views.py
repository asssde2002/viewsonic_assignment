import uuid
from fastapi import HTTPException, Depends
from fastapi_restful.cbv import cbv
from typing import List, Optional
from models import TaskRecord, TaskStatus
from tasks import sleep
from utils import revoke_task
from sqlmodel import Session, select

from fastapi_restful.inferring_router import InferringRouter
from database.utils import get_db
from datetime import datetime

task_router = InferringRouter()


@cbv(task_router)
class TaskViewSet:
    session: Session = Depends(get_db)

    @task_router.get("/", response_model=List[TaskRecord])
    def get_tasks(self):
        taskrecords = self.session.execute(select(TaskRecord)).scalars().all()
        return taskrecords

    @task_router.post("/", status_code=201, response_model=TaskRecord)
    def create_task(self, taskrecord: Optional[TaskRecord] = None):
        task = sleep.delay()
        now = datetime.utcnow()
        taskrecord = TaskRecord(id=task.id, created_at=now, updated_at=now)
        self.session.add(taskrecord)
        self.session.commit()
        self.session.refresh(taskrecord)
        return taskrecord

    @task_router.delete("/{task_id}", status_code=204)
    def delete_task(self, task_id: uuid.UUID):
        taskrecord = self.session.execute(select(TaskRecord).where(TaskRecord.id == task_id)).scalars().first()
        if taskrecord is None:
            raise HTTPException(status_code=404, detail=f"Task ({taskrecord.id}) is not found")
        elif taskrecord.status in [TaskStatus.COMPLETED, TaskStatus.CANCELED]:
            raise HTTPException(status_code=400, detail=f"Task ({taskrecord.id}) cannot be canceled")
        
        revoke_task(taskrecord.id)
        taskrecord.status = TaskStatus.CANCELED
        self.session.commit()
