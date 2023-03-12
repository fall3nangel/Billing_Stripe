from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from models.payment import Currency


class ProductRequest(BaseModel):
    id: UUID
    fd: datetime
    td: datetime | None = None


class ProductResponse(BaseModel):
    id: UUID
    name: str
    fd: datetime
    td: datetime | None = None
    status: str


class InvoiceResponse(BaseModel):
    id: str
    cost: int


class PaymentToExternalRequest(BaseModel):
    amount: int
    currency: str
    user_id: str
    user_name: str
    email: str
    product_name: str

class DelPaymentToExternalRequest(BaseModel):
    id: UUID


class PaymentRequest(BaseModel):
    id: UUID
    amount: int
    currency: str
    pay_date: datetime


class PaymentResponse(BaseModel):
    id: UUID
    description: str
    amount: int
    currency: Currency
    pay_date: datetime

    class Config:
        orm_mode = True


class UserRequest(BaseModel):
    login: str
    fullname: str | None = None
    password: str | None = None
    email: str
    phone: str | None = None


class UserResponse(BaseModel):
    id: str
    login: str
    fullname: str | None = None
    email: str
    phone: str | None = None
    allow_send_email: bool
    confirmed_email: bool
    created_at: datetime
    updated_at: datetime
