from datetime import UTC, datetime, timedelta
from uuid import UUID

from argon2.exceptions import VerifyMismatchError
from jwt import InvalidSignatureError
from litestar import Request
from uuid6 import uuid7

from prolog_backend.config.api import api_settings
from prolog_backend.config.jwt import jwt_settings
from prolog_backend.exceptions.auth import InvalidPassword, InvalidToken
from prolog_backend.exceptions.user import UserDoesNotExist, UserIsNotActive
from prolog_backend.models.user import User
from prolog_backend.repositories.memory import MemoryRepository
from prolog_backend.schemas.auth import LoginCredentials, LoginResult, RefreshResult
from prolog_backend.schemas.token import Token, TokenPurpose
from prolog_backend.schemas.user import UserOut
from prolog_backend.services.base import BaseService
from prolog_backend.utils.hasher import Algorithm, Hasher


class AuthService(BaseService):
    def login(self, data: LoginCredentials, request: Request | None = None) -> LoginResult:
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
        if request is not None:
            if refresh_cookie := request.cookies.get(api_settings.REFRESH_COOKIE_KEY):
                self.uow.memory.refresh_tokens_blacklist.set(
                    refresh_cookie, "", timedelta(minutes=jwt_settings.REFRESH_TOKEN_LIFETIME_MINUTES)
                )

        return result

    def get_user_by_id(self, user_id: UUID) -> User | None:
        with self.uow:
            user = self.uow.user.get_or_none(id=user_id)
        return user

    @staticmethod
    def get_user_from_request(request: Request) -> UserOut:
        return UserOut.to_model(request.user)

    def logout(self, request: Request):
        with self.uow:
            self.uow.memory.sessions.delete(str(request.user.id))

        if refresh_cookie := request.cookies.get(api_settings.REFRESH_COOKIE_KEY):
            self.uow.memory.refresh_tokens_blacklist.set(
                refresh_cookie, "", timedelta(minutes=jwt_settings.REFRESH_TOKEN_LIFETIME_MINUTES)
            )

    def refresh_tokens(self, request: Request) -> RefreshResult:
        cookie_refresh_token = request.cookies.get(api_settings.REFRESH_COOKIE_KEY)
        if cookie_refresh_token is None:
            InvalidToken(status_code=401).raise_exception()
        if MemoryRepository().refresh_tokens_blacklist.exists(cookie_refresh_token):
            InvalidToken(status_code=401).raise_exception()
        try:
            token = Token.from_jwt(token=cookie_refresh_token)
        except InvalidSignatureError:
            InvalidToken(status_code=401).raise_exception()
            raise
        if token.purpose != TokenPurpose.REFRESH:
            InvalidToken(status_code=401).raise_exception()
        if token.sub != request.user.id:
            InvalidToken(status_code=401).raise_exception()
        if (
            token.iat + timedelta(minutes=jwt_settings.REFRESH_TOKEN_LIFETIME_MINUTES).total_seconds()
            < datetime.now(UTC).timestamp()
        ):
            InvalidToken(status_code=401).raise_exception()

        session_id = uuid7().hex
        access_token = Token(
            sub=request.user.id,
            purpose=TokenPurpose.ACCESS,
            session_id=Hasher.hash(value=session_id, algorithm=Algorithm.SHA1),
            iat=datetime.now(UTC).timestamp(),
        ).to_jwt()
        refresh_token = Token(
            sub=request.user.id, purpose=TokenPurpose.REFRESH, iat=datetime.now(UTC).timestamp()
        ).to_jwt()

        result = RefreshResult(access_token=access_token, refresh_token=refresh_token, session_id=session_id)

        MemoryRepository().sessions.set(
            name=str(request.user.id),
            value=access_token,
            ex=timedelta(minutes=jwt_settings.ACCESS_TOKEN_LIFETIME_MINUTES),
        )
        MemoryRepository().refresh_tokens_blacklist.set(
            cookie_refresh_token, "", timedelta(minutes=jwt_settings.REFRESH_TOKEN_LIFETIME_MINUTES)
        )

        return result
