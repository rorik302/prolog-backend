from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from prolog_backend.models.base import SharedModel

if TYPE_CHECKING:
    from prolog_backend.models.tenant import Tenant


class User(SharedModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    tenant_id: Mapped[UUID] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    tenant: Mapped["Tenant"] = relationship(back_populates="users")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
