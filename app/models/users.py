from sqlalchemy import TIMESTAMP, Boolean, Integer, String
from sqlalchemy.orm import Mapped, column_property, mapped_column

from app.models import BaseModel
from app.schemas.users import UserSchema


class User(BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True
    )
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    first_name: Mapped[str] = mapped_column(String(150), nullable=True)
    last_name: Mapped[str] = mapped_column(String(150), nullable=True)
    telephone: Mapped[str] = mapped_column(String(50), nullable=False)
    telegram_user_id: Mapped[str] = mapped_column(Integer, nullable=True)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    country: Mapped[str] = mapped_column(String(50), nullable=False)
    city: Mapped[str] = mapped_column(String(50), nullable=False)
    last_login: Mapped[str] = mapped_column(TIMESTAMP, nullable=True)

    is_superuser: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    is_staff: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )

    @column_property
    def full_name(self) -> str:
        """Returns the best name"""
        if self.first_name or self.last_name:
            return (
                f"{self.first_name.title() or ''} "
                f"{self.last_name.title() or ''}"
            ).strip()
        return self.email

    def to_pydantic_model(self):
        return UserSchema.model_validate(self)
