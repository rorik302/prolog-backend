import pytest
from prolog_backend.config.api import api_settings
from prolog_backend.models.tenant import Tenant
from prolog_backend.models.user import User
from prolog_backend.schemas.auth import LoginCredentials
from prolog_backend.utils.hasher import Hasher
from sqlalchemy import delete, insert, select
from sqlalchemy.orm import Session

from tests.config import test_settings


class TestAuthAPI:
    @pytest.fixture
    def inactive_test_user(self, session: Session):
        tenant = session.scalar(select(Tenant).filter_by(id=test_settings.TENANT_UUID))
        inactive_user_email = "inactive_test_user@test.ru"
        session.execute(
            insert(User).values(
                email=inactive_user_email,
                password=Hasher.hash(value=test_settings.USER_PASSWORD),
                is_active=False,
                tenant_id=tenant.id,
            )
        )
        session.commit()

        yield session.scalar(select(User).filter_by(email=inactive_user_email))

        session.execute(delete(User).filter_by(email=inactive_user_email))
        session.commit()

    def test_login(self, base_client, uow):
        with base_client:
            response = base_client.post(
                "/api/v1/auth/login",
                json=LoginCredentials(email=test_settings.USER_EMAIL, password=test_settings.USER_PASSWORD).to_json(),
            )

        assert response.status_code == 200
        assert api_settings.AUTH_HEADER_KEY in response.headers
        assert api_settings.REFRESH_COOKIE_KEY in response.cookies
        assert api_settings.SESSION_ID_COOKIE_KEY in response.cookies
        with uow:
            assert uow.memory.sessions.exists(str(test_settings.USER_UUID))
            uow.memory.sessions.delete(str(test_settings.USER_UUID))

    def test_invalid_login(self, base_client, inactive_test_user):
        with base_client:
            # Проверка неверной электронной почты
            response = base_client.post(
                "/api/v1/auth/login",
                json=LoginCredentials(
                    email="invalid_test_user@test.ru", password=test_settings.USER_PASSWORD
                ).to_json(),
            )
            assert response.status_code == 401
            assert response.json()["detail"] == "Unauthorized"

            # Проверка неверного пароля
            response = base_client.post(
                "/api/v1/auth/login",
                json=LoginCredentials(email=test_settings.USER_EMAIL, password="invalid").to_json(),
            )
            assert response.status_code == 401
            assert response.json()["detail"] == "Unauthorized"

            # Проверка неактивного пользователя
            response = base_client.post(
                "/api/v1/auth/login",
                json=LoginCredentials(email=inactive_test_user.email, password=test_settings.USER_PASSWORD).to_json(),
            )
            assert response.status_code == 403
            assert response.json()["detail"] == "UserIsNotActive"
