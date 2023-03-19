import logging

from models.admin_panel import AdminPanelMovie, AdminPanelProduct, AdminPanelProductMoviePair
from models.billing import BillingMovie, BillingProduct, BillingProductMoviePair


def movie_converter(movies: list[AdminPanelMovie]) -> list[BillingMovie]:
    """
    Конвертирование данных в формат хранения биллинга
    :param movies: Список фильмов из панели администратора
    :return: фильмов произведение формата биллинга
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
        logging.exception("Ошибка валидации данных\n%s", error)
        raise error
    logging.debug(f"Сконвертировано записей - %s", {len(converted_data)})
    return converted_data


def product_converter(products: list[AdminPanelProduct]) -> list[BillingProduct]:
    """
    Конвертирование данных в формат хранения биллинга
    :param products: Список продуктов из панели администратора
    :return: Список продуктов формата биллинга
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
        logging.exception("Ошибка валидации данных\n%s", error)
        raise error
    logging.debug(f"Сконвертировано записей - %s", {len(converted_data)})
    return converted_data


def product_movie_pair_converter(
    product_movie_pairs: list[AdminPanelProductMoviePair],
) -> list[BillingProductMoviePair]:
    """
    Конвертирование данных в формат хранения биллинга
    :param product_movie_pairs: Список соответствий фильмов и продуктов из панели администратора
    :return: Список соответствий фильмов и продуктов формата биллинга
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
        logging.exception("Ошибка валидации данных\n%s", error)
        raise error
    logging.debug(f"Сконвертировано записей - %s", {len(converted_data)})
    return converted_data
