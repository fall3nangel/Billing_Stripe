from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class InvoiceResponse(BaseModel):
    id: UUID
    cost: int


class PaymentRequest(BaseModel):
    id: UUID


class PaymentResponse(BaseModel):
    id: UUID
    access_token: str
    refresh_token: str