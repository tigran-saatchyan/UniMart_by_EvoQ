from abc import ABC, abstractmethod

from sqlalchemy import and_, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class AbstractRepository(ABC):
    @abstractmethod
    async def add(self, data: dict) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, owner: User):
        raise NotImplementedError

    async def get(self, id: int, owner: User):
        raise NotImplementedError

    async def update(self, id: int, data: dict, owner: User):
        raise NotImplementedError

    async def delete(self, id: int, owner: User):
        raise NotImplementedError


class BaseRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(
        self,
        data: dict,
    ) -> int:
        statement = insert(self.model).values(**data).returning(self.model.id)
        result = await self.session.execute(statement)

        return result.scalar_one()

    async def get_all(self, owner: User):
        statement = select(self.model).where(self.model.owner_id == owner.id)
        result = await self.session.execute(statement)
        return [row[0].to_pydantic_model() for row in result.all()]

    async def get(self, id: int, owner: User):
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
        return await self.session.execute(statement)
