from typing import Optional

from pydantic import BaseModel, EmailStr, constr, validator
from datetime import datetime


class User(BaseModel):
    id: Optional[str] = None
    username: str
    email: EmailStr
    hashed_password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    created_time: datetime
    updated_time: datetime
    is_active: bool = True


class UserIn(BaseModel):
    username: constr(regex=r'^[\w.@+-]+$', min_length=1, max_length=150)
    email: EmailStr
    password1: constr(regex=r'^(?=.*[A-Z])(?=.*\d).{8,}$')
    password2: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool = True

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password1' in values and v != values['password1']:
            raise ValueError('passwords do not match')
        return v


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
    password: str
