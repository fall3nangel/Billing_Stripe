from functools import lru_cache

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import settings
from services.db import DBService

POSTGRES_URL = f"postgresql+asyncpg://{settings.postgres.user}:{settings.postgres.password}@{settings.postgres.host}:{settings.postgres.port}/{settings.postgres.db}"

schema = "users"
engine = create_async_engine(POSTGRES_URL, echo=True)
engine.execution_options(schema_translate_map={None: schema})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
Base = declarative_base()
db = SessionLocal()


@lru_cache()
def get_db_service() -> DBService:
    return DBService(db)


@lru_cache()
def get_db():
    return db
