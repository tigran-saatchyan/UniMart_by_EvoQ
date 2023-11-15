from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import TIMESTAMP, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models import BaseModel
from app.schemas.users import UserRead


class User(SQLAlchemyBaseUserTable[int], BaseModel):
    __tablename__ = "users"

    telephone: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False
    )
    first_name: Mapped[str] = mapped_column(String(150), nullable=True)
    last_name: Mapped[str] = mapped_column(String(150), nullable=True)
    last_login: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=True
    )

    def to_pydantic_model(self):
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

    class PydanticMeta:
        computed = ("full_name",)
        exclude = ("is_active", "is_superuser", "is_verified")
