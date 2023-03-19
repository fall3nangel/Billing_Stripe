"""Конфигурация приложения."""
import logging
from logging import config as logging_config
from pathlib import Path

from pydantic import BaseSettings, Field

BASE_DIR = Path(__file__).resolve().parent.parent


class Postgres(BaseSettings):
    host: str = Field("127.0.0.1")
    port: int = Field(5432)
    dbname: str = Field("movies_database", alias="db")
    user: str = Field("app")
    password: str = Field("123qwe")


class Settings(BaseSettings):
    postgres: Postgres = Field(Postgres)
    project_name: str = Field("etl")
    debug: bool = Field(False)
    fetch_limit: int = 1000

    class Config:
        env_file = BASE_DIR.joinpath(".env")
        env_nested_delimiter = "__"


settings = Settings()

LOG_DEFAULT_HANDLERS = [
    "console",
]


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "": {
            "handlers": LOG_DEFAULT_HANDLERS,
            "level": "INFO",
        },
    },
    "root": {
        "level": "INFO",
        "formatter": "verbose",
        "handlers": LOG_DEFAULT_HANDLERS,
    },
}


if settings.debug:
    LOGGING["root"]["level"] = "DEBUG"

logging_config.dictConfig(LOGGING)

logging.debug("%s", settings.dict())
