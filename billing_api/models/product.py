import uuid

from sqlalchemy import Column, String, DECIMAL, Enum
from sqlalchemy.dialects.postgresql import UUID

from db.postgres import Base

PRODUCT_DURATION = "month", "day"
class Product(Base):
    __tablename__ = "product"
    __table_args__ = {'schema': "invoice"}
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String, nullable=False)
    price = Column(DECIMAL(10, 2))
    duration = Column("duration", Enum(PRODUCT_DURATION, name="gender_enum", create_type=False))

