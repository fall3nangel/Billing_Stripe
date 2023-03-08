from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class InvoiceResponse(BaseModel):
    id: str
    cost: int


class PaymentRequest(BaseModel):
    id: UUID


class PaymentResponse(BaseModel):
    id: UUID
    access_token: str
    refresh_token: str


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