from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid6 import uuid7

from prolog_backend.models.base import SharedModel

if TYPE_CHECKING:
    from prolog_backend.models.user import User


def generate_tenant_schema_name() -> str:
    return f"tenant_{uuid7().hex}"


class Tenant(SharedModel):
    __tablename__ = "tenants"

    schema_name: Mapped[str] = mapped_column(unique=True, nullable=False, default=generate_tenant_schema_name)
    users: Mapped[list["User"]] = relationship(back_populates="tenant")

    def __repr__(self):
        return f"<Tenant(id={self.id}, schema_name={self.schema_name})>"
