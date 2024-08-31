from os import getenv

from dotenv import load_dotenv
from litestar.config.cors import CORSConfig
from pydantic_settings import BaseSettings

load_dotenv()


class CORSSettings(BaseSettings):
    CORS_ALLOW_ORIGIN: str = getenv("CORS_ALLOW_ORIGIN")


cors_settings: CORSSettings = CORSSettings()

cors_config = CORSConfig(allow_credentials=True, allow_origins=cors_settings.CORS_ALLOW_ORIGIN.split(","))
