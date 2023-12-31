"""Repository for interacting with the Cart model in the database."""

from sqlalchemy import and_, delete, func, select, update

from app.models import User
from app.models.cart import Cart
from app.repositories.repository import BaseRepository


class CartRepository(BaseRepository):
    """Repository for interacting with the Cart model in the database.

    Attributes:
        model: The Cart model.
        session: The database session.
    """

    model = Cart

    async def get_total_price(self, user: User):
        """Get the total price of all products in the user's cart.

        Args:
            user (User): The user for whom to calculate the total price.

        Returns:
            float: The total price of all products in the user's cart.
        """
        statement = select(func.sum(Cart.price)).where(
            Cart.owner_id == user.id
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_product_id(self, product_id: int, user: User):
        """Get a cart item by product ID for a specific user.

        Args:
            product_id (int): The ID of the product.
            user (User): The user for whom to retrieve the cart item.

        Returns:
            CartRead: The Pydantic model representing the cart item,
                or None if not found.
        """
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
        """Update a cart item by product ID for a specific user.

        Args:
            product_id (int): The ID of the product.
            data (dict): The data to update in the cart item.
            user (User): The user for whom to update the cart item.

        Returns:
            int: The product ID of the updated cart item.
        """
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
        """Delete a cart item by product ID for a specific user.

        Args:
            product_id (int): The ID of the product.
            user (User): The user for whom to delete the cart item.

        Returns:
            None: The result of the deletion operation.
        """
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
        """Delete all cart items for a specific user.

        Args:
            user (User): The user for whom to delete all cart items.

        Returns:
            None: The result of the deletion operation.
        """
        statement = (
            delete(self.model)
            .where(
                self.model.owner_id == user.id,
            )
            .returning()
        )
        return await self.session.execute(statement)
