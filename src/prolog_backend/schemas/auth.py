from prolog_backend.schemas.base import BaseSchema, EmailStr


class LoginCredentials(BaseSchema):
    email: EmailStr
    password: str


class LoginResult(BaseSchema):
    access_token: str
    refresh_token: str
    session_id: str
