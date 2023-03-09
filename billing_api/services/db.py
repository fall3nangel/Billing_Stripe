import logging

from sqlalchemy import select

#
class DBService:
    def __init__(self, session):
        self.db = session

    async def get_product(self, id: str):
        from models.product import Product

        res = await self.db.execute(select(Product).filter_by(id=id))
        return res.first()

    async def add_invoice_by_product(self, id_product: str) -> bool:
        from models.product import Product

        res = await self.db.execute(select(Product).filter_by(id=id_product))
        if not (product := res.first()):
            logging.error(f"Отсутствует продукт с uuid '{id_product}'")
            return False
        logging.debug(product[0].name)

    # async def get_user(self, id: str):
    #     from models.user import User
    #     res = await self.session.execute(select(User).filter_by(id=id))
    #     return res.first()[0]
    #
    # async def get_user_by_login(self, login: str):
    #     from models.user import User
    #     res = await self.session.execute(select(User).filter_by(login=login))
    #     return res.first()[0]
    #
    # async def add_user(self, login: str, password: str, email: str, fullname: str, phone: str, subscribed: bool):
    #     from models.user import User
    #     user = User(
    #         login=login,
    #         password=password,
    #         email=email,
    #         fullname=fullname,
    #         phone=phone,
    #         subscribed=False,
    #     )
    #     self.session.add(user)
    #     await self.session.commit()
    #     return user
