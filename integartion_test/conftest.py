from pathlib import Path
from typing import Any
from typing import Generator

import pytest
from sqlalchemy.sql import text

from clients.billing import Billing
from models.product import Product, Movie
from models.user import User
from postgres import engine, SessionTesting, Base

BASE_DIR = Path(__file__).parent.resolve()


# @pytest.fixture(scope="function")
# def db_session() -> Generator[SessionTesting, Any, None]:
#     connection = engine.connect()
#     transaction = connection.begin()
#     session = SessionTesting(bind=connection)
#     yield session  # use the session in tests.
#     session.close()
#     transaction.rollback()
#     connection.close()


@pytest.fixture(scope="function")
def db_session() -> Generator[SessionTesting, Any, None]:
    db = SessionTesting()
    Base.metadata.create_all(bind=engine)
    yield db
    for tbl in reversed(Base.metadata.sorted_tables):
        print(tbl)
        engine.execute(tbl.delete())
    # engine.execute(text("""TRUNCATE TABLE users."user" CASCADE;"""))


@pytest.fixture(scope="function")
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


@pytest.fixture(scope="session")
def billing_client():
    client = Billing(url="http://127.0.0.1:8000")
    return client
