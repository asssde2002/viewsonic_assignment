from sqlmodel import create_engine, Session
from .constants import DATABASE_URL, CACHE_LOCATION
import redis
from contextlib import contextmanager

engine = create_engine(DATABASE_URL)

@contextmanager
def get_session():
    with Session(engine) as session:
        yield session

@contextmanager
def get_redis_client():
    with redis.from_url(CACHE_LOCATION) as client:
        yield client
