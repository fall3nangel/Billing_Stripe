import json
import logging
from abc import abstractmethod
from datetime import datetime, date
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


class BaseStorage:
    @abstractmethod
    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище"""
        pass

    @abstractmethod
    def retrieve_state(self) -> dict:
        """Загрузить состояние локально из постоянного хранилища"""
        return {}


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: Path | None = None):
        self.file_path = file_path

    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище"""
        with open(self.file_path, mode="w", encoding="utf-8") as writed_file:
            json.dump(state, writed_file, ensure_ascii=False, indent=4, default=json_serial)

    def retrieve_state(self) -> dict:
        """Загрузить состояние локально из постоянного хранилища"""
        current_state = {}
        try:
            current_state = json.load(open(self.file_path, encoding="utf-8"))
        except:
            pass
        finally:
            return current_state


class State:
    """
    Класс для хранения состояния при работе с данными, чтобы постоянно не перечитывать данные с начала.
    Здесь представлена реализация с сохранением состояния в файл.
    В целом ничего не мешает поменять это поведение на работу с БД или распределённым хранилищем.
    """

    def __init__(self, storage: BaseStorage):
        self.storage = storage
        self.state = None

    def set_state(self, key: str, value: Any, use_cache=True) -> None:
        """Установить состояние для определённого ключа"""
        state = self.state
        if not state or not use_cache:
            state = self.storage.retrieve_state()
        state[key] = value
        self.storage.save_state(state)

    def get_state(self, key: str) -> Any:
        """Получить состояние по определённому ключу"""
        state = self.storage.retrieve_state()
        if key not in state:
            return None
        result = state[key]
        logging.debug("Storage key - %s: %s", key, result)
        return result
