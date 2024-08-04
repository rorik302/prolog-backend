from argparse import Namespace

from alembic import command
from alembic.config import Config
from sqlalchemy import inspect
from sqlalchemy.sql.ddl import CreateSchema

from prolog_backend.config.alembic import alembic_settings
from prolog_backend.config.database import database_settings
from prolog_backend.repositories.base import BaseRepository


class DatabaseRepository(BaseRepository):
    def schema_exists(self, schema_name: str) -> bool:
        return inspect(self.session.bind).has_schema(schema_name=schema_name)

    def create_schema(self, schema_name: str):
        self.session.execute(CreateSchema(name=schema_name, if_not_exists=True))

    def _get_alembic_config(self, schema_name: str):
        config = Config(alembic_settings.INI_PATH)
        ini_section = (
            alembic_settings.SHARED_INI_SECTION if schema_name == database_settings.SHARED_SCHEMA_NAME else None
        )
        config.config_ini_section = ini_section
        config.attributes["session"] = self.session
        config.attributes["schema_name"] = schema_name
        config.cmd_opts = Namespace(autogenerate=True)
        return config

    def make_migrations(self, schema_name: str, message: str):
        config = self._get_alembic_config(schema_name=schema_name)
        command.revision(config, message=message, autogenerate=True)

    def migrate(self, schema_name: str):
        config = self._get_alembic_config(schema_name=schema_name)
        command.upgrade(config, "head")
