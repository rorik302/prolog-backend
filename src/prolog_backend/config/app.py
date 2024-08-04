from enum import Enum
from os import getenv

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Mode(str, Enum):
    DEV = "DEV"
    PROD = "PROD"
    TEST = "TEST"


class AppSettings(BaseSettings):
    MODE: Mode = getenv("APP_MODE")
    DEBUG: bool = bool(getenv("APP_DEBUG", False))


app_settings: AppSettings = AppSettings()
