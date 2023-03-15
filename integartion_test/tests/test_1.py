from models.product import Product
import allure
from allure import step

def test_1(db_session, initial_data, billing_client):
    product, movies = initial_data
    with step("Проверка отсутствия прав у пользователя на просмотр фильма"):
        assert not billing_client.allow_watching_movie(movie_id=movies[0].id), billing_client.last_error
    with step("Запрос пользователем на покупку подписки"):
        assert billing_client.add_product_to_user(product_id=product.id), billing_client.last_error

    return
