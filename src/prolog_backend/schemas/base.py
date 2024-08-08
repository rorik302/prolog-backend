from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, BeforeValidator
from pydantic import EmailStr as _EmailStr

from prolog_backend.models.base import BaseModel as _BaseModel

EmailStr = Annotated[_EmailStr, BeforeValidator(lambda v: v.lower())]


class BaseSchema(BaseModel):
    def to_json(self, exclude_none=True, exclude_unset=True):
        return self.model_dump(mode="json", exclude_none=exclude_none, exclude_unset=exclude_unset)

    @classmethod
    def to_model(cls, obj: _BaseModel):
        return cls.model_validate(obj, from_attributes=True)


class ModelSchema(BaseSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime
    is_active: bool
