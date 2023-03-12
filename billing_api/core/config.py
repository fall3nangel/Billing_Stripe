"""Конфигурация приложения."""
import logging
from logging import config as logging_config
from pathlib import Path

from pydantic import BaseModel, BaseSettings, Field

from core.logger import LOGGING

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class UsersApp(BaseModel):
    jwt_secret_key: str = Field("someword")
    algorithm: str = Field("HS256")
    create_pay_url: str = Field("http://0.0.0.0:8000/api/v1/pay/create")
    cancel_pay_url: str = Field("http://0.0.0.0:8000/api/v1/pay/cancel")

class Postgres(BaseSettings):
    host: str = Field("127.0.0.1")
    port: int = Field(5432)
    db: str = Field("movies_database")
    user: str = Field("app")
    password: str = Field("123qwe")


class Rabbitmq(BaseModel):
    server: str = Field("127.0.0.1")
    port: int = Field(5672)
    user: str
    password: str


class Settings(BaseSettings):
    users_app: UsersApp = Field(UsersApp())
    postgres: Postgres = Field(Postgres)
    rabbitmq: Rabbitmq = Field(Rabbitmq)
    project_name: str = Field("billing")
    debug: bool = Field(False)

    class Config:
        env_file = BASE_DIR.joinpath(".env")
        env_nested_delimiter = "__"


settings = Settings()

if settings.debug:
    LOGGING["root"]["level"] = "DEBUG"

logging_config.dictConfig(LOGGING)

logging.debug("%s", settings.dict())
