"""Repository module."""

from abc import ABC, abstractmethod

from sqlalchemy import and_, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class AbstractRepository(ABC):
    @abstractmethod
    async def add(self, data: dict) -> int:
        """Add a new record to the repository.

        Args:
            data (dict): The data to be added.

        Returns:
            int: The ID of the added record.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, owner: User):
        """Get all records from the repository for a specific owner.

        Args:
            owner (User): The owner of the records.

        Returns:
            list: A list of records.
        """
        raise NotImplementedError

    async def get(self, id: int, owner: User):
        """Get a specific record from the repository.

        Args:
            id (int): The ID of the record.
            owner (User): The owner of the record.

        Returns:
            pydantic.Model: The retrieved record.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: int, data: dict, owner: User):
        """Update a specific record in the repository.

        Args:
            id (int): The ID of the record to be updated.
            data (dict): The data to be updated.
            owner (User): The owner of the record.

        Returns:
            int: The ID of the updated record.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int, owner: User):
        """Delete a specific record from the repository.

        Args:
            id (int): The ID of the record to be deleted.
            owner (User): The owner of the record.

        Returns:
            None
        """
        raise NotImplementedError


class BaseRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, data: dict) -> int:
        """Add a new record to the repository.

        Args:
            data (dict): The data to be added.

        Returns:
            int: The ID of the added record.
        """
        statement = insert(self.model).values(**data).returning(self.model.id)
        result = await self.session.execute(statement)
        return result.scalar_one()

    async def get_all(self, owner: User):
        """Get all records from the repository for a specific owner.

        Args:
            owner (User): The owner of the records.

        Returns:
            list: A list of records.
        """
        statement = select(self.model).where(self.model.owner_id == owner.id)
        result = await self.session.execute(statement)
        return [row[0].to_pydantic_model() for row in result.all()]

    async def get(self, id: int, owner: User):
        """Get a specific record from the repository.

        Args:
            id (int): The ID of the record.
            owner (User): The owner of the record.

        Returns:
            pydantic.Model: The retrieved record.
        """
        statement = select(self.model).where(
            and_(
                self.model.id == id,
                self.model.owner_id == owner.id,
            )
        )
        result = await self.session.execute(statement)
        result = result.scalar_one()
        return result.to_pydantic_model()

    async def update(self, id: int, data: dict, owner: User):
        """Update a specific record in the repository.

        Args:
            id (int): The ID of the record to be updated.
            data (dict): The data to be updated.
            owner (User): The owner of the record.

        Returns:
            int: The ID of the updated record.
        """
        statement = (
            update(self.model)
            .where(
                and_(
                    self.model.id == id,
                    self.model.owner_id == owner.id,
                )
            )
            .values(**data)
            .returning(self.model.product_id)
        )
        result = await self.session.execute(statement)
        return result.scalar_one()

    async def delete(self, id: int, owner: User):
        """Delete a specific record from the repository.

        Args:
            id (int): The ID of the record to be deleted.
            owner (User): The owner of the record.

        Returns:
            None
        """
        statement = (
            delete(self.model)
            .where(
                and_(
                    self.model.id == id,
                    self.model.owner_id == owner.id,
                )
            )
            .returning()
        )
        await self.session.execute(statement)
