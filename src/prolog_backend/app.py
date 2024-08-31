from litestar import Litestar

from prolog_backend.api import api_router
from prolog_backend.config.app import app_settings
from prolog_backend.config.cors import cors_config


def create_app() -> Litestar:
    return Litestar(debug=app_settings.DEBUG, route_handlers=[api_router], cors_config=cors_config)


app = create_app()
