import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

from db.postgres import engine, get_db_service
from models.product import Product

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)
Base = declarative_base()
db = SessionLocal()


async def create_user():
    product = Product(name="Фильмы для детей", price=1000.00, duration="month")
    db.add(product)
    await db.flush()
    await db.commit()


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_user())
    loop.close()


if __name__ == "__main__":
    main()
