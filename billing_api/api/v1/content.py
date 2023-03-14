import uuid
from http import HTTPStatus

from fastapi import APIRouter, Body, Depends, HTTPException, Request

from auth.auth_bearer import auth
from auth.auth_handler import encode_jwt
from db.postgres import get_db_service
from services.db import DBService

from fastapi.exceptions import HTTPException
from http import HTTPStatus
from db.postgres import get_db, get_db_service
from services.db import DBService

from .schemas import (
    UserRequest
)

router = APIRouter()


@router.get(
    "/get-token",
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


@router.get(
    "/check-rights/{movie_id}",
    responses={
        int(HTTPStatus.OK): {
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


@router.post(
    "/register",
    response_model=None,
    summary="Регистрация пользователя",
    description="Регистрация пользователя",
    tags=["content"],
)
async def register(
    data: UserRequest = Body(default=None),
    db: DBService = Depends(get_db_service)
) -> str:
    user = await db.get_user_by_login(data.login)
    if user and data.login == user.login:
        raise HTTPException(HTTPStatus.BAD_REQUEST, detail="login exists")
    if len(data.password) < 6:
        raise HTTPException(HTTPStatus.BAD_REQUEST, detail="password error")
    await db.add_user(data.login, data.password, data.email, data.fullname, data.phone)

    new_user = await db.get_user_by_login(data.login)
    if new_user:
        token: str = encode_jwt(new_user.id)
        return token
    else:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, detail="user error")

@router.post(
    "/login",
    response_model=None,
    summary="Вход пользователя",
    description="Вход пользователя",
    tags=["content"],
)
async def login(
    data: UserRequest = Body(default=None),
    db: DBService = Depends(get_db_service)
) -> str:
    if not data.login and not data.password:
        raise HTTPException(HTTPStatus.BAD_REQUEST, detail="login error")
    user = await db.get_user_by_login(data.login)
    if not user:
        raise HTTPException(HTTPStatus.BAD_REQUEST, detail="login not exists")
    else:
        if user.check_password(data.password):
            token: str = encode_jwt(user.id)
            return token
        else:
            raise HTTPException(HTTPStatus.BAD_REQUEST, detail="password error")