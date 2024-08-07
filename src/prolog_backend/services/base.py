from sqlalchemy.orm import Session

from prolog_backend.utils.unit_of_work import UnitOfWork


class BaseService:
    def __init__(self, session: Session):
        self.session = session
        self.uow: UnitOfWork = UnitOfWork(session=session)
