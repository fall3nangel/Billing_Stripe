from pathlib import Path
from typing import Any
from typing import Generator

import pytest

from clients.billing import Billing
from clients.payapi import PayApi
from clients.telegram import TelegramReporter
from core.config import settings
from models.product import Product, Movie
from postgres import SessionTesting

BASE_DIR = Path(__file__).parent.resolve()


@pytest.fixture(scope="session")
def billing_client():
    client = Billing(url=settings.billing_url_test)
    assert client.create_test_user(), client.last_error
    return client


@pytest.fixture(scope="session")
def payapi_client():
    client = PayApi(url=settings.payapi_url_test)
    return client


@pytest.fixture(scope="session")
def db_session(billing_client) -> Generator[SessionTesting, Any, None]:
    yield SessionTesting()


@pytest.fixture(scope="session")
def send_telegram_notify():
    telegream_client = TelegramReporter(token=settings.telegram.token, chat_id=settings.telegram.chat)

    def inner(message):
        return telegream_client.send_notify(message=message)

    return inner


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
