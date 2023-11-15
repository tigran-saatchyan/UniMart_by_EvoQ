from datetime import datetime
from typing import Optional

from fastapi_users import schemas
from pydantic import Field


class UserRead(schemas.BaseUser[int]):
    id: int
    first_name: str
    last_name: str
    telephone: str
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    confirm_password: str
    first_name: Optional[str] = Field(None)
    last_name: Optional[str] = Field(None)
    telephone: Optional[str] = Field(None)


class UserUpdate(schemas.BaseUserUpdate):
    confirm_password: str
    first_name: Optional[str] = Field(None)
    last_name: Optional[str] = Field(None)
    telephone: Optional[str] = Field(None)
