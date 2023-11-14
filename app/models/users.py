from sqlalchemy import TIMESTAMP, Boolean, Integer, LargeBinary, String
from sqlalchemy.orm import Mapped, column_property, mapped_column

from app.models import BaseModel
from app.schemas.users import UserSchema


class User(BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True
    )
    password_hash: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    password_salt: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    telephone: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False
    )

    first_name: Mapped[str] = mapped_column(String(150), nullable=True)
    last_name: Mapped[str] = mapped_column(String(150), nullable=True)
    telegram_user_id: Mapped[str] = mapped_column(Integer, nullable=True)
    role: Mapped[str] = mapped_column(String(50), default="user")
    country: Mapped[str] = mapped_column(String(50), nullable=True)
    city: Mapped[str] = mapped_column(String(50), nullable=True)
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

    @property
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
        return UserSchema(
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
            is_staff=self.is_staff,
            is_active=self.is_active,
            is_verified=self.is_verified,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
