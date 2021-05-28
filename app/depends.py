from fastapi import Depends, HTTPException

from database import database
from security import JWTBearer, decode_access_token
from users_repository import UsersRepository


def get_user_repository():
    return UsersRepository(database)


async def get_current_user(
        users: UsersRepository = Depends(get_user_repository),
        token: str = Depends(JWTBearer()),
):
    payload = decode_access_token(token)
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=403, detail="Invalid credentials")
    user = await users.get_user_by_username(username)
    return user
