from datetime import datetime
from uuid import UUID

from sqlalchemy import MetaData, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import expression
from uuid6 import uuid7

from prolog_backend.config.database import database_settings

shared_metadata = MetaData(schema=database_settings.SHARED_SCHEMA_NAME)
tenant_metadata = MetaData()


class BaseModel(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7)
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now(), onupdate=func.now())
    is_active: Mapped[bool] = mapped_column(nullable=False, server_default=expression.true())


class SharedModel(BaseModel):
    __abstract__ = True
    metadata = shared_metadata


class TenantModel(BaseModel):
    __abstract__ = True
    metadata = tenant_metadata
