from sqlalchemy import inspect
from sqlalchemy.sql.ddl import CreateSchema

from prolog_backend.repositories.base import BaseRepository


class DatabaseRepository(BaseRepository):
    def schema_exists(self, schema_name: str) -> bool:
        return inspect(self.session.bind).has_schema(schema_name=schema_name)

    def create_schema(self, schema_name: str):
        self.session.execute(CreateSchema(name=schema_name, if_not_exists=True))
