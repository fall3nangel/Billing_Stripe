import base64
import json
import logging
from enum import Enum
from pathlib import Path

import requests

REQUEST_TIMEOUT: int = 10
SEND_TIMEOUT: int = 300

logger = logging.getLogger("allure_report_push")


class AllureReportPush(object):
    def __init__(
        self,
        url: str,
        reports_dir: Path,
        project_name: str = "default",
        clean_project: bool = False,
        generate_reports: bool = False,
    ):
        # Инициализация переменных
        self.allure_reports_dir = reports_dir
        self.allure_project_id = project_name
        self.allure_clean_project = clean_project
        self.last_error: str = ""
        self.allure_api_url: str = f"{url}/allure-docker-service"
        self.allure_generate_reports = generate_reports
        self.url_project = f"{url}/allure-docker-service/projects/{project_name}/reports/latest/index.html"

    def check_connect(self) -> bool:
        """
        Возвращает отрицательный результат если API Allure не доступен или возвращает неверный ответ
        @return: bool
        """
        request: str = f"{self.allure_api_url}/projects/{self.allure_project_id}"
        # Отправляется запрос на сервер и проверяется на ошибки
        try:
            response: request = requests.get(request, timeout=REQUEST_TIMEOUT)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            logger.error(f'Ошибка запроса к API Allure "{request}", сервер не доступен ')
            return False
        if response.status_code == 200:
            return True
        # Если проекта не существует, то создаем
        if response.status_code == 404:
            create_code = self.create_project()
            # При успешном создании проекта
            if create_code == 201:
                return True
        # Логирование ошибки
        logger.error(
            f'Ошибочный ответ от API Allure: "{request}", '
            f"response: {response.status_code} "
            f"{response.content.decode(encoding='UTF-8', errors='ignore')}"
        )
        return False

    def send_reports(self) -> bool:
        """
        Функция отправляет файлы отчетов из директории, указанной при инициализации на API Allure,
        URL которого так же указывается при инициализации.

        :return: Логический резултат выполнения функции
        """
        file_data_list = self.get_files_data_list()

        if not file_data_list:
            logger.error("Нет отчетов для отправки на сервер allure")
            return False
        if self.clean_results() != 200:
            self.last_error = "Allure: Ошибка очистики результатов"
            return False

        if self.allure_clean_project:
            if self.clean_history() != 200:
                self.last_error = "Allure: Ошибка очистки истории"
                return False

        headers = {"accept": "*/*", "Content-Type": "application/json"}
        data = json.dumps({"results": file_data_list}, separators=(",", ":"))
        url: str = f"{self.allure_api_url}/send-results?project_id={self.allure_project_id}"
        response: requests = requests.post(url=url, data=data, headers=headers, timeout=SEND_TIMEOUT)
        if response.status_code != 200:
            self.last_error = f"Allure: Ошибка отправки отчётов результатов, '{response.status_code}'"
            return False

        if self.allure_generate_reports:
            if self.generate_reports() != 200:
                self.last_error = "Allure: Ошибка генерации отчетов"
                return False
        return True

    def clean_history(self) -> int:
        """
        Очистка истории отчетов на сервере Allure

        :return: Код ответа от API Allure
        """
        request = f"{self.allure_api_url}/clean-history?project_id={self.allure_project_id}"
        # Отправляется запрос на сервер и проверяется на ошибки
        response = requests.get(request, timeout=REQUEST_TIMEOUT)
        if response.status_code != 200:
            logger.error(
                f"Ошибка очистки истории отчетов в Allure API: {request}, "
                f"код ошибки {response.status_code}"
                f"{response.content.decode(encoding='UTF-8', errors='ignore')}"
            )
        return response.status_code

    def clean_results(self) -> int:
        """
        Очистка результатов теста на сервере Allure

        :return: Код ответа от API Allure
        """
        request: str = f"{self.allure_api_url}/clean-results?project_id={self.allure_project_id}"
        # Отправляется запрос на сервер и проверяется на ошибки
        response = requests.get(request, timeout=REQUEST_TIMEOUT)
        if response.status_code != 200:
            logger.error(
                f"Ошибка очистки отчетов Allure API: {request}, "
                f"код ошибки {response.status_code} "
                f"{response.content.decode(encoding='UTF-8', errors='ignore')}"
            )
        return response.status_code

    def create_project(self) -> int:
        """
        Запрос для создания проекта

        :return: Код ответа от API Allure
        """
        headers = {"accept": "*/*", "Content-Type": "application/json"}
        data = json.dumps({"id": self.allure_project_id}, separators=(",", ":"))
        # Посылаем запрос на сервер
        request: str = f"{self.allure_api_url}/projects"
        response = requests.post(request, headers=headers, data=data, timeout=REQUEST_TIMEOUT)
        if response.status_code != 201:
            logger.error(
                f"Ошибка создания проекта: {request}, "
                f"код ошибки {response.status_code} "
                f"{response.content.decode(encoding='UTF-8', errors='ignore')}"
            )
        return response.status_code

    def generate_reports(self) -> int:
        """
        Запрос для генерации отчета

        :return: Код ответа от API Allure
        """
        request: str = f"{self.allure_api_url}/generate-report?project_id={self.allure_project_id}"
        # Отправляется запрос на сервер и проверяется на ошибки
        response = requests.get(request, timeout=SEND_TIMEOUT)
        if response.status_code != 200:
            logger.error(
                f"Ошибка очистки отчетов Allure API: {request}, "
                f"код ошибки {response.status_code} "
                f"{response.content.decode(encoding='UTF-8', errors='ignore')}"
            )
        return response.status_code

    def send_file(self, file_name: str, content_base64: str) -> int:
        """
        Отправка на сервер аллюра содержимого файла
        :return: Код ответа от API Allure
        """
        # Формируем данные для запроса
        headers = {"accept": "*/*", "Content-Type": "application/json"}
        file_data: dict = {"file_name": file_name, "content_base64": content_base64}
        data = json.dumps({"results": [file_data]}, separators=(",", ":"))
        # Формируем запрос
        request: str = f"{self.allure_api_url}/send-results?project_id={self.allure_project_id}"
        # Посылаем запрос на сервер
        response = requests.post(request, headers=headers, data=data, timeout=SEND_TIMEOUT)
        if response.status_code != 200:
            logger.error(
                f'Ошибка отправки файла в Allure API: "{self.allure_api_url}", '
                f'код ошибки: "{response.status_code}", '
                f"{response.content.decode(encoding='UTF-8', errors='ignore')}"
            )
        return response.status_code

    def get_files_data_list(self) -> list:
        """
        Получить из папки с отчетами все файлы, подготовить для отправки на сервер
        :return: Список с содержимым файлов из директории отчетов в формате base64
        """
        # Формируем данные для запроса
        file_data_list: list = []
        # Пробегаемся по всем элементам директории из которой необходимо отправить файлы
        for file_name in self.allure_reports_dir.iterdir():
            file_path = self.allure_reports_dir / file_name
            # Если объект не является файлом, то такой объект прикладывать не надо, его следует пропустить
            if not file_path.is_file():
                continue
            # Открываем файл для чтения
            try:
                with open(file_path, "rb") as file_report:
                    content = file_report.read()
                    # Если файл нулевого размера, то пропускаем
                    if not content.strip():
                        continue
                    # Собираем json и прикладываем к списку для отправки
                    file = {"file_name": file_name.name, "content_base64": base64.b64encode(content).decode("UTF-8")}
                    file_data_list.append(file)
            finally:
                file_report.close()
        return file_data_list
