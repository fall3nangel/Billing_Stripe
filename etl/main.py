import time
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import DictCursor

from convertors import movie_converter, product_converter

# from backoff import backoff
# from converters import converter_genres, converter, converter_persons
from etl import PostgresExtractor, PostgresLoader
from models.admin_panel import AdminPanelMovies, AdminPanelProduct
from logger import logger

# from models import FetchedGenres, FetchedFilmWorks, FetchedPersons
from query_executors.movies import query_get_movies, query_get_products
from config import settings
from storage import JsonFileStorage, State

BASE_DIR = Path(__file__).resolve().parent

load_dotenv()

step_extractors = [
    # ("movie", AdminPanelMovies, query_get_movies, movie_converter),
    ("product", AdminPanelProduct, query_get_products, product_converter),
]


# @backoff()
def postgres_to_elastic():
    """
    Выгрузка данных из потсгреса в эластик
    :return:
    """

    json_data = JsonFileStorage(file_path=BASE_DIR.joinpath("main_states.json").name)
    state = State(json_data)
    with psycopg2.connect(**settings.postgres.dict(), cursor_factory=DictCursor) as pg_connect:
        last_time = state.get_state("last_time")
        logger.debug("storage last time: %s", last_time)
        pg_extractor = PostgresExtractor(connect=pg_connect, last_time=last_time)
        pg_loader = PostgresLoader(connect=pg_connect)
        expose_last_time = pg_extractor.get_server_datetime()
        logger.debug("expose last time: %s", expose_last_time)
        for billing_bd_name, validator, query_executor, converter_executor in step_extractors:
            logger.info("Заполнение индекса %s", billing_bd_name)
            for data in pg_extractor.get_updated(validator=validator, query_executor=query_executor):
                print(data)
                billing_format_data = converter_executor(data)
                pg_loader.save_all_data(db=billing_bd_name, inserted_data=billing_format_data)
                time.sleep(1)
    #
    #     state.set_state("last_time", expose_last_time)
    #     logger.info("Сохранено состояние %s", expose_last_time)


if __name__ == "__main__":
    while True:
        postgres_to_elastic()
        time.sleep(10)
