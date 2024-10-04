from codecs import decode
from typing import Any, Sequence, Literal, Optional, Type
from datetime import timedelta

import redis.asyncio as aioredis


class RedisClient:
    def __init__(self, client: aioredis.Redis) -> None:
        self._client = client
        self.DEFAULT_TOKENS_COUNT: int = 5

    @classmethod
    def from_url(cls: Type["RedisClient"], url: str) -> "RedisClient":
        return cls(client=aioredis.from_url(url, decode_responses=True))

    @staticmethod
    def _convert_key(key: Optional[str | int]) -> str:
        return str(key)

    @staticmethod
    def _convert_result_list(result: Optional[Sequence[bytes]]) -> Sequence[str]:
        return [*map(decode, result)]

    async def get_one(self, key: Optional[str | int]) -> Optional[str]:
        return await self._client.get(self._convert_key(key))

    async def set_one(
        self,
        key: Optional[str | int],
        value: Optional[str | int],
        expire: Optional[timedelta | int],
    ) -> Optional[bool]:
        return await self._client.set(
            self._convert_key(key), self._convert_key(value), ex=expire
        )

    async def set_dict(
        self, key: Optional[str | int], value: Optional[dict]
    ) -> Optional[int]:
        return await self._client.hset(self._convert_key(key), mapping=value)

    async def get_dict_all(self, key: Optional[str | int]) -> Optional[dict]:
        return await self._client.hgetall(self._convert_key(key))

    async def delete(self, *keys: Optional[str | int]) -> Optional[int]:
        return await self._client.delete(*{self._convert_key(key) for key in keys})

    async def set_list(
        self,
        key: Any,
        *values: str,
        side: Literal["right", "left"] = "left",
        expire_seconds: Optional[int] = None,
        expire_milliseconds: Optional[int] = None,
    ) -> int:
        key = self._convert_key(key)

        push = self._client.lpush if side == "left" else self._client.rpush

        result = await push(key, *values)

        if expire_seconds:
            await self._client.expire(key, expire_seconds)
        if expire_milliseconds:
            await self._client.pexpire(key, expire_milliseconds)

        return result

    async def get_list(self, key: Any, start: int = 0, end: int = -1) -> Sequence[str]:
        return self._convert_result_list(
            await self._client.lrange(self._convert_key(key), start, end)
        )

    async def pop(self, key: Any, value: str, count: int = 0) -> int:
        return await self._client.lrem(self._convert_key(key), count, value)

    async def set_expire(
        self, key: Optional[str | int], time: Optional[timedelta | int]
    ) -> Optional[bool]:
        return await self._client.expire(self._convert_key(key), time)

    async def get_ttl(self, key: Optional[str | int]) -> Optional[int]:
        return await self._client.ttl(self._convert_key(key))
