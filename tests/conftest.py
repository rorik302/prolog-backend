import pytest
from litestar.testing import TestClient
from prolog_backend.app import create_app
from prolog_backend.config.api import api_settings
from prolog_backend.config.app import Mode, app_settings
from prolog_backend.config.database import database_settings
from prolog_backend.models import SharedModel, TenantModel
from prolog_backend.models.tenant import Tenant
from prolog_backend.models.user import User
from prolog_backend.schemas.auth import LoginCredentials
from prolog_backend.services.auth import AuthService
from prolog_backend.utils.hasher import Hasher
from prolog_backend.utils.sqlalchemy import Session, engine
from prolog_backend.utils.unit_of_work import UnitOfWork
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
                id=test_settings.USER_UUID,
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


@pytest.fixture
def session():
    with Session() as session:
        yield session


@pytest.fixture
def uow(session) -> UnitOfWork:
    return UnitOfWork(session=session)


@pytest.fixture(scope="session")
def app():
    return create_app()


@pytest.fixture
def base_client(app):
    return TestClient(app=app)


@pytest.fixture
def client(session, base_client):
    result = AuthService(session=session).login(
        data=LoginCredentials(email=test_settings.USER_EMAIL, password=test_settings.USER_PASSWORD)
    )
    base_client.headers.update({api_settings.AUTH_HEADER_KEY: f"Bearer {result.access_token}"})
    base_client.cookies.set(name=api_settings.REFRESH_COOKIE_KEY, value=result.refresh_token)
    base_client.cookies.set(name=api_settings.SESSION_ID_COOKIE_KEY, value=result.session_id)
    return base_client
