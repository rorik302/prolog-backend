from typing import Generator

from sqlalchemy.orm import Session as _Session

from prolog_backend.utils.sqlalchemy import Session


def get_session() -> Generator[_Session, None, None]:
    with Session() as session:
        yield session
