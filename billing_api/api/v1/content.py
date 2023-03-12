import uuid
from http import HTTPStatus

from fastapi import APIRouter, Body, Depends, HTTPException, Request

from auth.auth_bearer import auth
from auth.auth_handler import encode_jwt
from db.postgres import get_db_service
from services.db import DBService

router = APIRouter()


@router.get(
    "/login",
    response_model=None,
    summary="Получение токена на доступ к API",
    description="Получение токена на доступ к API",
    tags=["content"],
)
async def get_access_token(user_id: str | None = None) -> str:
    if not user_id:
        user_id = str(uuid.uuid4())
    token: str = encode_jwt(user_id)
    return token


@router.post(
    "/check-rights/{movie_id}",
    responses={
        int(HTTPStatus.CREATED): {
            "model": bool,
            "description": "Successful Response",
        },
    },
    summary="Проверка прав на просмотр фильма",
    description="Проверка прав на просмотр фильма",
    tags=["content"],
    dependencies=[Depends(auth)],
)
async def check_rights(
    movie_id: str, request: Request, db: DBService = Depends(get_db_service)
) -> bool:
    user_id = request.state.user_id
    # user_id = "3fa85f64-5717-4562-b3fc-1c963f66afa6"
    product = await db.get_product_by_movie(str(movie_id))
    product_id = getattr(product, "id")
    return await db.check_payment(user_id, str(product_id))
