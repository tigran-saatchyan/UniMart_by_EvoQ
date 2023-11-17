from typing import Any, Dict, Optional, Union

from fastapi import Depends, HTTPException, Request, status
from fastapi_users import (
    BaseUserManager,
    IntegerIDMixin,
    exceptions,
    models,
    schemas,
)
from sqlalchemy.exc import IntegrityError

from app.models import User
from app.repositories.users import UsersRepository
from app.services.validators import PasswordValidator, TelephoneValidator
from app.settings import config
from app.settings.auth import get_user_table


class UserManager(IntegerIDMixin, BaseUserManager[User, int], UsersRepository):
    reset_password_token_secret = config.JWT_SECRET
    verification_token_secret = config.JWT_SECRET

    async def validate_password(
        self, password: str, user: Union[schemas.UC, models.UP, Dict[str, Any]]
    ) -> None:
        validator = PasswordValidator()
        if isinstance(user, dict):
            validator(password, user["confirm_password"])
        else:
            validator(password, user.confirm_password)

    @staticmethod
    async def validate_telephone(
        user: Union[schemas.UC, models.UP, Dict[str, Any]]
    ) -> None:
        validator = TelephoneValidator()
        if isinstance(user, dict):
            validator(user["telephone"])
        else:
            validator(user.telephone)

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)
        await self.validate_telephone(user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict.pop("confirm_password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        try:
            created_user = await self.user_db.create(user_dict)
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this telephone already exists",
            ) from e
        return created_user

    async def _update(
        self, user: models.UP, update_dict: Dict[str, Any]
    ) -> models.UP:
        validated_update_dict = {}
        for field, value in update_dict.items():
            if field == "email" and value != user.email:
                try:
                    await self.get_by_email(value)
                    raise exceptions.UserAlreadyExists()
                except exceptions.UserNotExists:
                    validated_update_dict[field] = value
                    validated_update_dict["is_verified"] = False
            elif field == "password" and value is not None:
                await self.validate_password(value, update_dict)
                validated_update_dict[
                    "hashed_password"
                ] = self.password_helper.hash(value)
            elif field == "telephone" and value is not None:
                await self.validate_telephone(update_dict)
                validated_update_dict[field] = value

            else:
                validated_update_dict[field] = value
        return await self.user_db.update(user, validated_update_dict)


async def get_user_manager(user_db=Depends(get_user_table)):
    yield UserManager(user_db)
