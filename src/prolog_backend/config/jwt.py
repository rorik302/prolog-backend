from os import getenv

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from prolog_backend.config.directories import PROJECT_DIR

load_dotenv()


class JWTSettings(BaseSettings):
    PRIVATE_KEY: str = (PROJECT_DIR / "certs/jwt_private.pem").read_text()
    PUBLIC_KEY: str = (PROJECT_DIR / "certs/jwt_public.pem").read_text()
    ALGORITHM: str = "RS256"
    ACCESS_TOKEN_LIFETIME_MINUTES: int = getenv("JWT_ACCESS_TOKEN_LIFETIME_MINUTES")
    REFRESH_TOKEN_LIFETIME_MINUTES: int = getenv("JWT_REFRESH_TOKEN_LIFETIME_MINUTES")


jwt_settings: JWTSettings = JWTSettings()
