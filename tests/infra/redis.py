import pytest
from redis.asyncio import Redis

from src.infra.redis import RedisImpl


@pytest.fixture
async def init_data(redis: Redis):
    await redis.set("aaa", "bbb")


async def test_redis_get(redis, init_data):
    store = RedisImpl(redis)
    assert await store.get("aaa") == b"bbb"
    
    
async def test_redis_set(redis):
    store = RedisImpl(redis)
    await store.set("test addr", "addr value")
    result = await store.get("test addr")
    assert result == b"addr value"