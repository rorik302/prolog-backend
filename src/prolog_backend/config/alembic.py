from pathlib import Path

from pydantic_settings import BaseSettings

from prolog_backend.config.directories import PROJECT_DIR


class AlembicSettings(BaseSettings):
    INI_PATH: Path = PROJECT_DIR / "alembic.ini"
    SHARED_INI_SECTION: str = "shared"
    TENANT_INI_SECTION: str = "tenant"


alembic_settings: AlembicSettings = AlembicSettings()
