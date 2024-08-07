from typing import Annotated

from pydantic import BaseModel, BeforeValidator
from pydantic import EmailStr as _EmailStr

EmailStr = Annotated[_EmailStr, BeforeValidator(lambda v: v.lower())]


class BaseSchema(BaseModel):
    def to_json(self, exclude_none=True, exclude_unset=True):
        return self.model_dump(mode="json", exclude_none=exclude_none, exclude_unset=exclude_unset)
