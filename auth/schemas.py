from datetime import datetime
import uuid
from typing import Optional

from fastapi_users import schemas, password
from pydantic import EmailStr, BaseModel


class UserRead(schemas.BaseUser[int]):
    id: int
    email: EmailStr
    username: str
    role: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(schemas.BaseUserCreate):
    id: int
    email: EmailStr
    username: str
    role: int
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    pass
