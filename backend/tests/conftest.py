import asyncio
import os
import sys
from typing import AsyncGenerator, Callable, Generator

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from celery_app import celery_app
from database.constants import ASYNC_TEST_DATABASE_URL

test_engine = create_async_engine(
    ASYNC_TEST_DATABASE_URL,
    future=True,
)

celery_app.conf.update(task_eager_propagates=True, task_always_eager=True)


async_session = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture(scope="session", autouse=True)
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture()
async def test_session() -> AsyncSession:
    async with test_engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.drop_all)
        await connection.run_sync(SQLModel.metadata.create_all)
        async with async_session(bind=connection) as session:
            yield session
            await session.flush()
            await session.rollback()


@pytest.fixture()
def override_get_async_session(test_session: AsyncSession) -> Callable:
    async def _override_get_async_session():
        yield test_session

    return _override_get_async_session


@pytest.fixture()
def app(override_get_async_session: Callable) -> FastAPI:
    from database.utils import get_async_session
    from main import app

    app.dependency_overrides[get_async_session] = override_get_async_session

    return app


@pytest_asyncio.fixture()
async def async_client(app: FastAPI) -> AsyncGenerator:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
