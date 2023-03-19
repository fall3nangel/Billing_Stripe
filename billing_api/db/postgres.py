from core.config import settings
from fastapi_utils.session import FastAPISessionMaker
from services.db import DBService
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

POSTGRES_URL = f"postgresql+asyncpg://{settings.postgres.user}:{settings.postgres.password}@{settings.postgres.host}:{settings.postgres.port}/{settings.postgres.db}"

schema = "users"
engine = create_async_engine(POSTGRES_URL, echo=True)
engine.execution_options(schema_translate_map={None: schema})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
Base = declarative_base()


def get_db_service() -> DBService:
    session = SessionLocal()
    try:
        yield DBService(session)
    finally:
        session.close()


def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
