from app.api.v1.dependencies import UOWDependency
from app.models import User
from app.schemas.products import ProductsCreate, ProductsUpdate


class ProductsService:
    @staticmethod
    async def add(
        uow: UOWDependency, product: ProductsCreate, user: User
    ) -> int:
        product_dict = product.model_dump()
        product_dict["owner_id"] = user.id
        async with uow:
            product_id = await uow.products.add(product_dict)
            await uow.commit()
            return product_id

    @staticmethod
    async def get_all(uow: UOWDependency, user: User):
        async with uow:
            return await uow.products.get_all(user)

    @staticmethod
    async def get(uow: UOWDependency, product_id: int, user: User):
        async with uow:
            return await uow.products.get(product_id, user)

    @staticmethod
    async def update(
        uow: UOWDependency,
        product_id: int,
        product: ProductsUpdate,
        user: User,
    ):
        product_dict = product.model_dump()
        async with uow:
            await uow.products.update(product_id, product_dict, user)
            await uow.commit()
            return product_id

    @staticmethod
    async def delete(uow: UOWDependency, product_id: int, user: User):
        async with uow:
            result = await uow.products.delete(product_id, user)
            await uow.commit()
            return result
