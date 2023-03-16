import json
import logging
import uuid
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
    RefundPaymentToExternalRequest,
)

from core.config import settings

router = APIRouter()


@router.post(
    "/add-product/{product_id}",
    status_code=HTTPStatus.CREATED,
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
    product_id: str,
    db: DBService = Depends(get_db_service),
) -> ProductResponse:
    user_id = request.state.user_id
    # user_id = "3fa85f64-5717-4562-b3fc-1c963f66afa6"
    # data.id = "3fa85f64-5717-4562-b3fc-2c963f66afa6"

    # добавление подписки в профиль пользователя
    await db.add_product_to_user(product_id, user_id)

    # выставление счета на оплату
    await db.add_invoice_by_product(user_id, product_id)

    # получение подписки
    product = await db.get_product(product_id)
    price = getattr(product, "price")
    product_name = getattr(product, "name")
    product_id = getattr(product, "id")
    duration = getattr(product, "duration")

    # получение счета на оплату
    # invoice = await db.get_last_invoice_by_user(user_id, product_id)

    # получение профиля пользователя
    user = await db.get_user(user_id)
    fullname = getattr(user, "fullname")
    email = getattr(user, "email")

    # добавление записи в таблицу платежей
    payment_id = uuid.uuid4()
    await db.add_payment_to_user(payment_id, user_id, price, "RUB", None)

    # запрос на оплату для передачи в платежную систему
    pay_req = PaymentToExternalRequest(
        order_id=payment_id,
        amount=price,
        currency="RUB",
        user_id=user_id,
        user_name=fullname,
        product_name=product_name,
        email=email,
    )

    resp = await task(
        f"{settings.paymentservice.url}/create-checkout-session",
        pay_req.__dict__,
    )
    # logging.info(json.loads(resp)["url"])
    return ProductResponse(
        id=product_id,
        name=product_name,
        price=price,
        duration=duration,
        url=json.loads(resp)["url"]
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
    # dependencies=[Depends(auth)],
)
async def add_payment(
    # request: Request,
    data: PaymentRequest = Body(default=None),
    db: DBService = Depends(get_db_service),
) -> PaymentResponse:
    # user_id = request.state.user_id

    # добавление записи в таблицу платежей
    # payment = await db.add_payment_to_user(data.user_id, data.amount, data.currency, data.pay_date)

    # получение платежа
    payment = await db.get_payment(data.order_id)
    payment_id = getattr(payment, "id")
    currency = getattr(payment, "currency")
    amount = getattr(payment, "amount")
    description = getattr(payment, "description")

    pay_date = datetime.now()

    # обновление платежа
    await db.update_payment(data.order_id, pay_date, data.payment_intent_id)

    return PaymentResponse(
        id=payment_id,
        description=description,
        amount=amount,
        currency=currency,
        pay_date=pay_date,
    )


@router.delete(
    "/cancel-payment/{payment_id}",
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
    payment_id: str,
    db: DBService = Depends(get_db_service),
) -> None:
    # data.id = "3fa85f64-5717-4562-b3fc-2c963f66afa6"

    # получение платежа
    payment = await db.get_payment(payment_id)

    # удаление платежа
    pay_req = RefundPaymentToExternalRequest(payment_intent_id=getattr(payment, "payment_intent_id"))
    status = await task(
        f"{settings.paymentservice.url}/refund",
        pay_req.__dict__,
    )

    # удаление записи из таблицы платежей
    await db.del_payment(payment_id)


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
async def get_payments(fd: date, td: date, request: Request, conn=Depends(get_db)) -> Page[PaymentResponse]:
    user_id = request.state.user_id
    # user_id = "3fa85f64-5717-4562-b3fc-1c963f66afa6"

    # запрос на получение платежей
    query = select(Payment).filter(Payment.pay_date >= fd).filter(Payment.pay_date <= td)
    return await paginate(conn, query)


@router.get(
    "/products",
    responses={
        int(HTTPStatus.OK): {
            "model": list[ProductResponse],
            "description": "Successful Response",
        },
    },
    summary="Получение списка подписок",
    description="Получение списка подписок",
    tags=["billing"],
    dependencies=[Depends(auth)],
)
async def get_products(
    request: Request,
    db: DBService = Depends(get_db_service),
) -> list[ProductResponse]:
    user_id = request.state.user_id
    # user_id = "3fa85f64-5717-4562-b3fc-1c963f66afa6"
    products = await db.get_all_products()

    return [
        ProductResponse(
            id=p.id,
            name=p.name,
            price=p.price,
            duration=p.duration,
        )
        for p in products
    ]


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
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    async with session.post(url, json=data, headers=headers) as response:
        return await response.text()


async def task(url: str, data: dict) -> dict:
    async with aiohttp.ClientSession() as session:
        logging.debug("%s\n%s", url, data)
        result = await request(session, url, data)
        logging.debug("%s", result)
        return result
