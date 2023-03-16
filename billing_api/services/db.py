import logging
from datetime import date, datetime

from dateutil.relativedelta import relativedelta
from sqlalchemy import select
from sqlalchemy.orm import selectinload


class DBService:
    def __init__(self, session):
        self.db = session

    async def get_user(self, id: str):
        from models.user import User

        res = await self.db.execute(select(User).filter_by(id=id))
        return res.scalars().first()

    async def get_product(self, id: str):
        from models.product import Product

        res = await self.db.execute(select(Product).filter_by(id=id))
        return res.scalars().first()

    async def get_all_products(self):
        from models.product import Product

        res = await self.db.execute(select(Product))
        return res.scalars().all()

    async def get_last_invoice_by_user(self, user_id: str, product_id: str):
        from models.invoice import Invoice

        res = await self.db.execute(
            select(Invoice)
            .filter_by(user_id=user_id)
            .filter_by(product_id=product_id)
            .order_by(Invoice.start_date.desc())
        )
        return res.scalars().first()

    async def get_payment(self, id: str):
        from models.payment import Payment

        res = await self.db.execute(select(Payment).filter_by(id=id))
        return res.scalars().first()

    async def update_payment(self, id: str, pay_date: datetime, intent_id: str):
        from models.payment import Payment

        payment = await self.db.execute(select(Payment).filter_by(id=id))

        setattr(payment, "pay_date", pay_date)
        setattr(payment, "payment_intent_id", intent_id)
        await self.db.commit()

    async def get_last_payment_by_user(self, user_id: str, product_id: str):
        from models.payment import Payment

        res = await self.db.execute(
            select(Payment)
            .filter_by(user_id=user_id)
            .filter_by(product_id=product_id)
            .order_by(Payment.pay_date.desc())
        )
        return res.scalars().first()

    async def add_invoice_by_product(self, user_id: str, product_id: str):
        from models.invoice import Invoice
        from models.product import Product

        res = await self.db.execute(select(Product).filter_by(id=product_id))

        if not (product := res.scalars().first()):
            logging.error(f"Отсутствует продукт с uuid '{product_id}'")
        logging.debug(product.name)

        invoice = Invoice(
            product_id=product.id,
            user_id=user_id,
            description=f"Счет на оплату {product.name}",
            price=product.price,
            start_date=datetime.now(),
            finish_date=datetime.now() + relativedelta(month=1),
        )
        self.db.add(invoice)
        await self.db.commit()

        return invoice

    async def add_next_invoice(
        self, user_id: str, product_id: str, price: int, start_date: datetime
    ):
        from models.invoice import Invoice
        from models.product import Product

        invoice = Invoice(
            product_id=product_id,
            user_id=user_id,
            description=f"Счет на оплату",
            price=price,
            start_date=start_date,
            finish_date=start_date + relativedelta(month=1),
        )
        self.db.add(invoice)
        await self.db.commit()

    """async def add_product(self, id: str, name: str, price: int, duration: str):
        from models.product import Product, Movie
        movie1 = Movie(id="3fa85f64-5717-3562-b3fc-2c963f66afa4", name="test1", description="test1")
        movie2 = Movie(id="4fa85f64-5717-3562-b3fc-2c963f66afa4", name="test2", description="test2")
        product = Product(
            id=id,
            name=name,
            price=price,
            duration=duration,
            movies=[movie1, movie2]
        )
        self.db.add(product)
        await self.db.commit()
        return product"""

    async def add_product_to_user(self, product_id: str, user_id: str):
        from models.product import Product
        from models.user import User

        res1 = await self.db.execute(
            select(Product)
            .filter_by(id=product_id)
            .options(selectinload(Product.movies))
        )
        product = res1.scalars().first()
        res2 = await self.db.execute(
            select(User).filter_by(id=user_id).options(selectinload(User.products))
        )
        user = res2.scalars().first()
        setattr(user, "products", [product])
        await self.db.commit()

        return product

    async def add_payment_to_user(
        self, payment_id: str, user_id: str, amount: int, currency: str, pay_date: datetime
    ):
        from models.invoice import Invoice
        from models.payment import Currency, Payment

        res = await self.db.execute(
            select(Invoice)
            .filter_by(user_id=user_id)
            .order_by(Invoice.start_date.desc())
        )
        invoice = res.scalars().first()

        payment = Payment(
            id=payment_id,
            product_id=invoice.product_id,
            user_id=user_id,
            invoice_id=invoice.id,
            description=f"Платеж по счету {invoice.id} за период : {invoice.start_date} - {invoice.finish_date}",
            amount=amount,
            currency=Currency[currency],
            pay_date=pay_date,
        )
        self.db.add(payment)
        await self.db.commit()

        res = await self.db.execute(
            select(Invoice)
            .filter_by(user_id=user_id)
            .order_by(Invoice.start_date.desc())
        )
        invoice = res.scalars().first()

        payment = await self.get_last_payment_by_user(user_id, invoice.product_id)

        if payment:
            await self.add_next_invoice(
                user_id, invoice.product_id, amount, invoice.finish_date
            )

        return payment

    async def del_payment(self, payment_id: str):
        from models.payment import Payment

        res = await self.db.execute(select(Payment).filter_by(id=payment_id))
        payment = res.scalars().first()
        await self.db.delete(payment)
        await self.db.commit()

    async def del_product_from_user(self, product_id: str, user_id: str):
        from models.product import Product
        from models.user import User

        res1 = await self.db.execute(
            select(Product)
            .filter_by(id=product_id)
            .options(selectinload(Product.movies))
        )
        product = res1.scalars().first()
        res2 = await self.db.execute(
            select(User).filter_by(id=user_id).options(selectinload(User.products))
        )
        user = res2.scalars().first()
        new_products = [prod for prod in user.products if str(prod.id) != product_id]
        setattr(user, "products", new_products)
        await self.db.commit()
        return product

    async def check_payment(self, user_id: str, product_id: str) -> bool:
        from models.invoice import Invoice
        from models.payment import Payment

        res = await self.db.execute(
            select(Payment)
            .filter_by(user_id=user_id)
            .filter_by(product_id=product_id)
            .order_by(Payment.pay_date.desc())
        )
        payment: Payment = res.scalars().first()

        if not payment:
            return False

        res = await self.db.execute(select(Invoice).filter_by(id=payment.invoice_id))
        invoice: Invoice = res.scalars().first()

        if invoice.start_date.replace(tzinfo=None) <= datetime.now() and (
            invoice.finish_date is None or datetime.now() < invoice.finish_date.replace(tzinfo=None)
        ):
            return True

        """deadline = datetime.now() - relativedelta(month=1)

        if deadline <= payment.pay_date.replace(tzinfo=None):
            return True"""
        return False

    async def get_product_by_movie(self, movie_id: str) -> str:
        from models.product import Movie, Product

        # movie_id = "1fa85f64-5717-4562-b3fc-2c963f66afa4"
        res = await self.db.execute(
            select(Product).filter(Product.movies.any(Movie.id.in_([movie_id])))
        )

        return res.scalars().first()

    async def get_user_by_login(self, login: str):
        from models.user import User

        res = await self.db.execute(select(User).filter_by(login=login))
        return res.scalars().first()

    async def add_user(self, login: str, password: str, email: str, fullname: str, phone: str):
        from models.user import User

        user = User(
            login=login,
            password=password,
            email=email,
            fullname=fullname,
            phone=phone,
            timezone=0,
        )
        self.db.add(user)
        await self.db.commit()