import uuid
import aiohttp
import json
import asyncio
from http import HTTPStatus
from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from auth.auth_bearer import auth
from auth.auth_handler import encode_jwt
from .schemas import UserRequest, UserResponse, InvoiceResponse, PaymentRequest, PaymentResponse

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


@router.post(
    "/add-product",
    responses={
        int(HTTPStatus.CREATED): {
            "model": PaymentResponse,
            "description": "Successful Response",
        },
    },
    summary="Покупка продукта(подписки) пользователем",
    description="При покупке подписки выставляется счет на оплату, который передается в платежную систему, после подтверждения оплаты пользователю добавляются права на пользование подпиской",
    tags=["billing"],
    # dependencies=[Depends(auth)],
)
async def make_payment(
    data: PaymentRequest = Body(default=None),
) -> PaymentResponse:
    return PaymentResponse(
        id=str(data.id),
        accesss_token="",
        refresh_token="",
    )

@router.delete(
    "/cancel-payment",
    responses={
        int(HTTPStatus.NO_CONTENT): {
            "model": None,
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
) -> None:
    pass

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
    # dependencies=[Depends(auth)],
)
async def create_invoice(
    user_id: str,
) -> InvoiceResponse:

    return InvoiceResponse(
        id=str(user_id),
        cost=1000
    )

@router.get(
    "/payments/{fd}/{td}",
    responses={
        int(HTTPStatus.CREATED): {
            "model": list,
            "description": "Successful Response",
        },
    },
    summary="Получение выписки платежей",
    description="Получение выписки платежей за период",
    tags=["billing"],
    # dependencies=[Depends(auth)],
)
async def get_payments(
    fd: datetime,
    td: datetime
) -> InvoiceResponse:

    return InvoiceResponse(
        id=str(user_id),
        cost=1000
    )