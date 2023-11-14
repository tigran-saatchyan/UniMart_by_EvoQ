from fastapi import HTTPException, status
from sqlalchemy import select

from app.models import User
from app.utils.repository import BaseRepository


class UsersRepository(BaseRepository):
    model = User

    async def get_by_email(self, email: str):
        if email:
            statement = select(self.model).where(self.model.email == email)
        else:
            raise ValueError("email must be provided")
        result = await self.session.execute(statement)
        return result.scalars().first()

    async def get_by_telephone(self, telephone: str):
        if telephone:
            statement = select(self.model).where(
                self.model.telephone == telephone
            )
        else:
            raise ValueError("telephone must be provided")
        result = await self.session.execute(statement)
        return result.scalars().first()

    async def is_exists(self, user_dict: dict):
        is_exists_email = await self.get_by_email(user_dict["email"])
        is_exists_telephone = await self.get_by_telephone(
            user_dict["telephone"]
        )
        if is_exists_email or is_exists_telephone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email OR telephone "
                "number already exists",
            )
