from prolog_backend.models.user import User
from prolog_backend.repositories.base import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = User
