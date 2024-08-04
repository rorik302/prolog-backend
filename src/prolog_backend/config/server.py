from os import getenv

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = bool(getenv("SERVER_RELOAD", False))


server_settings: ServerSettings = ServerSettings()
