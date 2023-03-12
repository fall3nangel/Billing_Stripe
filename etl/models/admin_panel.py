import datetime

from pydantic import BaseModel


class AdminPanelMovie(BaseModel):
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


class AdminPanelProductMoviePair(BaseModel):
    """
    Модель фильмов для запроса в бд постгреса
    """

    id: str
    product_id: str
    filmwork_id: str
