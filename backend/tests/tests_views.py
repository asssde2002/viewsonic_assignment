import uuid
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import pytest
from sqlmodel import select

from models import TaskRecord, TaskStatus

TEST_CACHE_LOCATION = "redis://redis:6379/2"


def mock_judge_to_use_cache(*args, **kwargs):
    return False


@pytest.mark.asyncio
@patch("tasks.time.sleep")
async def test_create_task(mock_sleep, async_client, test_session):
    response = await async_client.post("/tasks/")
    assert response.status_code == 201

    tasks = await test_session.exec(select(TaskRecord))
    tasks = tasks.all()
    assert len(tasks) == 1
    assert tasks[0].status == TaskStatus.PENDING
    assert mock_sleep.called


@pytest.mark.asyncio
@patch("controllers.ListTaskRecordCacheController.judge_to_use_cache", new=mock_judge_to_use_cache)
async def test_get_tasks_without_cache(async_client, test_session):
    now = datetime.now(timezone.utc)
    task1_id = str(uuid.uuid4())
    tr1 = TaskRecord(id=task1_id, status=TaskStatus.PENDING, created_at=now, updated_at=now)
    task2_id = str(uuid.uuid4())
    tr2 = TaskRecord(
        id=task2_id, status=TaskStatus.COMPLETED, created_at=now + timedelta(days=1), updated_at=now + timedelta(days=1)
    )
    test_session.add_all([tr1, tr2])
    await test_session.commit()

    response = await async_client.get("/tasks/")
    assert response.status_code == 200

    tasks = response.json()
    assert len(tasks) == 2
    assert tasks[0]["id"] == task1_id
    assert tasks[1]["id"] == task2_id


@pytest.mark.asyncio
@patch("database.constants.CACHE_LOCATION", TEST_CACHE_LOCATION)
async def test_get_tasks_with_cache(async_client, test_session):
    now = datetime.now(timezone.utc)
    task1_id = str(uuid.uuid4())
    tr1 = TaskRecord(id=task1_id, status=TaskStatus.PENDING, created_at=now, updated_at=now)
    task2_id = str(uuid.uuid4())
    tr2 = TaskRecord(
        id=task2_id, status=TaskStatus.COMPLETED, created_at=now + timedelta(days=1), updated_at=now + timedelta(days=1)
    )
    test_session.add_all([tr1, tr2])
    await test_session.commit()

    response = await async_client.get("/tasks/")
    assert response.status_code == 200

    tasks = response.json()
    assert len(tasks) == 2
    assert tasks[0]["id"] == task1_id
    assert tasks[1]["id"] == task2_id


@pytest.mark.asyncio
async def test_delete_task(async_client, test_session):
    task_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)
    tr1 = TaskRecord(id=task_id, status=TaskStatus.PENDING, created_at=now, updated_at=now)
    test_session.add(tr1)
    await test_session.commit()

    response = await async_client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204

    updated_task = await test_session.get(TaskRecord, task_id)
    assert updated_task.status == TaskStatus.CANCELED
