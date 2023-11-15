from abc import ABC, abstractmethod

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def add(self, data: dict) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self):
        raise NotImplementedError

    async def get(self, id: int):
        raise NotImplementedError

    async def update(self, id: int, data: dict):
        raise NotImplementedError

    async def delete(self, id: int):
        raise NotImplementedError


class BaseRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, data: dict) -> int:
        statement = insert(self.model).values(**data).returning(self.model.id)
        result = await self.session.execute(statement)

        return result.scalar_one()

    async def get_all(self):
        statement = select(self.model)
        result = await self.session.execute(statement)
        return [row[0].to_pydantic_model() for row in result.all()]

    async def get(self, id: int):
        statement = select(self.model).where(self.model.id == id)
        result = await self.session.execute(statement)
        result = result.scalar_one()
        return result.to_pydantic_model()

    async def update(self, id: int, data: dict):
        statement = (
            update(self.model)
            .where(self.model.id == id)
            .values(**data)
            .returning(self.model.id)
        )
        result = await self.session.execute(statement)

        return result.scalar_one()

    async def delete(self, id: int):
        statement = delete(self.model).where(self.model.id == id).returning()
        return await self.session.execute(statement)
