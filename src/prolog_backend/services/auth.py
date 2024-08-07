from datetime import UTC, datetime, timedelta

from argon2.exceptions import VerifyMismatchError
from litestar import Request
from uuid6 import uuid7

from prolog_backend.config.api import api_settings
from prolog_backend.config.jwt import jwt_settings
from prolog_backend.exceptions.auth import InvalidPassword
from prolog_backend.exceptions.user import UserDoesNotExist, UserIsNotActive
from prolog_backend.schemas.auth import LoginCredentials, LoginResult
from prolog_backend.schemas.token import Token, TokenPurpose
from prolog_backend.services.base import BaseService
from prolog_backend.utils.hasher import Algorithm, Hasher


class AuthService(BaseService):
    def login(self, data: LoginCredentials, request: Request) -> LoginResult:
        with self.uow:
            user = self.uow.user.get_or_none(email=data.email)
            if user is None:
                UserDoesNotExist(status_code=401, default_detail=True).raise_exception()
            try:
                Hasher.verify(password=data.password, hashed=user.password)
            except VerifyMismatchError:
                InvalidPassword(status_code=401, default_detail=True).raise_exception()
            if not user.is_active:
                UserIsNotActive(status_code=403).raise_exception()

        session_id = uuid7().hex
        access_token = Token(
            sub=user.id,
            purpose=TokenPurpose.ACCESS,
            session_id=Hasher.hash(value=session_id, algorithm=Algorithm.SHA1),
            iat=datetime.now(UTC).timestamp(),
        ).to_jwt()
        refresh_token = Token(sub=user.id, purpose=TokenPurpose.REFRESH, iat=datetime.now(UTC).timestamp()).to_jwt()

        result = LoginResult(access_token=access_token, refresh_token=refresh_token, session_id=session_id)

        self.uow.memory.sessions.set(
            name=str(user.id), value=access_token, ex=timedelta(minutes=jwt_settings.ACCESS_TOKEN_LIFETIME_MINUTES)
        )
        if refresh_cookie := request.cookies.get(api_settings.REFRESH_COOKIE_KEY):
            self.uow.memory.refresh_tokens_blacklist.set(
                refresh_cookie, "", timedelta(minutes=jwt_settings.REFRESH_TOKEN_LIFETIME_MINUTES)
            )

        return result
