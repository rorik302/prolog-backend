from click import group

from prolog_backend.config.app import Mode, app_settings
from prolog_backend.models.tenant import Tenant
from prolog_backend.models.user import User
from prolog_backend.repositories.database import DatabaseRepository
from prolog_backend.repositories.tenant import TenantRepository
from prolog_backend.repositories.user import UserRepository
from prolog_backend.utils.hasher import Hasher
from prolog_backend.utils.sqlalchemy import Session


@group(name="tenant")
def tenant_group():
    """Управление тенантами"""
    pass


@tenant_group.command("init_dev")
def init_dev_tenant():
    """Инициализация тенанта для разработки"""

    assert app_settings.MODE == Mode.DEV

    with Session() as session:
        tenant_repo = TenantRepository(session=session)
        user_repo = UserRepository(session=session)

        if (
            tenant_repo.get_or_none(schema_name="dev") is not None
            or user_repo.get_or_none(email="user@example.com") is not None
        ):
            print("Тенант и пользователь уже существуют")
            return

        tenant_instance = Tenant(schema_name="dev")
        tenant = tenant_repo.create(instance=tenant_instance)
        user_instance = User(email="user@example.com", password=Hasher.hash(value="string"), tenant_id=tenant.id)
        user = user_repo.create(instance=user_instance)
        session.commit()
        session.reset()

        if tenant_repo.get_or_none(id=tenant.id) is not None and user_repo.get_or_none(id=user.id) is not None:
            db_repo = DatabaseRepository(session=session)
            db_repo.create_schema(schema_name=tenant.schema_name)
            db_repo.migrate(schema_name=tenant.schema_name)
