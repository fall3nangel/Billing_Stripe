import datetime
import uuid

from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, String, Table, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.postgres import Base


user_role = Table(
    "user_role_link",
    Base.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("user_id", ForeignKey('users"."user.id'), primary_key=False),
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

    class Meta:
        db_table = 'users"."role'
        verbose_name = "role"
        verbose_name_plural = "roles"


user_notification = Table(
    "users.UserNotificationUserGroup",
    Base.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("user_id", ForeignKey('users"."user.id'), primary_key=False),
    Column(
        "notification_user_group_id",
        ForeignKey("notificationgroup.id"),
        primary_key=False,
    ),
)


class NotificationGroup(Base):
    __tablename__ = "notificationgroup"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = Column(String, nullable=False)

    class Meta:
        db_table = 'users"."notificationgroup'
        verbose_name = "notificationgroup"
        verbose_name_plural = "notificationgroups"


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
    allow_send_email = Column(Boolean)
    confirmed_email = Column(Boolean)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    timezone = Column(Integer)
    groups = relationship(
        "NotificationGroup",
        secondary=user_notification,
        primaryjoin=id == user_notification.c.user_id,
        secondaryjoin=NotificationGroup.id == user_notification.c.notification_user_group_id,
        backref="users",
    )
    roles = relationship(
        "Role",
        secondary=user_role,
        primaryjoin=id == user_role.c.user_id,
        secondaryjoin=Role.id == user_role.c.role_id,
        backref="users",
    )

    def __init__(self, login=None, password=None, email=None, fullname=None, phone=None, subscribed=False, timezone=0):
        self.login = login
        self.password = password
        self.email = email
        self.fullname = fullname
        self.phone = phone
        self.allow_send_email = subscribed
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        self.confirmed_email = False
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
        db_table = 'users"."user'
        verbose_name = "user"
        verbose_name_plural = "users"