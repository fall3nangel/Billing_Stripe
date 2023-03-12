import json
from datetime import date, datetime
from http import HTTPStatus

import aiohttp
from fastapi import APIRouter, Body, Depends, Request
from fastapi_pagination import Page

from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy import select

from auth.auth_bearer import auth
from db.postgres import get_db, get_db_service
from models.payment import Payment
from services.db import DBService

from .schemas import (
    InvoiceResponse,
    PaymentRequest,
    PaymentResponse,
    ProductRequest,
    ProductResponse,
    PaymentToExternalRequest,
    DelPaymentToExternalRequest
)

from core.config import settings

router = APIRouter()


@router.post(
    "/add-product",
    responses={
        int(HTTPStatus.CREATED): {
            "model": ProductResponse,
            "description": "Successful Response",
        },
    },
    summary="Покупка продукта(подписки) пользователем",
    description="При покупке подписки выставляется счет на оплату, который передается в платежную систему",
    tags=["billing"],
    dependencies=[Depends(auth)],
)
async def add_product(
    request: Request,
    data: ProductRequest = Body(default=None),
    db: DBService = Depends(get_db_service),
) -> ProductResponse:
    user_id = request.state.user_id
    # user_id = "3fa85f64-5717-4562-b3fc-1c963f66afa6"
    # data.id = "3fa85f64-5717-4562-b3fc-2c963f66afa6"

    # добавление подписки в профиль пользователя
    await db.add_product_to_user(str(data.id), user_id)

    # выставление счета на оплату
    await db.add_invoice_by_product(user_id, str(data.id))

    # получение подписки
    product = await db.get_product(str(data.id))

    # получение счета на оплату
    invoice = await db.get_last_invoice_by_user(user_id, str(data.id))

    # получение профиля пользователя
    user = await db.get_user(user_id)

    # запрос на оплату для передачи в платежную систему
    pay_req = PaymentToExternalRequest(amount=getattr(product, "price"), currency="RUB",
                                   user_id=user_id, user_name=getattr(user, "fullname"),
                                   product_name=getattr(product, "name"), email=getattr(user, "email"))
    # todo url to payAPI from env
    status = await task(
        settings.users_app.create_pay_url,
        pay_req.__dict__,
    )
    return ProductResponse(
        id=getattr(product, "id"),
        name=getattr(product, "name"),
        fd=getattr(invoice, "start_date"),
        td=getattr(invoice, "finish_date"),
        status=status,
    )


@router.delete(
    "/del-product",
    responses={
        int(HTTPStatus.CREATED): {
            "model": None,
            "description": "Successful Response",
        },
    },
    summary="Отказ от подписки",
    description="Отказ пользователя от подписки",
    tags=["billing"],
    dependencies=[Depends(auth)],
)
async def del_product(
    request: Request,
    data: ProductRequest = Body(default=None),
    db: DBService = Depends(get_db_service),
) -> None:
    user_id = request.state.user_id
    # user_id = "3fa85f64-5717-4562-b3fc-1c963f66afa6"
    # data.id = "3fa85f64-5717-4562-b3fc-2c963f66afa6"

    # удаление подписки из профиля пользователя
    await db.del_product_from_user(str(data.id), user_id)


@router.post(
    "/add-payment",
    responses={
        int(HTTPStatus.CREATED): {
            "model": PaymentResponse,
            "description": "Successful Response",
        },
    },
    summary="Добавление платежа",
    description="Добавление платежа",
    tags=["billing"],
    dependencies=[Depends(auth)],
)
async def add_payment(
    request: Request,
    data: PaymentRequest = Body(default=None),
    db: DBService = Depends(get_db_service),
) -> PaymentResponse:
    user_id = request.state.user_id
    # user_id = "3fa85f64-5717-4562-b3fc-1c963f66afa6"
    # data.id = "3fa85f64-5717-4562-b3fc-2c963f66afa6"

    # добавление записи в таблицу платежей
    payment = await db.add_payment_to_user(
        user_id, data.amount, data.currency, data.pay_date
    )
    return PaymentResponse(
        id=getattr(payment, "id"),
        desription=getattr(payment, "description"),
        amount=getattr(payment, "amount"),
        currency=getattr(payment, "currency"),
        pay_date=getattr(payment, "pay_date"),
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
    tags=["billing"],
    dependencies=[Depends(auth)],
)
async def cancel_payment(
    request: Request,
    data: PaymentRequest = Body(default=None),
    db: DBService = Depends(get_db_service),
) -> None:
    # data.id = "3fa85f64-5717-4562-b3fc-2c963f66afa6"

    # удаление платежа
    pay_req = DelPaymentToExternalRequest(id=data.id)
    status = await task(
        settings.users_app.cancel_pay_url,
        pay_req.__dict__,
    )

    # удаление записи из таблицы платежей
    await db.del_payment(str(data.id))


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
    tags=["billing"],
    # dependencies=[Depends(auth)],
)
async def create_invoice(
    user_id: str,
) -> InvoiceResponse:
    pass


@router.get(
    "/payments/{fd}/{td}",
    responses={
        int(HTTPStatus.OK): {
            "model": Page[PaymentResponse],
            "description": "Successful Response",
        },
    },
    summary="Получение выписки платежей",
    description="Получение выписки платежей за период с пагинацией",
    tags=["billing"],
    dependencies=[Depends(auth)],
)
async def get_payments(
    fd: date,
    td: date,
    request: Request,
    conn=Depends(get_db)
) -> Page[PaymentResponse]:
    user_id = request.state.user_id
    #user_id = "3fa85f64-5717-4562-b3fc-1c963f66afa6"

    # запрос на получение платежей
    query = (
        select(Payment).filter(Payment.pay_date >= fd).filter(Payment.pay_date <= td)
    )
    return await paginate(conn, query)


"""
@router.post(
    "/test",
    responses={
        int(HTTPStatus.CREATED): {
            "model": bool,
            "description": "Successful Response",
        },
    },
    summary="Test",
    description="Test",
    tags=["billing"],
    # dependencies=[Depends(auth)],
)
async def test(
    data: PaymentRequest = Body(default=None),
) -> bool:
    pay = PaymentToExternalRequest(id="3fa85f64-5717-4562-b3fc-1c963f66afa6", amount=100, currency="RUB", user_id="3fa85f64-5717-4562-b3fc-1c963f66afa6", user_name="ivanov", product_name="test", email="ivanov@test.com")
    return True
"""

async def request(session, url: str, data: dict):
    async with session.post(url, json=data) as response:
        return await response.text()


async def task(url: str, data: dict) -> dict:
    async with aiohttp.ClientSession() as session:
        task = request(session, url, data)
        result = await task
        return result
