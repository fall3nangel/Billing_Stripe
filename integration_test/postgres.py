from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from core.config import settings

POSTGRES_URL = f"postgresql://{settings.postgres.user}:{settings.postgres.password}@{settings.postgres.host}:{settings.postgres.port}/{settings.postgres.db}"
engine = create_engine(POSTGRES_URL, echo=True, pool_pre_ping=True)
engine.execution_options(schema_translate_map={None: "users"})
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
