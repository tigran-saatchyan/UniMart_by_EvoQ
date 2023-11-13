from app.api.v1.dependencies import UOWDependency
from app.schemas.products import ProductsSchemaAdd, ProductsSchemaEdit


class ProductsService:
    @staticmethod
    async def add(uow: UOWDependency, product: ProductsSchemaAdd) -> int:
        product_dict = product.model_dump()
        async with uow:
            product_id = await uow.products.add(product_dict)
            await uow.commit()
            return product_id

    @staticmethod
    async def get_all(uow: UOWDependency):
        async with uow:
            return await uow.products.get_all()

    @staticmethod
    async def get(uow: UOWDependency, product_id: int):
        async with uow:
            return await uow.products.get(product_id)

    @staticmethod
    async def update(
        uow: UOWDependency, product_id: int, product: ProductsSchemaEdit
    ):
        product_dict = product.model_dump()
        async with uow:
            await uow.products.update(product_id, product_dict)
            await uow.commit()
            return product_id

    @staticmethod
    async def delete(uow: UOWDependency, product_id: int):
        async with uow:
            await uow.products.delete(product_id)
            await uow.commit()
