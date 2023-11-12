from pydantic import BaseModel


class UserSchema(BaseModel):
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

    class Config:
        from_attributes = True
