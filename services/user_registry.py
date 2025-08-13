from services.redis_handler import RedisHandler
from services.api_client import APIClient


class UserRegistryService:
    def __init__(self, redis_handler: RedisHandler, api_client: APIClient, ttl: int = 600):
        self.redis_handler = redis_handler
        self.api_client = api_client
        self.ttl = ttl

    def _key(self, key_prefix: str, telegram_id: int) -> str:
        return f"{key_prefix}:{telegram_id}"

    async def is_verified(self, telegram_id: int) -> bool:
        key_prefix = 'verified'
        key = self._key(key_prefix, telegram_id)
        cached = await self.redis_handler.get_bool(key)
        if cached is not None:
            return cached

        response = await self.api_client.get_players(params={'telegram_id': telegram_id, 'is_verified': True})
        data = response.json()
        if data.get('results'):
            await self.redis_handler.set_bool(key, True, self.ttl)
            return True
        return False

    async def is_agreed(self, telegram_id: int) -> bool:
        key_prefix = 'agreed'
        key = self._key(key_prefix, telegram_id)
        cached = await self.redis_handler.get_bool(key)
        if cached is not None:
            return cached

        response = await self.api_client.get_players(params={'telegram_id': telegram_id, 'is_agreed': True})
        data = response.json()
        if data.get('results'):
            await self.redis_handler.set_bool(key, True, self.ttl)
            return True
        return False

    async def is_admin(self, telegram_id: int) -> bool:
        key_prefix = 'admin'
        key = self._key(key_prefix, telegram_id)
        cached = await self.redis_handler.get_bool(key)
        if cached is not None:
            return cached

        response = await self.api_client.get_profiles(params={'telegram_id': telegram_id, 'is_admin': True})
        data = response.json()
        if data.get('results'):
            await self.redis_handler.set_bool(key, True, self.ttl)
            return True
        return False

    async def with_team(self, telegram_id: int) -> bool:
        key_prefix = 'with_team'
        key = self._key(key_prefix, telegram_id)
        cached = await self.redis_handler.get_bool(key)
        if cached is not None:
            return cached

        response = await self.api_client.get_players(params={'telegram_id': telegram_id, 'with_team': True})
        data = response.json()
        if data.get('results'):
            await self.redis_handler.set_bool(key, True, self.ttl)
            return True
        return False

    async def is_questioned(self, telegram_id: int) -> bool:
        key_prefix = 'is_questioned'
        key = self._key(key_prefix, telegram_id)
        cached = await self.redis_handler.get_bool(key)
        if cached is not None:
            return cached

        response = await self.api_client.get_players(params={'telegram_id': telegram_id, 'is_questioned': True})
        data = response.json()
        if data.get('results'):
            await self.redis_handler.set_bool(key, True, self.ttl)
            return True
        return False
