import datetime

import psycopg2
from psycopg2.extensions import connection as pg_connection
from pydantic import ValidationError

from config import settings
from logger import logger


class PostgresExtractor:
    """
    Порционное получение актуальных данных по фильмам из БД
    """

    def __init__(self, connect: pg_connection, last_time=None):
        """
        :param connect: Соединение с базой Postgress
        """
        self.cursor = connect.cursor()
        self.last_time = last_time if last_time else datetime.datetime.min
        self.limit = settings.fetch_limit

    def get_server_datetime(self) -> datetime.datetime:
        """
        Получение текущего времени сервера Postgress
        :return:
        """
        self.cursor.execute("select now();")
        data = self.cursor.fetchall().pop()
        return data[0]

    def get_updated(self, query_executor, validator):
        offset = 0
        while True:
            query = query_executor(last_time=self.last_time, limit=self.limit, offset=offset)
            logger.debug(query)
            self.cursor.execute(query)
            try:
                models_list = [validator(**dict(row)) for row in self.cursor.fetchall()]
            except ValidationError as error:
                logger.exception("Ошибка валидации данных postgress \n%s", error)
                raise error
            if not models_list:
                break
            logger.debug(f"Получено записей - %s", {len(models_list)})
            yield models_list
            offset = offset + self.limit


class PostgresLoader:
    def __init__(self, connect: pg_connection):
        self.connect = connect
        self.cursor = connect.cursor()

    def save_all_data(self, db: str, inserted_data):
        # Получаем список имен полей для вставки
        fields_name_list = [key for key in inserted_data[0].dict()]
        # Переформатирем список полей в строку в формат sql
        fields_name_str = ", ".join([key for key in fields_name_list])
        fields_name_str_with_exclude = ", ".join([f"EXCLUDED.{key}" for key in fields_name_list])
        # Генерим строку по количеству элементов для вставки из %s для формата sql
        amount_values_str = ", ".join("%s" for _ in range(len(fields_name_list)))
        # Список из объектов данных
        inserted_data_list = [tuple(values_row.dict().values()) for values_row in inserted_data]
        logger.debug(inserted_data_list)
        try:
            self.cursor.executemany(
                f"""INSERT INTO {db}({fields_name_str}) VALUES({amount_values_str}) 
                        ON CONFLICT (id) 
                        DO UPDATE SET ({fields_name_str}) = ({fields_name_str_with_exclude});""",
                inserted_data_list,
            )

        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(error)
            raise error

    def commit_data(self):
        self.connect.commit()
