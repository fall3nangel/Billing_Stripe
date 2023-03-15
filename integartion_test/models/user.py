import uuid

from sqlalchemy import Column, String, TIMESTAMP, Integer
from sqlalchemy.dialects.postgresql import UUID

from postgres import Base


class User(Base):
    __tablename__ = "user"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )

