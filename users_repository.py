from databases import Database
from models import users
from schemas import UserIn, User
from security import hash_password
import datetime


class UsersRepository:
    def __init__(self, database: Database):
        self.database = database

    async def get_all_users(self, skip: int = 0, limit: int = 100):
        query = users.select()
        return await self.database.fetch_all(query)

    async def create_user(self, user: UserIn):
        user = User(
            username=user.username,
            email=user.email,
            hashed_password=hash_password(user.password1),
            first_name=user.first_name,
            last_name=user.last_name,
            created_time=datetime.datetime.utcnow(),
            updated_time=datetime.datetime.utcnow()
        )

        values = {**user.dict()}
        values.pop('id', None)

        query = users.insert().values(**values)
        user.id = await self.database.execute(query)
        return user

    async def get_user_by_id(self, id: int):
        query = users.select().where(users.c.id == id)
        user = await self.database.fetch_one(query)
        if user is None:
            return None
        return User.parse_obj(user)

    async def get_user_by_username(self, username: str):
        query = users.select().where(users.c.username == username)
        user = await self.database.fetch_one(query)
        if user is None:
            return None
        return User.parse_obj(user)

    async def get_user_by_email(self, email: str):
        query = users.select().where(users.c.email == email)
        user = await self.database.fetch_one(query)
        if user is None:
            return None
        return User.parse_obj(user)

    async def update_user(self, id: int, user: UserIn):
        user = User(
            id=id,
            username=user.username,
            email=user.email,
            hashed_password=hash_password(user.password1),
            first_name=user.first_name,
            last_name=user.last_name,
            created_time=datetime.datetime.utcnow(),
            updated_time=datetime.datetime.utcnow(),
            is_active=user.is_active
        )
        values = {**user.dict()}
        values.pop('created_at', None)
        values.pop('id', None)
        query = users.update().where(users.c.id == id).values(**values)
        await self.database.execute(query)
        return user

    async def delete_user(self, id: int):
        query = users.delete().where(users.c.id == id)
        return await self.database.execute(query=query)
