from os import getenv

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class RedisSettings(BaseSettings):
    HOST: str = getenv("REDIS_HOST")
    PORT: int = int(getenv("REDIS_PORT"))
    PASSWORD: str = getenv("REDIS_PASSWORD")


redis_settings: RedisSettings = RedisSettings()
