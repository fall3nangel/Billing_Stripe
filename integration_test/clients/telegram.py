import httpx


class TelegramReporter:
    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id
        self.url = "https://api.telegram.org/bot"
        self.headers = {"Content-Type": "application/json"}

    def send_notify(self, message):
        httpx.post(
            f"{self.url}{self.token}/sendMessage",
            json=dict(
                chat_id=self.chat_id,
                text=message,
            ),
            headers=self.headers,
        )
