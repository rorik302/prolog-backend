from logging.config import fileConfig

from alembic import context
from prolog_backend.config.database import database_settings
from prolog_backend.migrations.utils import alembic_include_object, alembic_process_revision_directives
from prolog_backend.models import SharedModel
from sqlalchemy import text
from sqlalchemy.orm import Session

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = SharedModel.metadata

config.set_main_option("sqlalchemy.url", database_settings.DB_URL)


def run_migrations_online() -> None:
    session: Session = config.attributes.get("session") or context.get_x_argument(as_dictionary=True).get("session")
    assert session, "Нужно передать сессию для миграции"

    connection = session.connection()
    connection.execute(text(f"SET search_path TO {database_settings.SHARED_SCHEMA_NAME}"))
    connection.commit()
    connection.dialect.default_schema_name = database_settings.SHARED_SCHEMA_NAME
    context.configure(
        connection=session.connection(),
        target_metadata=target_metadata,
        include_object=alembic_include_object(),
        process_revision_directives=alembic_process_revision_directives(config=config, context=context),
    )

    with context.begin_transaction():
        context.run_migrations()

    connection.close()


run_migrations_online()
