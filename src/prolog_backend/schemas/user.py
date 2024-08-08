from uuid import UUID

from prolog_backend.schemas.base import EmailStr, ModelSchema


class UserOut(ModelSchema):
    email: EmailStr
    tenant_id: UUID
