from sqlalchemy.orm import Session

from prolog_backend.repositories.memory import MemoryRepository
from prolog_backend.repositories.user import UserRepository


class UnitOfWork:
    def __init__(self, session: Session):
        self.session = session

    def __enter__(self):
        self.memory: MemoryRepository = MemoryRepository()
        self.user: UserRepository = UserRepository(session=self.session)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            self.session.rollback()
        self.session.close()

    def commit(self):
        self.session.commit()
