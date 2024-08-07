from prolog_backend.models.tenant import Tenant
from prolog_backend.repositories.base import SQLAlchemyRepository


class TenantRepository(SQLAlchemyRepository[Tenant]):
    model = Tenant
