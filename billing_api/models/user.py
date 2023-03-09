import datetime
import uuid

from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, String, Table, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.postgres import Base

from models.role import Role, user_role
from models.product import Product


user_product = Table(
    "user_product_link",
    Base.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("product_id", ForeignKey("product.id"), primary_key=False),
    Column(
        "user_id",
        ForeignKey("user.id"),
        primary_key=False,
    ),
)

class User(Base):
    __tablename__ = "user"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=True)
    email = Column(String)
    fullname = Column(String)
    phone = Column(String)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    timezone = Column(Integer)
    roles = relationship(
        "Role",
        secondary=user_role,
        primaryjoin=id == user_role.c.user_id,
        secondaryjoin=Role.id == user_role.c.role_id,
        backref="users",
        cascade="all,delete"
    )
    products = relationship(
        "Product",
        secondary=user_product,
        primaryjoin=id == user_product.c.user_id,
        secondaryjoin=Product.id == user_product.c.product_id,
        backref="users",
        cascade="all,delete"
    )

    def __init__(self, login=None, password=None, email=None, fullname=None, phone=None, timezone=0):
        self.login = login
        self.password = password
        self.email = email
        self.fullname = fullname
        self.phone = phone
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        self.timezone = timezone

    @property
    def as_dict(self) -> dict:
        return {
            "login": self.login,
            "fullname": self.fullname,
            "email": self.email,
            "phone": self.phone,
            "timezone": self.timezone,
        }

    class Meta:
        db_table = "user"
        verbose_name = "user"
        verbose_name_plural = "users"