import logging
import time
from pathlib import Path

import backoff
import psycopg2
from psycopg2.extras import DictCursor

from config import settings
from convertors import movie_converter, product_converter, product_movie_pair_converter
from etl import PostgresExtractor, PostgresLoader
from models.admin_panel import AdminPanelMovie, AdminPanelProduct, AdminPanelProductMoviePair
from query_executors.movies import query_get_movies, query_get_products, query_get_product_movie_pairs
from storage import JsonFileStorage, State

BASE_DIR = Path(__file__).resolve().parent

step_extractors = [
    ("movie", AdminPanelMovie, query_get_movies, movie_converter),
    ("product", AdminPanelProduct, query_get_products, product_converter),
    ("product_movie_link", AdminPanelProductMoviePair, query_get_product_movie_pairs, product_movie_pair_converter),
]


@backoff.on_exception(backoff.expo, (psycopg2.OperationalError, psycopg2.DatabaseError))
def etl():
    """
    Выгрузка данных из потсгреса в эластик
    :return:
    """

    json_data = JsonFileStorage(file_path=BASE_DIR.joinpath("main_states.json").name)
    state = State(json_data)
    with psycopg2.connect(**settings.postgres.dict(), cursor_factory=DictCursor) as pg_connect:
        last_time = state.get_state("last_time")
        pg_extractor = PostgresExtractor(connect=pg_connect, last_time=last_time)
        pg_loader = PostgresLoader(connect=pg_connect)
        expose_last_time = pg_extractor.get_server_datetime()
        for billing_bd_name, validator, query_executor, converter_executor in step_extractors:
            for data in pg_extractor.get_updated(validator=validator, query_executor=query_executor):
                logging.debug("Extracted data: %s", data)
                billing_format_data = converter_executor(data)
                pg_loader.save_all_data(db=billing_bd_name, inserted_data=billing_format_data)
        pg_loader.commit_data()
        state.set_state("last_time", expose_last_time)
        logging.info("Сохранено состояние %s", expose_last_time)


if __name__ == "__main__":
    while True:
        etl()
        time.sleep(10)
