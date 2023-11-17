from typing import List, Union, overload

from fastapi import HTTPException, status
from sqlalchemy.exc import NoResultFound

from app.api.v1.dependencies import UOWDependency
from app.models import User
from app.schemas.cart import CartCreate, CartUpdate
from app.services.products import ProductsService
from app.services.validators import (
    ProductInCartValidator,
)


class CartService:
    @overload
    def add(self, uow: UOWDependency, product: CartCreate, user: User) -> int:
        pass

    @overload
    def add(
        self, uow: UOWDependency, products: List[CartCreate], user: User
    ) -> List[int]:
        pass

    async def add(
        self,
        uow: UOWDependency,
        products: Union[CartCreate, List[CartCreate]],
        user: User,
    ) -> Union[int, List[int]]:
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
        result = []
        for product in products:
            product_id = await self.add_one(uow, product, user)
            result.append(product_id)
        return result

    @staticmethod
    async def get_all(uow: UOWDependency, user: User):
        async with uow:
            return await uow.cart.get_all(user)

    @staticmethod
    async def get(uow: UOWDependency, product_id: int, user: User):
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
        async with uow:
            result = await uow.cart.delete_by_owner_id_and_product_id(
                product_id, user
            )
            await uow.commit()
            return result

    @staticmethod
    async def delete_all(uow: UOWDependency, user: User):
        async with uow:
            result = await uow.cart.delete_all_by_owner_id(user)
            await uow.commit()
            return result

    @staticmethod
    async def get_total_price(uow: UOWDependency, user: User) -> float:
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
        try:
            _product = await ProductsService().get(uow, product_id, user)
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        is_product_in_cart = await uow.cart.get_by_product_id(product_id, user)
        return is_product_in_cart, _product
