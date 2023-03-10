from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import async_session

from api.v1.schemas import InvoiceResponse
from db.postgres import get_db_service
from models.product import Product
from services.db import DBService

router = APIRouter()


@router.get(
    "/test-invoice/{inv_id}",

    summary="Счет на оплату",
    description="Счет на оплату подписки с учетом скидки и активных купонов",
    tags=["invoices"],
    # dependencies=[Depends(auth)],
)
async def add_invoice(
    inv_id: str,
    db: DBService = Depends(get_db_service),
):
    # async with async_session() as session:
    #     session.add(Product(dict()))
    #     await session.flush()
    #     await session.commit()
    await db.add_invoice_by_product(id_product="b163b6ff-ec24-4b1b-a575-7f35777ddd1f")
    return InvoiceResponse(
        id=str(inv_id),
        cost=1000
    )



#
#
# @router.post(
#     "/invoice",
#     responses={
#         int(HTTPStatus.CREATED): {
#             "model": InvoiceResponse,
#             "description": "Successful Response",
#         },
#     },
#     summary="Создать счет на оплату",
#     tags=["invoices"],
#     # dependencies=[Depends(auth)],
# )
# async def create_invoice(
#     user_id: str,
# ) -> InvoiceResponse:
#
#     return InvoiceResponse(
#         id=str(user_id),
#         cost=1000
#     )
