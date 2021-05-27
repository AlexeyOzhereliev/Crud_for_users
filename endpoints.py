from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from schemas import User, UserIn, TokenData, Token
from security import verify_password, create_access_token
from users_repository import UsersRepository
from depends import get_user_repository, get_current_user


router = APIRouter()


@router.post("/token-auth", tags=["Token_auth"], response_model=Token)
async def get_token(token_data: TokenData,
                    users: UsersRepository = Depends(get_user_repository)):
    user = await users.get_user_by_username(token_data.username)
    if user is None or not verify_password(token_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return Token(access_token=create_access_token(dict(sub=user.username)),
                 token_type="Bearer")


@router.post("/users", tags=["Users"], response_model=User, response_model_exclude={'hashed_password', 'id'})
async def register_user(user: UserIn,
                        users: UsersRepository = Depends(get_user_repository)):
    bd_user = await users.get_user_by_username(user.username)
    bd_email = await users.get_user_by_email(user.email)
    if bd_user is not None:
        raise HTTPException(status_code=500, detail='This username already exists')
    elif bd_email is not None:
        raise HTTPException(status_code=500, detail='This email already exists')
    return await users.create_user(user)


@router.get("/users", tags=["Users"], response_model=List[User], response_model_exclude={'hashed_password', 'id'})
async def read_users(users: UsersRepository = Depends(get_user_repository)):
    return await users.get_all_users()


@router.get("/users/{id}", tags=["Users"], response_model=User, response_model_exclude={'hashed_password', 'id'})
async def read_user(id: int, users: UsersRepository = Depends(get_user_repository)):
    return await users.get_user_by_id(id=id)


@router.put("/users/{id}", tags=["Users"], response_model=User, response_model_exclude={'hashed_password', 'id'})
async def update_user(id: int,
                      user: UserIn,
                      users: UsersRepository = Depends(get_user_repository),
                      current_user: User = Depends(get_current_user)):
    old_user = await users.get_user_by_id(id=id)
    bd_user = await users.get_user_by_username(user.username)
    bd_email = await users.get_user_by_email(user.email)
    if old_user is None or old_user.username != current_user.username:
        return HTTPException(status_code=404, detail="User not found")
    if bd_user is not None:
        raise HTTPException(status_code=500, detail='This username already exists')
    elif bd_email is not None:
        raise HTTPException(status_code=500, detail='This email already exists')
    return await users.update_user(id=id, user=user)


@router.delete("/users/{id}", tags=["Users"], response_model=User)
async def delete_user(id: int, users: UsersRepository = Depends(get_user_repository),
                      current_user: User = Depends(get_current_user)):
    user_being_deleted = await users.get_user_by_id(id=id)
    if user_being_deleted is None or user_being_deleted.username != current_user.username:
        return HTTPException(status_code=404, detail="User not found")
    return await users.delete_user(id=id)
