from pydantic import BaseModel


class BillingMovie(BaseModel):
    """
    Модель фильмов для запроса в бд постгреса
    """

    id: str
    name: str
    description: str = None


class BillingProduct(BaseModel):
    """
    Модель фильмов для запроса в бд постгреса
    """

    id: str
    name: str
    price: int
    duration: str


class BillingProductMoviePair(BaseModel):
    """
    Модель фильмов для запроса в бд постгреса
    """

    id: str
    product_id: str
    movie_id: str
