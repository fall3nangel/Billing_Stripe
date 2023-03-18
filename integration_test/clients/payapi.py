class PayApi:
    def __init__(self, url):
        self.url = f"{url}/api/v1"
        self.headers = {"accept": "*/*", "Content-Type": "application/json"}
        self.last_error = None
        self.last_json = None
        self.allow_watching = None
