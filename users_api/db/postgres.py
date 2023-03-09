from functools import lru_cache
from asyncio import current_task

import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from services.db import DBService
from core.config import settings

POSTGRES_URL = f"postgresql+asyncpg://{settings.postgres.user}:{settings.postgres.password}@{settings.postgres.host}:{settings.postgres.port}/{settings.postgres.db}"

schema = "users"
engine = create_async_engine(POSTGRES_URL, echo=True)
engine.execution_options(schema_translate_map={None: schema})

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

'''
@lru_cache()
async def get_db() -> AsyncSession:
    return SessionLocal()
'''

@lru_cache()
def get_db_service() -> DBService:
    return DBService(db)

