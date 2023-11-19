"""Service class for managing user shopping carts."""

from typing import List, Union, overload

from fastapi import HTTPException, status
from sqlalchemy.exc import NoResultFound

from app.api.v1.dependencies import UOWDependency
from app.models import User
from app.schemas.cart import CartCreate, CartUpdate
from app.services.products import ProductsService
from app.services.validators import ProductInCartValidator


class CartService:
    """Service class for managing user shopping carts.

    Methods:
        add: Add one or multiple products to the user's cart.
        add_one: Add a single product to the user's cart.
        add_many: Add multiple products to the user's cart.
        get_all: Get all products from the user's cart.
        get: Get a specific product from the user's cart.
        update: Update the quantity of a product in the user's cart.
        delete: Remove a product from the user's cart.
        delete_all: Remove all products from the user's cart.
        get_total_price: Get the total price of all products in the
            user's cart.
        is_in_cart: Check if a product is already in the user's cart.
    """

    @overload
    def add(
        self, uow: UOWDependency, product: CartCreate, user: User
    ) -> int: ...

    @overload
    def add(
        self, uow: UOWDependency, products: List[CartCreate], user: User
    ) -> List[int]: ...

    async def add(
        self,
        uow: UOWDependency,
        products: Union[CartCreate, List[CartCreate]],
        user: User,
    ) -> Union[int, List[int]]:
        """Add one or multiple products to the user's cart.

        Args:
            uow (UOWDependency): The unit of work dependency.
            products (Union[CartCreate, List[CartCreate]]): The product
                or list of products to add.
            user (User): The user for whom to add the products.

        Returns:
            Union[int, List[int]]: The product ID(s) that were added
                to the cart.
        """
        if isinstance(products, list):
            async with uow:
                result = await self.add_many(uow, products, user)
        else:
            async with uow:
                result = await self.add_one(uow, products, user)
        return result

    async def add_one(
        self, uow: UOWDependency, product: CartCreate, user: User
    ):
        """Add a single product to the user's cart.

        Args:
            uow (UOWDependency): The unit of work dependency.
            product (CartCreate): The product to add.
            user (User): The user for whom to add the product.

        Returns:
            int: The product ID that was added to the cart.
        """
        cart_dict = product.model_dump()
        cart_dict["owner_id"] = user.id
        is_product_in_cart, _product = await self.is_in_cart(
            uow, product.product_id, user
        )
        validator = ProductInCartValidator()
        validator(is_product_in_cart)
        cart_dict["price"] = _product.price * product.quantity
        await uow.cart.add(cart_dict)
        await uow.commit()
        return product.product_id

    async def add_many(
        self, uow: UOWDependency, products: List[CartCreate], user: User
    ):
        """Add multiple products to the user's cart.

        Args:
            uow (UOWDependency): The unit of work dependency.
            products (List[CartCreate]): The list of products to add.
            user (User): The user for whom to add the products.

        Returns:
            List[int]: The list of product IDs that were added to the cart.
        """
        result = []
        for product in products:
            product_id = await self.add_one(uow, product, user)
            result.append(product_id)
        return result

    @staticmethod
    async def get_all(uow: UOWDependency, user: User):
        """Get all products from the user's cart.

        Args:
            uow (UOWDependency): The unit of work dependency.
            user (User): The user for whom to retrieve the cart items.

        Returns:
            List: The list of cart items.
        """
        async with uow:
            return await uow.cart.get_all(user)

    @staticmethod
    async def get(uow: UOWDependency, product_id: int, user: User):
        """Get a specific product from the user's cart.

        Args:
            uow (UOWDependency): The unit of work dependency.
            product_id (int): The ID of the product to retrieve.
            user (User): The user for whom to retrieve the cart item.

        Returns:
            dict: The cart item.
        """
        async with uow:
            result = await uow.cart.get_by_product_id(product_id, user)
            if result is not None:
                return result

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

    async def update(
        self,
        uow: UOWDependency,
        product_id: int,
        product: CartUpdate,
        user: User,
    ):
        """Update the quantity of a product in the user's cart.

        Args:
            uow (UOWDependency): The unit of work dependency.
            product_id (int): The ID of the product to update.
            product (CartUpdate): The updated product information.
            user (User): The user for whom to update the cart item.

        Returns:
            int: The updated product ID.
        """
        product_dict = product.model_dump()
        is_product_in_cart, _product = await self.is_in_cart(
            uow, product_id, user
        )
        if is_product_in_cart is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )
        product_dict["price"] = _product.price * product.quantity
        async with uow:
            await uow.cart.update_by_product_id(product_id, product_dict, user)
            await uow.commit()
            return product_id

    @staticmethod
    async def delete(uow: UOWDependency, product_id: int, user: User):
        """Remove a product from the user's cart.

        Args:
            uow (UOWDependency): The unit of work dependency.
            product_id (int): The ID of the product to remove.
            user (User): The user for whom to remove the cart item.

        Returns:
            dict: The result of the deletion operation.
        """
        async with uow:
            result = await uow.cart.delete_by_owner_id_and_product_id(
                product_id, user
            )
            await uow.commit()
            return result

    @staticmethod
    async def delete_all(uow: UOWDependency, user: User):
        """Remove all products from the user's cart.

        Args:
            uow (UOWDependency): The unit of work dependency.
            user (User): The user for whom to remove all cart items.

        Returns:
            dict: The result of the deletion operation.
        """
        async with uow:
            result = await uow.cart.delete_all_by_owner_id(user)
            await uow.commit()
            return result

    @staticmethod
    async def get_total_price(uow: UOWDependency, user: User) -> float:
        """Get the total price of all products in the user's cart.

        Args:
            uow (UOWDependency): The unit of work dependency.
            user (User): The user for whom to calculate the total price.

        Returns:
            float: The total price of all products in the cart.
        """
        async with uow:
            total_price = await uow.cart.get_total_price(user)
            if total_price is not None:
                return total_price

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart is empty",
            )

    @staticmethod
    async def is_in_cart(uow, product_id, user):
        """Check if a product is already in the user's cart.

        Args:
            uow: The unit of work dependency.
            product_id: The ID of the product to check.
            user: The user for whom to check the cart.

        Returns:
            tuple: A tuple containing a boolean indicating if the
                product is in the cart and the product information.
        """
        try:
            _product = await ProductsService().get(uow, product_id, user)
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        is_product_in_cart = await uow.cart.get_by_product_id(product_id, user)
        return is_product_in_cart, _product
