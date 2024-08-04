from click import group

from prolog_backend.repositories.database import DatabaseRepository
from prolog_backend.utils.sqlalchemy import Session


@group(name="database")
def database_group():
    """Управление базой данных"""
    pass


@database_group.command("create_schema")
def create_schema():
    """Создание схемы"""

    while len(schema_name := input("Имя схемы: ")) == 0:
        print("Название схемы не может быть пустым")

    with Session() as session:
        db_repo = DatabaseRepository(session=session)
        if db_repo.schema_exists(schema_name=schema_name):
            print("Схема с таким именем уже существует")
            return
        db_repo.create_schema(schema_name=schema_name)
        session.commit()
