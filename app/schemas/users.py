from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.services.validators import (
    EmailValidator,
    PasswordValidator,
    TelephoneValidator,
)


class UserSchema(BaseModel):
    id: int
    email: str
    password_hash: str
    first_name: str
    last_name: str
    telephone: str
    telegram_user_id: str
    role: str
    country: str
    city: str
    last_login: str
    is_superuser: bool
    is_staff: bool
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UsersSchemaAdd(BaseModel):
    email: str
    password: str
    confirm_password: str
    first_name: Optional[str] = Field(None)
    last_name: Optional[str] = Field(None)
    telephone: Optional[str] = Field(None)
    telegram_user_id: Optional[int] = Field(None)
    role: Optional[str] = Field("user")
    country: Optional[str] = Field(None)
    city: Optional[str] = Field(None)

    def _validate_password(self):
        validator = PasswordValidator()
        validator(self.password, self.confirm_password)

    def _validate_email(self):
        validator = EmailValidator()
        validator(self.email)

    def _validate_telephone(self):
        validator = TelephoneValidator()
        validator(self.telephone)

    def validate_data(self):
        self._validate_password()
        self._validate_email()
        self._validate_telephone()


class UsersSchemaEdit(BaseModel):
    first_name: Optional[str] = Field(None)
    last_name: Optional[str] = Field(None)
    telephone: Optional[str] = Field(None)
    telegram_user_id: Optional[int] = Field(None)
    country: Optional[str] = Field(None)
    city: Optional[str] = Field(None)

    def _validate_telephone(self):
        if self.telephone:
            validator = TelephoneValidator()
            validator(self.telephone)

    def validate_data(self):
        self._validate_telephone()
