"""Database model representing a user."""

from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import TIMESTAMP, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models import BaseModel
from app.schemas.users import UserRead


class User(SQLAlchemyBaseUserTable[int], BaseModel):
    """Database model representing a user.

    Attributes:
        id (int): The primary key of the user.
        email (str): The email address of the user.
        hashed_password (str): The hashed password of the user.
        telephone (str): The telephone number of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        last_login (datetime): The timestamp of the last login.
        full_name (str): The full name of the user.
        telegram_user_id (str): The Telegram user ID of the user.
        role (str): The role of the user.
        country (str): The country of the user.
        city (str): The city of the user.
        is_superuser (bool): Indicates whether the user is a superuser.
        is_active (bool): Indicates whether the user is active.
        is_verified (bool): Indicates whether the user is verified.
        created_at (datetime): The timestamp when the user was created.
        updated_at (datetime): The timestamp when the user was last updated.
    """

    telephone: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False
    )
    first_name: Mapped[str] = mapped_column(String(150), nullable=True)
    last_name: Mapped[str] = mapped_column(String(150), nullable=True)
    last_login: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=True
    )

    def to_pydantic_model(self):
        """Convert the database model to a Pydantic model (UserRead).

        Returns:
            UserRead: The Pydantic model representing the user.
        """
        return UserRead(
            id=self.id,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            full_name=self.full_name,
            telephone=self.telephone,
            telegram_user_id=self.telegram_user_id,
            role=self.role,
            country=self.country,
            city=self.city,
            last_login=self.last_login,
            is_superuser=self.is_superuser,
            is_active=self.is_active,
            is_verified=self.is_verified,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
