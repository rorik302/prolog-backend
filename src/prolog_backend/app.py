from litestar import Litestar

from prolog_backend.config.app import app_settings


def create_app() -> Litestar:
    return Litestar(debug=app_settings.DEBUG)


app = create_app()
