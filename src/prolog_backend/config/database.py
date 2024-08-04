from os import getenv

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class DatabaseSettings(BaseSettings):
    NAME: str = getenv("DB_NAME")
    USER: str = getenv("DB_USER")
    PASSWORD: str = getenv("DB_PASSWORD")
    HOST: str = getenv("DB_HOST")
    PORT: int = int(getenv("DB_PORT"))
    DB_URL: str = f"postgresql+psycopg://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}"
    DEBUG: bool = bool(getenv("DB_DEBUG", False))
    SHARED_SCHEMA_NAME: str = "shared"


database_settings: DatabaseSettings = DatabaseSettings()
