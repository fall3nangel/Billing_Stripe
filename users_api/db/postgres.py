from functools import lru_cache

import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from services.db import DBService
from core.config import settings

POSTGRES_URL = f"postgresql+asyncpg://{settings.postgres.user}:{settings.postgres.password}@{settings.postgres.host}:{settings.postgres.port}/{settings.postgres.db}"

engine = create_async_engine(POSTGRES_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

Base = declarative_base()

'''
convention = {
    "all_column_names": lambda constraint, table: "_".join([
        column.name for column in constraint.columns.values()
    ]),
    "ix": "ix__%(table_name)s__%(all_column_names)s",
    "uq": "uq__%(table_name)s__%(all_column_names)s",
    "ck": "ck__%(table_name)s__%(all_column_names)s",
    "fk": ("fk__%(table_name)s__%(all_column_names)s",
           "%(reffered_table_name)s"
           ),
    "pk": "pk__%(table_name)s"
}

metadata = sqlalchemy.MetaData(naming_convention=convention)
'''
# Base.metadata = metadata

db = SessionLocal()

@lru_cache()
async def get_db() -> AsyncSession:
    return SessionLocal()

