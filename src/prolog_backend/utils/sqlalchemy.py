from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from prolog_backend.config.database import database_settings

engine = create_engine(url=database_settings.DB_URL, pool_pre_ping=True, echo=database_settings.DEBUG)
Session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
