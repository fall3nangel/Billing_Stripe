from sqlalchemy import select


class DBService:
    def __init__(self, session):
        # session.execute("SET search_path TO users;")
        self.session = session

    async def get_user(self, id: str):
        from models.user import User
        res = await self.session.execute(select(User).filter_by(id=id))
        return res.first()[0]

    async def get_user_by_login(self, login: str):
        from models.user import User
        res = await self.session.execute(select(User).filter_by(login=login))
        return res.first()[0]

    async def add_user(self, login: str, password: str, email: str, fullname: str, phone: str, subscribed: bool):
        from models.user import User
        user = User(
            login=login,
            password=password,
            email=email,
            fullname=fullname,
            phone=phone,
            subscribed=False,
        )
        '''result = await self.session.execute(
            "SELECT * FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';")
        for r in result:
            print(r)'''
        self.session.add(user)
        await self.session.commit()
        return user
