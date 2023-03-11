from logger import logger
from models.admin_panel import AdminPanelMovies
from models.billing import BillingMovies


def movie_converter(movies: list[AdminPanelMovies]) -> list[BillingMovies]:
    """
    Конвертирование данных в формат хранения эластика
    :param movies: Список произвдений из БД
    :return: Список произведение формата эластика
    """
    try:
        converted_data = [
            BillingMovies(
                id=movie.id,
                name=movie.title,
                description=movie.description,
            )
            for movie in movies
        ]
    except Exception as error:
        logger.exception("Ошибка валидации данных\n%s", error)
        raise error
    logger.debug(f"Сконвертировано записей - %s", {len(converted_data)})
    return converted_data