import uuid
from http import HTTPStatus
from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from auth.auth_bearer import auth
from auth.auth_handler import encode_jwt
from .schemas import InvoiceResponse, PaymentRequest, PaymentResponse, UserRequest, UserResponse

from db.postgres import get_db_service
from services.db import DBService

router = APIRouter()

@router.get(
    "/login",
    response_model=None,
    summary="",
    description="",
    response_description="",
)
async def get_access_token(user_id: str | None = None) -> str:
    if not user_id:
        user_id = str(uuid.uuid4())
    token: str = encode_jwt(user_id)
    return token

@router.get(
    "/invoice",
    responses={
        int(HTTPStatus.OK): {
            "model": InvoiceResponse,
            "description": "Successful Response",
        },
    },
    summary="Счет на оплату",
    description="Счет на оплату подписки с учетом скидки и активных купонов",
    tags=["users"],
    dependencies=[Depends(auth)],
)
async def get_invoice(
    sub_id: str,
) -> InvoiceResponse:
    return InvoiceResponse(
        id=str(sub_id),
        cost=1000
    )


@router.post(
    "/add-user",
    responses={
        int(HTTPStatus.CREATED): {
            "model": UserResponse,
            "description": "Successful Response",
        },
    },
    summary="Создание пользователя",
    description="Создание пользователя",
    tags=["users"],
)
async def add_user(
    data: UserRequest = Body(default=None),
    db: DBService = Depends(get_db_service),
) -> UserResponse:
    await db.add_user(login=data.login,
            password=data.password,
            email=data.email,
            fullname=data.fullname,
            phone=data.phone,
            subscribed=False
    )
    user = await db.get_user_by_login(data.login)
    return UserResponse(
        id=str(user.id),
        login=user.login,
        fullname=user.fullname,
        email=user.email,
        phone=user.phone,
        allow_send_email=user.allow_send_email,
        confirmed_email=user.confirmed_email,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )

@router.get(
    "/user",
    responses={
        int(HTTPStatus.OK): {
            "model": UserResponse,
            "description": "Successful Response",
        },
    },
    summary="",
    description="",
    tags=["users"],
)
async def get_user(
    user_id: str,
    db: DBService = Depends(get_db_service)
) -> UserResponse:
    user = await db.get_user_by_login(user_id)
    return UserResponse(
        id=str(user.id),
        login=user.login,
        fullname=user.fullname,
        email=user.email,
        phone=user.phone,
        allow_send_email=user.allow_send_email,
        confirmed_email=user.confirmed_email,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )

@router.post(
    "/make-payment",
    responses={
        int(HTTPStatus.CREATED): {
            "model": PaymentResponse,
            "description": "Successful Response",
        },
    },
    summary="Запрос на совершение платежа",
    description="Совершение платежа по выставленному счету на оплату",
    tags=["users"],
    dependencies=[Depends(auth)],
)
async def make_payment(
    data: PaymentRequest = Body(default=None),
) -> PaymentResponse:

    return PaymentResponse(
        id=str(data.id),
        accesss_token="",
        refresh_token="",
    )


@router.get(
    "/payment",
    responses={
        int(HTTPStatus.OK): {
            "model": PaymentResponse,
            "description": "Successful Response",
        },
    },
    summary="Счет на оплату",
    description="Счет на оплату подписки с учетом скидки и активных купонов",
    tags=["users"],
    dependencies=[Depends(auth)],
)
async def get_payment(
    pay_id: str,
) -> PaymentResponse:
    return PaymentResponse(
        id=str(pay_id),
        cost=1000
    )


@router.post(
    "/cancel-payment",
    responses={
        int(HTTPStatus.CREATED): {
            "model": PaymentResponse,
            "description": "Successful Response",
        },
    },
    summary="Отмена платежа",
    description="Отмена платежа",
    tags=["users"],
    dependencies=[Depends(auth)],
)
async def cancel_payment(
    data: PaymentRequest = Body(default=None),
) -> PaymentResponse:

    return PaymentResponse(
        id=str(data.id),
        accesss_token="",
        refresh_token="",
    )

@router.post(
    "/invoice",
    responses={
        int(HTTPStatus.CREATED): {
            "model": InvoiceResponse,
            "description": "Successful Response",
        },
    },
    summary="Периодический счет на оплату",
    description="Периодический счет на оплату подписки с учетом скидки и активных купонов",
    tags=["users"],
    dependencies=[Depends(auth)],
)
async def get_invoice(
    user_id: str,
) -> InvoiceResponse:
    return InvoiceResponse(
        id=str(user_id),
        cost=1000
    )