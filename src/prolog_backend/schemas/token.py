from enum import Enum
from uuid import UUID

import jwt

from prolog_backend.config.jwt import jwt_settings
from prolog_backend.schemas.base import BaseSchema


class TokenPurpose(str, Enum):
    ACCESS = "ACCESS"
    REFRESH = "REFRESH"


class Token(BaseSchema):
    sub: UUID
    purpose: TokenPurpose
    session_id: str | None = None
    iat: float

    def to_jwt(self):
        return jwt.encode(payload=self.to_json(), key=jwt_settings.PRIVATE_KEY, algorithm=jwt_settings.ALGORITHM)
