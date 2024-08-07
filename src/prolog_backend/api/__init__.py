from litestar import Router

from prolog_backend.api.v1 import v1_router
from prolog_backend.dependencies.database import get_session

api_router = Router(path="/api", route_handlers=[v1_router], dependencies={"session": get_session})
