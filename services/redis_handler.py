from typing import Optional
from redis import asyncio as aioredis


class RedisHandler:
    def __init__(self, client: aioredis.Redis):
        self.client = client

    @classmethod
    async def from_url(cls, url: str) -> 'RedisHandler':
        client = aioredis.Redis.from_url(url, encoding='utf-8', decode_responses=True)
        return cls(client)

    async def get_bool(self, key: str) -> Optional[bool]:
        val = await self.client.get(key)
        if val is None:
            return
        return val == '1'

    async def set_bool(self, key: str, value: bool, ttl_seconds: int) -> None:
        await self.client.set(key, '1' if value else '0', ex=ttl_seconds)

    async def delete(self, key: str) -> None:
        await self.client.delete(key)
