"""Repository for interacting with the User model in the database."""

from sqlalchemy import select

from app.models import User
from app.utils.repository import BaseRepository


class UsersRepository(BaseRepository):
    """Repository for interacting with the User model in the database.

    Attributes:
        model: The User model.
        session: The database session.
    """

    model = User

    async def get_by_telephone(self, telephone: str):
        """Get a user by telephone number.

        Args:
            telephone (str): The telephone number to search for.

        Returns:
            User: The user with the specified telephone number,
                or None if not found.
        """
        if telephone:
            statement = select(self.model).where(
                self.model.telephone == telephone
            )
        else:
            raise ValueError("telephone must be provided")
        result = await self.session.execute(statement)
        return result.scalars().first()
