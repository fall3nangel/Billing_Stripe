from models.product import Product
import allure
from allure import step


def test_1(db_session, initial_data, billing_client):
    product, movies = initial_data
    with step("Получение списка доступных продуктов"):
        assert billing_client.get_products(), billing_client.last_error
        assert len(billing_client.last_json), "Ожидается один продукт"
        subscribed_product = billing_client.last_json[0]
        print(subscribed_product)

    with step("Проверка отсутствия прав у пользователя на просмотр фильма"):
        assert billing_client.get_rights(movie_id=movies[0].id), billing_client.last_error
        assert not billing_client.last_json['allow']

    with step("Запрос пользователем на покупку подписки"):
        assert billing_client.add_product_to_user(
            product_id=subscribed_product['id']
        ), billing_client.last_error
        print(billing_client.last_json)

    with step("Проверка отсутствия прав у пользователя на просмотр фильма после оформления подписки"):
        assert billing_client.get_rights(movie_id=movies[0].id), billing_client.last_error
        assert not billing_client.last_json['allow']

    '''with step("Отмена платежа"):
        payments = billing_client.get_payments()
        print(billing_client.last_json)
        assert billing_client.cancel_payment(payment_id=payments[0].id), billing_client.last_error
    '''
    return
