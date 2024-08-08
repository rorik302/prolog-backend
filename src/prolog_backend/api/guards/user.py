from litestar.connection import ASGIConnection
from litestar.handlers import BaseRouteHandler

from prolog_backend.exceptions.user import UserIsNotActive


def user_is_active(connection: ASGIConnection, route_handler: BaseRouteHandler) -> None:
    if route_handler.name not in ["login"]:
        if connection.user and connection.user.is_active:
            return

        UserIsNotActive(status_code=403).raise_exception()
