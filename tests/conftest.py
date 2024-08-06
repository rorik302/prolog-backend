import pytest
from prolog_backend.config.app import Mode, app_settings
from prolog_backend.config.database import database_settings
from prolog_backend.models import SharedModel, TenantModel
from prolog_backend.models.tenant import Tenant
from prolog_backend.models.user import User
from prolog_backend.utils.hasher import Hasher
from prolog_backend.utils.sqlalchemy import engine
from sqlalchemy import insert
from sqlalchemy.sql.ddl import CreateSchema, DropSchema

from tests.config import test_settings


@pytest.fixture(autouse=True)
def prepare_db():
    assert app_settings.MODE == Mode.TEST

    with engine.connect() as conn:
        # Подготовка схем БД
        conn.execute(DropSchema(name=database_settings.SHARED_SCHEMA_NAME, if_exists=True, cascade=True))
        conn.execute(DropSchema(name=test_settings.TENANT_SCHEMA_NAME, if_exists=True, cascade=True))
        conn.execute(CreateSchema(name=database_settings.SHARED_SCHEMA_NAME, if_not_exists=True))
        conn.execute(CreateSchema(name=test_settings.TENANT_SCHEMA_NAME, if_not_exists=True))
        SharedModel.metadata.create_all(bind=conn)
        TenantModel.metadata.create_all(bind=conn)

        # Создание тенанта и пользователя
        conn.execute(insert(Tenant).values(id=test_settings.TENANT_UUID, schema_name=test_settings.TENANT_SCHEMA_NAME))
        conn.execute(
            insert(User).values(
                email=test_settings.USER_EMAIL,
                password=Hasher.hash(value=test_settings.USER_PASSWORD),
                tenant_id=test_settings.TENANT_UUID,
            )
        )
        conn.commit()

    yield

    with engine.connect() as conn:
        # Очистка БД
        conn.execute(DropSchema(name=database_settings.SHARED_SCHEMA_NAME, if_exists=True, cascade=True))
        conn.execute(DropSchema(name=test_settings.TENANT_SCHEMA_NAME, if_exists=True, cascade=True))
        conn.commit()
