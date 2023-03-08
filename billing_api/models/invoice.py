import uuid

from sqlalchemy import Column, String, DateTime, DECIMAL
from sqlalchemy.dialects.postgresql import UUID

from db.postgres import Base


class Invoice(Base):
    __tablename__ = "invoice"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    id_product = Column(UUID(as_uuid=True), nullable=False)
    id_user = Column(UUID(as_uuid=True), nullable=False)
    description = Column(String, unique=True, nullable=False)
    price = Column(DECIMAL(10, 2))
    start_date = Column(DateTime(timezone=True), nullable=True)
    finish_date = Column(DateTime(timezone=True), nullable=True)
