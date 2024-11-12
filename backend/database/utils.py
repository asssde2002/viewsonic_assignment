from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlmodel import create_engine
from .constants import ASYNC_DATABASE_URL, DATABASE_URL, CACHE_LOCATION
import redis.asyncio as async_redis
import redis

async_engine = create_async_engine(ASYNC_DATABASE_URL)
sync_engine = create_engine(DATABASE_URL)

async def get_async_session():
    async with AsyncSession(async_engine) as session:
        yield session

def get_redis_client(async_mode: bool = True):
    if async_mode:
        return async_redis.from_url(CACHE_LOCATION)
    else:
        return redis.from_url(CACHE_LOCATION)
