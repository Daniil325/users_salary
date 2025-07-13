from redis.asyncio import Redis

from src.infra.protocols import RedisRepo


class RedisImpl(RedisRepo):

    def __init__(self, client: Redis):
        self._client = client

    async def get(self, key: str) -> bytes:
        result = await self._client.get(key)
        return result

    async def set(self, key: str, value: str) -> None:
        await self._client.set(key, value)
