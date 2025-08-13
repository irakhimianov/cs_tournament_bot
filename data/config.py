import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class Bot:
    token: str


@dataclass
class Redis:
    host: str
    port: int
    db: int


@dataclass
class API:
    url: str
    token: str


@dataclass
class Config:
    bot: Bot
    redis: Redis
    api: API


def load_config() -> Config:
    load_dotenv()

    return Config(
        bot=Bot(
            token=os.getenv('TOKEN', ''),
        ),
        redis=Redis(
            host=os.getenv('REDIS_HOST', ''),
            port=int(os.getenv('REDIS_PORT', '6379')),
            db=int(os.getenv('REDIS_DB', '5')),
        ),
        api=API(
            url=os.getenv('API_URL', ''),
            token=os.getenv('API_TOKEN', ''),
        ),
    )
