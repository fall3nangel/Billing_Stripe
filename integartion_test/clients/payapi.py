import json
import logging
from datetime import datetime, date

import backoff
import httpx
from sqlalchemy.dialects.postgresql import UUID


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

    def _send_get(self, query: str, await_result: httpx.codes):
        result = httpx.get(f"{self.url}{query}", headers=self.headers)
        if result.status_code != await_result:
            self.last_error = f"Выполнение запроса привело к неожидаемому статусу {result.status_code}"
            return True, ""
        logging.debug("%s", result.json())
        return False, result.json()

    def _send_post(self, query: str, await_result: httpx.codes, **kwargs):
        result = httpx.post(f"{self.url}{query}", headers=self.headers, **kwargs)
        if result.status_code != await_result:
            self.last_error = f"Выполнение запроса привело к неожидаемому статусу {result.status_code}"
            return True, ""
        logging.debug("%s", result.json())
        return False, result.json()
