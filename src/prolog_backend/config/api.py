from pydantic_settings import BaseSettings


class APISettings(BaseSettings):
    AUTH_HEADER_KEY: str = "Authorization"
    REFRESH_COOKIE_KEY: str = "refresh"
    SESSION_ID_COOKIE_KEY: str = "session_id"


api_settings: APISettings = APISettings()
