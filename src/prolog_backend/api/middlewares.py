from jwt import InvalidSignatureError
from litestar.connection import ASGIConnection
from litestar.middleware import AbstractAuthenticationMiddleware, AuthenticationResult, DefineMiddleware
from litestar.types import ASGIApp

from prolog_backend.config.api import api_settings
from prolog_backend.exceptions.auth import InvalidAuthHeader, InvalidSessionID, InvalidToken, SessionIDNotProvided
from prolog_backend.exceptions.user import UserDoesNotExist
from prolog_backend.repositories.memory import MemoryRepository
from prolog_backend.schemas.token import Token, TokenPurpose
from prolog_backend.services.auth import AuthService
from prolog_backend.utils.hasher import Algorithm, Hasher
from prolog_backend.utils.sqlalchemy import Session


class RequestAuthMiddleware(AbstractAuthenticationMiddleware):
    def __init__(self, app: ASGIApp, exclude: list[str] | None = None):
        super().__init__(app=app, exclude=exclude)

    async def authenticate_request(self, connection: ASGIConnection) -> AuthenticationResult:
        auth_header = connection.headers.get(api_settings.AUTH_HEADER_KEY)
        if auth_header is None or not auth_header.startswith("Bearer "):
            InvalidAuthHeader(status_code=401, default_detail=True).raise_exception()
        session_id = connection.cookies.get(api_settings.SESSION_ID_COOKIE_KEY)
        if session_id is None:
            SessionIDNotProvided(status_code=401, default_detail=True).raise_exception()

        encoded_token = auth_header.split("Bearer ")[-1]
        try:
            token = Token.from_jwt(token=encoded_token)
        except InvalidSignatureError:
            InvalidToken(status_code=401, default_detail=True).raise_exception()
            raise

        if token.purpose != TokenPurpose.ACCESS:
            InvalidToken(status_code=401, default_detail=True).raise_exception()

        if Hasher.hash(value=session_id, algorithm=Algorithm.SHA1) != token.session_id:
            InvalidSessionID(status_code=401, default_detail=True).raise_exception()

        with Session() as session:
            user = AuthService(session=session).get_user_by_id(user_id=token.sub)
            if user is None:
                UserDoesNotExist(status_code=401, default_detail=True).raise_exception()
            if MemoryRepository().sessions.get(name=str(user.id)) != encoded_token:
                InvalidToken(status_code=401, default_detail=True).raise_exception()

        return AuthenticationResult(user=user, auth=token)


request_auth_middleware = DefineMiddleware(RequestAuthMiddleware, exclude=["/api/v1/auth/login"])
