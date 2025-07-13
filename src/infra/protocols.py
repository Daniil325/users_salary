from abc import ABC, abstractmethod


class RedisRepo(ABC):

    @abstractmethod
    async def get(self, key: str): ...

    @abstractmethod
    async def set(self, key: str, value: str): ...
