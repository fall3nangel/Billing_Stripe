import uuid

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import UUID

from db.postgres import Base

user_role = Table(
    "user_role_link",
    Base.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("user_id", ForeignKey("user.id"), primary_key=False),
    Column(
        "role_id",
        ForeignKey("role.id"),
        primary_key=False,
    ),
)


class Role(Base):
    __tablename__ = "role"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = Column(String, nullable=False)
