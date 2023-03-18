import uuid

from sqlalchemy import DECIMAL, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from db.postgres import Base


class Invoice(Base):
    __tablename__ = "invoice"
    __table_args__ = {"schema": "users"}
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    product_id = Column(UUID(as_uuid=True), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    description = Column(String, unique=True, nullable=False)
    price = Column(DECIMAL(10, 2))
    start_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    finish_date = Column(DateTime(timezone=True), nullable=True)
