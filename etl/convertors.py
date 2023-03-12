from logger import logger
from models.admin_panel import AdminPanelMovie, AdminPanelProduct, AdminPanelProductMoviePair
from models.billing import BillingMovie, BillingProduct, BillingProductMoviePair


def movie_converter(movies: list[AdminPanelMovie]) -> list[BillingMovie]:
    """
    Конвертирование данных в формат хранения эластика
    :param movies: Список произвдений из БД
    :return: Список произведение формата эластика
    """
    try:
        converted_data = [
            BillingMovie(
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


def product_converter(products: list[AdminPanelProduct]) -> list[BillingProduct]:
    """
    Конвертирование данных в формат хранения эластика
    :param products: Список произвдений из БД
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
            for product in products
        ]
    except Exception as error:
        logger.exception("Ошибка валидации данных\n%s", error)
        raise error
    logger.debug(f"Сконвертировано записей - %s", {len(converted_data)})
    return converted_data


def product_movie_pair_converter(
    product_movie_pairs: list[AdminPanelProductMoviePair],
) -> list[BillingProductMoviePair]:
    """
    Конвертирование данных в формат хранения эластика
    :param product_movie_pairs: Список произвдений из БД
    :return: Список произведение формата эластика
    """
    try:
        converted_data = [
            BillingProductMoviePair(
                id=product_movie_pair.id,
                product_id=product_movie_pair.product_id,
                movie_id=product_movie_pair.filmwork_id,
            )
            for product_movie_pair in product_movie_pairs
        ]
    except Exception as error:
        logger.exception("Ошибка валидации данных\n%s", error)
        raise error
    logger.debug(f"Сконвертировано записей - %s", {len(converted_data)})
    return converted_data
