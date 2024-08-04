from logging.config import fileConfig

from alembic import context
from prolog_backend.config.database import database_settings
from prolog_backend.migrations.utils import alembic_include_object, alembic_process_revision_directives
from prolog_backend.models import TenantModel
from sqlalchemy import text
from sqlalchemy.orm import Session

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = TenantModel.metadata

config.set_main_option("sqlalchemy.url", database_settings.DB_URL)


def run_migrations_online() -> None:
    schema_name = config.attributes.get("schema_name")
    assert schema_name, "Нужно передать имя схемы для миграции"
    session: Session = config.attributes.get("session")

    connection = session.connection()
    connection.execute(text(f"SET search_path TO {schema_name}"))
    connection.commit()
    connection.dialect.default_schema_name = schema_name

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_object=alembic_include_object(),
        process_revision_directives=alembic_process_revision_directives(config, context),
    )

    with context.begin_transaction():
        context.run_migrations()


run_migrations_online()
