import httpx


class Billing:
    def __init__(self, url):
        self.user_access_token = None
        self.url = f"{url}/api/v1"
        self.headers = {"accept": "*/*", "Content-Type": "application/json"}
        self.last_error = None

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
        self.user_access_token = data['access_token']
        return True

    def get_test_user_token(self):
        if not self.user_access_token:
            raise Exception("Токен пользователя не заполнен")
        return self.user_access_token
