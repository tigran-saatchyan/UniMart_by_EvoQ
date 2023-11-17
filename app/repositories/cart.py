from sqlalchemy import and_, delete, func, select, update

from app.models import User
from app.models.cart import Cart
from app.utils.repository import BaseRepository


class CartRepository(BaseRepository):
    model = Cart

    async def get_total_price(self, user: User):
        statement = select(func.sum(Cart.price)).where(
            Cart.owner_id == user.id
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_product_id(self, product_id: int, user: User):
        statement = select(self.model).where(
            and_(
                self.model.product_id == product_id,
                self.model.owner_id == user.id,
            )
        )
        result = await self.session.execute(statement)
        result = result.scalar_one_or_none()
        return result.to_pydantic_model() if result else None

    async def update_by_product_id(
        self, product_id: int, data: dict, user: User
    ):
        statement = (
            update(self.model)
            .where(
                and_(
                    self.model.product_id == product_id,
                    self.model.owner_id == user.id,
                )
            )
            .values(**data)
            .returning(self.model.product_id)
        )
        result = await self.session.execute(statement)

        return result.scalar_one()

    async def delete_by_owner_id_and_product_id(
        self, product_id: int, user: User
    ):
        statement = (
            delete(self.model)
            .where(
                and_(
                    self.model.product_id == product_id,
                    self.model.owner_id == user.id,
                )
            )
            .returning()
        )
        return await self.session.execute(statement)

    async def delete_all_by_owner_id(self, user: User):
        statement = (
            delete(self.model)
            .where(
                self.model.owner_id == user.id,
            )
            .returning()
        )
        return await self.session.execute(statement)
