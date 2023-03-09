import json
from typing import Generic
from aioredis import Redis
from typing import Generic, TypeVar


T = TypeVar("T")

CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class RedisService(Generic[T]):

    def __init__(self, redis: Redis):
        self.redis = redis

    async def put_item(self, item: T) -> None:
        typ = self.__orig_class__.__args__[0]

        key = f"{typ.__name__}:{item.id}"

        await self.redis.set(key, item.json(), expire=CACHE_EXPIRE_IN_SECONDS)

    async def get_item(self, id: str) -> T | None:
        typ = self.__orig_class__.__args__[0]

        key = f"{typ.__name__}:{id}"

        data = await self.redis.get(key)
        if not data:
            return None

        return typ.parse_raw(data)

    async def clear(self):
        await self.redis.flushdb()
