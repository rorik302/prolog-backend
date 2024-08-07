from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from prolog_backend.models.base import BaseModel


class BaseRepository:
    def __init__(self, session: Session):
        self.session = session


ModelType = TypeVar("ModelType", bound=BaseModel)


class SQLAlchemyRepository(BaseRepository, Generic[ModelType]):
    model: ModelType | None = None

    def __init__(self, session: Session):
        if self.model is None:
            raise AttributeError(f"Не указана модель для репозитория {self.__class__.__name__}")
        super().__init__(session=session)

    def get_or_none(self, **kwargs) -> ModelType | None:
        query = select(self.model).filter_by(**kwargs)
        return self.session.scalar(query)

    def create(self, instance: ModelType) -> ModelType:
        self.session.add(instance)
        self.session.flush()
        return instance
