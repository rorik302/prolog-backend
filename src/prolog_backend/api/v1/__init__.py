from litestar import Router

from prolog_backend.api.v1.auth import AuthController

v1_router = Router(path="v1", route_handlers=[AuthController])
