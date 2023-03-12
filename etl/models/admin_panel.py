from pydantic import BaseModel
import datetime


class AdminPanelMovies(BaseModel):
    """
    Модель фильмов для запроса в бд постгреса
    """

    id: str
    title: str
    description: str = None
    created_at: datetime.datetime
    updated_at: datetime.datetime


class AdminPanelProduct(BaseModel):
    """
    Модель фильмов для запроса в бд постгреса
    """

    id: str
    name: str
    price: int
    duration: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
