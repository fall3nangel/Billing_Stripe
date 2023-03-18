import logging
from pathlib import Path
from typing import Any, Final
from typing import Generator

import allure
import pytest

from clients.allure_report_push import AllureReportPush
from clients.billing import Billing
from clients.telegram import TelegramReporter
from core.config import settings
from models.product import Product, Movie
from postgres import SessionTesting

BASE_DIR = Path(__file__).parent.resolve()
ALLURE_REPORTS_DIR: Final = BASE_DIR / "allure-report"


def pytest_addoption(parser):
    parser.addoption("--allure-send", action="store_true")


def pytest_configure(config: pytest.Config):
    # Подключение к allure-серверу
    if config.getoption("--allure-send"):
        config.option.allure_report_dir = ALLURE_REPORTS_DIR
        allure_report = AllureReportPush(reports_dir=ALLURE_REPORTS_DIR, **settings.allure.dict())
        if not allure_report.check_connect():
            pytest.exit("Нет подключения к серверу allure!")
        config.allure_report = allure_report


def pytest_unconfigure(config):
    if hasattr(config, "allure_report"):
        if not config.allure_report.send_reports():
            pytest.exit(config.allure_report.last_error)
        logging.info(config.allure_report.url_project)


@allure.title(f"Подключение к API Биллинг сервиса")
@pytest.fixture(scope="session")
def billing_client():
    client = Billing(url=settings.billing_url_test)
    assert client.create_test_user(), client.last_error
    return client


@allure.title(f"Подключение в БД")
@pytest.fixture(scope="session")
def db_session(billing_client) -> Generator[SessionTesting, Any, None]:
    yield SessionTesting()


@allure.title(f"Подключения к телеграм")
@pytest.fixture(scope="session")
def send_telegram_notify():
    telegream_client = TelegramReporter(token=settings.telegram.token, chat_id=settings.telegram.chat)

    def inner(message):
        return telegream_client.send_notify(message=message)

    return inner


@allure.title(f"Заполнение БД тестовыми данными")
@pytest.fixture(scope="session")
def initial_data(db_session):
    movies = [
        Movie(name="Смешарики в кино", description=""),
        Movie(name="Фиксики в кино", description=""),
    ]
    product = Product(name="Фильмы для детей", price=1000.00, duration="month", movies=movies)
    db_session.add(product)
    db_session.flush()
    db_session.commit()
    return product, movies
