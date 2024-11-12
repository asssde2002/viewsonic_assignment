import uuid
from fastapi import HTTPException, Depends
from fastapi_restful.cbv import cbv
from typing import List, Optional
from models import TaskRecord, TaskStatus
from tasks import do_something
from utils import revoke_task
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession


from fastapi import APIRouter
from database.utils import get_async_session
from decorators import RedisCachePollingAPI
from controllers import ListTaskRecordCacheController

task_router = APIRouter()


@cbv(task_router)
class TaskViewSet:
    session: AsyncSession = Depends(get_async_session)

    @task_router.get("/", response_model=List[TaskRecord])
    @RedisCachePollingAPI(controller_class=ListTaskRecordCacheController, timeout=60)
    async def get_tasks(self):
        taskrecords = await self.session.exec(select(TaskRecord).order_by(TaskRecord.created_at))
        taskrecords = taskrecords.all()
        return taskrecords

    @task_router.post("/", status_code=201)
    async def create_task(self, taskrecord: Optional[TaskRecord] = None):
        task_id = str(uuid.uuid4())
        await TaskRecord.create(task_id, self.session)
        do_something.apply_async(task_id=task_id)

    @task_router.delete("/{task_id}", status_code=204)
    async def delete_task(self, task_id: uuid.UUID):
        taskrecord = await self.session.exec(select(TaskRecord).where(TaskRecord.id == task_id))
        taskrecord = taskrecord.first()
        if taskrecord is None:
            raise HTTPException(status_code=404, detail=f"Task ({taskrecord.id}) is not found")
        elif taskrecord.status in [TaskStatus.COMPLETED, TaskStatus.CANCELED]:
            raise HTTPException(status_code=400, detail=f"Task ({taskrecord.id}) cannot be canceled")
        
        revoke_task(str(task_id))
        await TaskRecord.async_update_status(str(task_id), TaskStatus.CANCELED, self.session)

