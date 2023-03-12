from logger import logger
from models.admin_panel import AdminPanelMovies, AdminPanelProduct
from models.billing import BillingMovies, BillingProduct


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

def product_converter(movies: list[AdminPanelProduct]) -> list[BillingProduct]:
    """
    Конвертирование данных в формат хранения эластика
    :param movies: Список произвдений из БД
    :return: Список произведение формата эластика
    """
    try:
        converted_data = [
            BillingProduct(
                id=product.id,
                name=product.name,
                price=product.price,
                duration=product.duration,
            )
            for product in movies
        ]
    except Exception as error:
        logger.exception("Ошибка валидации данных\n%s", error)
        raise error
    logger.debug(f"Сконвертировано записей - %s", {len(converted_data)})
    return converted_data