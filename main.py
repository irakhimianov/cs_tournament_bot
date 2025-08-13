import asyncio
import logging
from aiogram.contrib.middlewares.logging import LoggingMiddleware

import handlers
from loader import dp, bot, config
from services import notify_admin, set_default_commands
from services.redis_handler import RedisHandler
from services.user_registry import UserRegistryService
from services.api_client import APIClient

logger = logging.getLogger(__name__)


async def on_startup() -> None:
    logger.info('Setting up middlewares...')
    dp.setup_middleware(LoggingMiddleware())

    redis_handler = await RedisHandler.from_url(f'redis://{config.redis.host}:{config.redis.port}/{config.redis.db}')
    api_client = APIClient(url=config.api.url, token=config.api.token)
    registry = UserRegistryService(redis_handler=redis_handler, api_client=api_client)
    dp["registry_service"] = registry
    dp["api_client"] = api_client

    logger.info('Setting default commands...')
    await set_default_commands(dp)

    await dp.skip_updates()
    await dp.start_polling()


async def on_shutdown() -> None:
    logger.info('Shutting down...')
    await dp.storage.close()
    await dp.storage.wait_closed()
    bot_session = await bot.get_session()
    await bot_session.close()


async def main() -> None:
    try:
        await on_startup()
    finally:
        await on_shutdown()


if __name__ == '__main__':
    asyncio.run(main())
