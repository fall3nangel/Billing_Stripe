import uuid
import aiohttp
import asyncio
from http import HTTPStatus
from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from auth.auth_bearer import auth
from auth.auth_handler import encode_jwt
from .schemas import InvoiceResponse, PaymentRequest, PaymentResponse

from db.postgres import get_db_service
from services.db import DBService


router = APIRouter()


@router.get(
    "/test-invoice/{inv_id}",
    responses={
        int(HTTPStatus.OK): {
            "model": InvoiceResponse,
            "description": "Successful Response",
        },
    },
    summary="Счет на оплату",
    description="Счет на оплату подписки с учетом скидки и активных купонов",
    tags=["invoices"],
    # dependencies=[Depends(auth)],
)
async def get_invoice(
    inv_id: str,
) -> InvoiceResponse:
    return InvoiceResponse(
        id=str(inv_id),
        cost=1000
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
    tags=["invoices"],
    # dependencies=[Depends(auth)],
)
async def make_payment(
    data: PaymentRequest = Body(default=None),
) -> PaymentResponse:
    user_id = "ivanov"
    url: str = f"http://0.0.0.0:8000/api/v1/payments/make-payment/{user_id}"
    await task(url)
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
    tags=["invoices"],
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
    tags=["invoices"],
    # dependencies=[Depends(auth)],
)
async def create_invoice(
    user_id: str,
) -> InvoiceResponse:

    return InvoiceResponse(
        id=str(user_id),
        cost=1000
    )

async def request(session, url: str):
    async with session.get(url) as response:
        return await response.text()

async def task(url: str):
    async with aiohttp.ClientSession() as session:
        task = request(session, url)
        result = await asyncio.gather(task)
        print(result)