"""Pydantic models for the user schema."""

from datetime import datetime
from typing import Optional

from fastapi_users import schemas
from pydantic import Field


class UserRead(schemas.BaseUser[int]):
    """Pydantic model representing the read-only view of a user.

    Attributes:
        id (int): The unique identifier of the user.
        email (str): The email address of the user.
        hashed_password (str): The hashed password of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        telephone (str): The telephone number of the user.
        last_login (Optional[datetime]): The timestamp of the last login.
        is_superuser (bool): Indicates whether the user is a superuser.
        is_active (bool): Indicates whether the user is active.
        is_verified (bool): Indicates whether the user is verified.
        created_at (datetime): The timestamp when the user was created.
        updated_at (datetime): The timestamp when the user was last
            updated.

    Config:
        from_attributes (bool): Enable attribute assignment from class
            attributes.
    """

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
    """Pydantic model representing the creation of a user.

    Attributes:
        email (str): The email address of the user.
        password (str): The password of the user.
        confirm_password (str): The confirmation of the password.
        first_name (Optional[str]): The first name of the user.
        last_name (Optional[str]): The last name of the user.
        telephone (Optional[str]): The telephone number of the user.

    Config:
        schema_extra (dict): Additional information for OpenAPI schema.
    """

    confirm_password: str
    first_name: Optional[str] = Field(None)
    last_name: Optional[str] = Field(None)
    telephone: Optional[str] = Field(None)


class UserUpdate(schemas.BaseUserUpdate):
    """Pydantic model representing the update of a user.

    Attributes:
        password (Optional[str]): The new password of the user.
        confirm_password (str): The confirmation of the new password.
        first_name (Optional[str]): The new first name of the user.
        last_name (Optional[str]): The new last name of the user.
        telephone (Optional[str]): The new telephone number of the user.

    Config:
        schema_extra (dict): Additional information for OpenAPI schema.
    """

    confirm_password: str
    first_name: Optional[str] = Field(None)
    last_name: Optional[str] = Field(None)
    telephone: Optional[str] = Field(None)
