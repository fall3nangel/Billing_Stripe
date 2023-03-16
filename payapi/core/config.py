"""Конфигурация приложения."""
import logging
from logging import config as logging_config
from pathlib import Path

from pydantic import BaseModel, BaseSettings, Field

from core.logger import LOGGING

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    stripe_max_net_retries: int
    stripe_api_key: str
    stripe_webhook_secret: str
    billing_url: str = Field("http://0.0.0.0:8000/billing_api/v1/add-payment")
    project_name: str = Field("payapi")
    debug: bool = Field(False)

    class Config:
        env_file = BASE_DIR.joinpath(".env")
        env_nested_delimiter = "__"


settings = Settings()

if settings.debug:
    LOGGING["root"]["level"] = "DEBUG"

logging_config.dictConfig(LOGGING)

logging.debug("%s", settings.dict())
