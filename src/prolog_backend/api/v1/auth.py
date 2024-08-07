from datetime import timedelta

from litestar import Request, Response, post
from litestar.datastructures import Cookie, ResponseHeader
from sqlalchemy.orm import Session

from prolog_backend.api.base import BaseController
from prolog_backend.config.api import api_settings
from prolog_backend.config.jwt import jwt_settings
from prolog_backend.schemas.auth import LoginCredentials
from prolog_backend.services.auth import AuthService


class AuthController(BaseController):
    path = "/auth"
    tags = ["Auth"]

    @post("/login", sync_to_thread=False)
    def login(self, request: Request, session: Session, data: LoginCredentials) -> Response:
        result = AuthService(session=session).login(data=data, request=request)
        return Response(
            content=None,
            status_code=200,
            headers=[ResponseHeader(name=api_settings.AUTH_HEADER_KEY, value=result.access_token)],
            cookies=[
                Cookie(
                    key=api_settings.REFRESH_COOKIE_KEY,
                    value=result.refresh_token,
                    max_age=int(timedelta(minutes=jwt_settings.REFRESH_TOKEN_LIFETIME_MINUTES).total_seconds()),
                    httponly=True,
                    secure=True,
                    samesite="strict",
                ),
                Cookie(
                    key=api_settings.SESSION_ID_COOKIE_KEY,
                    value=result.session_id,
                    max_age=int(timedelta(minutes=jwt_settings.ACCESS_TOKEN_LIFETIME_MINUTES).total_seconds()),
                    httponly=True,
                    samesite="strict",
                ),
            ],
        )
