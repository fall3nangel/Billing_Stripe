import json
import logging
from datetime import datetime, date

import backoff
import httpx
from sqlalchemy.dialects.postgresql import UUID


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()

    if isinstance(obj, UUID):
        # if the obj is uuid, we simply return the value of uuid
        return obj.hex

    raise TypeError("Type %s not serializable" % type(obj))

class Billing:
    def __init__(self, url):
        self.url = f"{url}/api/v1"
        self.headers = {"accept": "*/*", "Content-Type": "application/json"}
        self.last_error = None

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
        if 'access_token' not in data:
            self.last_error = "Не обнаружено поле 'access_token' в ответе"
            return False
        self.headers["Authorization"] = f"Bearer {data['access_token']}"
        return True

    def allow_watching_movie(self, movie_id: str):
        result = httpx.get(
            f"{self.url}/content/check-rights/{movie_id}",
            headers=self.headers,
        )
        if result.status_code != httpx.codes.OK:
            self.last_error = f"Выполнение запроса привело к ошибке {result.status_code}"
            return False
        logging.debug(result)
        data = result.content
        if not data:
            self.last_error = "Нет прав на просмотр"
            return False
        return True

    def add_product_to_user(self, product_id: str):
        result = httpx.post(
            f"{self.url}/billing/add-product/",
            json=dict(
                id=product_id,
            ),
            headers=self.headers,
        )
        if result.status_code != httpx.codes.CREATED:
            self.last_error = f"Выполнение запроса привело к ошибке {result.status_code}"
            return False
        logging.debug("%s", result)
        data = result.json()
        if 'id' not in data and 'name' in data:
            self.last_error = "Некорректный ответ"
            return False
        return True
