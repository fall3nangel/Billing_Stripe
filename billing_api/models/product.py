import enum
import uuid

from sqlalchemy import (
    DECIMAL,
    Column,
    Enum,
    ForeignKey,
    String,
    Table,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.postgres import Base


class ProductDuration(enum.Enum):
    month = 1
    day = 2


product_movie = Table(
    "product_movie_link",
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
        "movie_id",
        ForeignKey("movie.id"),
        primary_key=False,
    ),
)


class Movie(Base):
    __tablename__ = "movie"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)


class Product(Base):
    __tablename__ = "product"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = Column(String, nullable=False)
    price = Column(DECIMAL(10, 2))
    duration = Column("duration", Enum(ProductDuration, name="duration_enum", create_type=False))
    movies = relationship(
        "Movie",
        secondary=product_movie,
        primaryjoin=id == product_movie.c.product_id,
        secondaryjoin=Movie.id == product_movie.c.movie_id,
        backref="products",
        cascade="all,delete",
    )
