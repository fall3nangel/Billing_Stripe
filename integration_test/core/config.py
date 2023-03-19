"""Конфигурация приложения."""
import logging
from logging import config as logging_config
from pathlib import Path

from pydantic import BaseSettings, Field

from core.logger import LOGGING

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Allure(BaseSettings):
    url: str = "http://127.0.0.1:5050"
    project_name: str = "default"
    generate_reports: bool = True
    clean_project: bool = True


class Postgres(BaseSettings):
    host: str = Field("127.0.0.1")
    port: int = Field(5432)
    db: str = Field("movies_database")
    user: str = Field("app")
    password: str = Field("123qwe")


class Telegram(BaseSettings):
    token: str = Field("6034914427:AAHDvUiv-3ULTX-PTrsIY85UMnoU67jaf1A")
    chat: str = Field("-895829670")
    send: bool = False


class Settings(BaseSettings):
    postgres: Postgres = Field(Postgres())
    project_name: str = Field("integartion_tests")
    telegram: Telegram = Field(Telegram())
    allure: Allure = Field(Allure())
    debug: bool = Field(False)
    payapi_url_test: str
    billing_url_test: str

    class Config:
        env_file = BASE_DIR.joinpath(".env")
        env_nested_delimiter = "__"


settings = Settings()

if settings.debug:
    LOGGING["root"]["level"] = "DEBUG"

logging_config.dictConfig(LOGGING)
logging.debug("%s", settings.dict())
