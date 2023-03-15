import logging
from enum import Enum

import backoff
import httpx


class SendType(Enum):
    post = httpx.post
    get = httpx.get


class Billing:
    def __init__(self, url):
        self.url = f"{url}/api/v1"
        self.headers = {"accept": "*/*", "Content-Type": "application/json"}
        self.last_error = None
        self.last_json = None
        self.allow_watching = None

    @backoff.on_exception(backoff.expo, httpx.ReadError)
    def create_test_user(self):
        result = httpx.post(
            f"{self.url}/content/register",
            json=dict(
                login="test_user_1",
                fullname="fullname",
                password="password",
                email="mail@example.com",
                phone="+77777777777",
            ),
            headers=self.headers,
        )
        if result.status_code != httpx.codes.OK:
            self.last_error = f"Выполнение запроса привело к ошибке {result.status_code}"
            return False
        data = result.json()
        if "access_token" not in data:
            self.last_error = "Не обнаружено поле 'access_token' в ответе"
            return False
        self.headers["Authorization"] = f"Bearer {data['access_token']}"
        return True

    def _send(self, query: str, await_result: httpx.codes, send_type: SendType, **kwargs):
        result = send_type(f"{self.url}{query}", headers=self.headers, **kwargs)
        if result.status_code != await_result:
            self.last_error = f"Выполнение запроса привело к неожидаемому статусу {result.status_code}"
            return True, ""
        logging.debug("%s", result.json())
        return False, result.json()

    def get_rights(self, movie_id: str):
        error, self.last_json = self._send(
            query=f"/content/check-rights/{movie_id}",
            send_type=SendType.post,
            await_result=httpx.codes.OK,
        )
        if error:
            return False
        return True

    def get_products(self):
        error, self.last_json = self._send(
            query="/billing/products",
            send_type=SendType.get,
            await_result=httpx.codes.OK,
        )
        if error:
            return False
        return True

    def add_product_to_user(self, product_id: str):
        error, self.last_json = self._send(
            query="/billing/add-product",
            send_type=SendType.post,
            await_result=httpx.codes.CREATED,
            json=dict(
                id=product_id,
            ),
        )
        if error:
            return False
        if "id" not in self.last_json and "name" not in self.last_json:
            self.last_error = "Отсутствуют необходимые поля"
            return False
        return True