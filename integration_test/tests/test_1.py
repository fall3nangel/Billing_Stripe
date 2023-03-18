import time

from models.product import Product
import allure
from allure import step


def test_1(db_session, initial_data, billing_client, send_telegram_notify):
    product, movies = initial_data
    with step("Получение списка доступных продуктов"):
        assert billing_client.get_products(), billing_client.last_error
        assert len(billing_client.last_json), "Ожидается один продукт"
        subscribed_product = billing_client.last_json[0]
        print(subscribed_product)

    with step("Проверка отсутствия прав у пользователя на просмотр фильма"):
        assert billing_client.get_rights(movie_id=movies[0].id), billing_client.last_error
        assert not billing_client.last_json['allow'], "Нет прав"

    with step("Запрос пользователем на покупку подписки"):
        assert billing_client.add_product_to_user(
            product_id=subscribed_product['id']
        ), billing_client.last_error
        print(billing_client.last_json)
        checkout_url = billing_client.last_json['url']

    with step("Проверка отсутствия прав у пользователя на просмотр фильма после оформления подписки"):
        assert billing_client.get_rights(movie_id=movies[0].id), billing_client.last_error
        assert not billing_client.last_json['allow']

    with step("Ожидание оплаты подписки пользователем в течении 2-х минут"):
        #send_telegram_notify(f"Оплату необходимо произвести по ссылке\n{checkout_url}")
        print(f"Оплату необходимо произвести по ссылке {checkout_url}")
        start_time = time.time()
        while time.time() < start_time + 120:
            billing_client.get_payments()
            print(billing_client.last_json)
            if billing_client.last_json['items']:
                return
            time.sleep(10)
        else:
            assert False, "За две минуты не было получено подтверждение об оплате"




    '''with step("Отмена платежа"):
        payments = billing_client.get_payments()
        print(billing_client.last_json)
        assert billing_client.cancel_payment(payment_id=payments[0].id), billing_client.last_error
    '''
    return
