from sqlalchemy import select

from app.models import User
from app.utils.repository import BaseRepository


class UsersRepository(BaseRepository):
    model = User

    async def get_by_telephone(self, telephone: str):
        if telephone:
            statement = select(self.model).where(
                self.model.telephone == telephone
            )
        else:
            raise ValueError("telephone must be provided")
        result = await self.session.execute(statement)
        return result.scalars().first()
