import datetime
import secrets
import string
import uuid

from pbkdf2 import crypt
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from core.config import settings
from db.postgres import Base
from models.product import Product
from models.role import Role, user_role

user_product = Table(
    "user_product_link",
    Base.metadata,
    Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    ),
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
        cascade="all,delete",
    )
    products = relationship(
        "Product",
        secondary=user_product,
        primaryjoin=id == user_product.c.user_id,
        secondaryjoin=Product.id == user_product.c.product_id,
        backref="users",
        cascade="all,delete",
    )

    def __init__(
        self,
        login=None,
        password=None,
        email=None,
        fullname=None,
        phone=None,
        timezone=0,
    ):
        self.login = login
        self.plain_password = password
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

    @hybrid_property
    def plain_password(self):
        return self.password

    @plain_password.setter
    def plain_password(self, plaintext):
        alphabet = string.ascii_letters + string.digits
        salt = "".join(secrets.choice(alphabet) for _ in range(settings.users_app.salt_length))
        hpswd = crypt(plaintext, salt, iterations=settings.users_app.psw_hash_iterations)
        parts_hpswd = hpswd.split("$")
        self.password = f"{parts_hpswd[3]}{parts_hpswd[4]}"

    def check_password(self, plaintext):
        salt = self.password[: settings.users_app.salt_length]
        hpswd = crypt(plaintext, salt, iterations=settings.users_app.psw_hash_iterations)
        hpswd_db = "$".join(
            [
                "",
                settings.users_app.kdf_algorithm,
                f"{settings.users_app.psw_hash_iterations:x}",
                salt,
                self.password[settings.users_app.salt_length :],
            ]
        )
        return hpswd == hpswd_db
