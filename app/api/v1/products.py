from fastapi import APIRouter

from app.api.v1.dependencies import UOWDependency
from app.schemas.products import ProductsSchemaAdd, ProductsSchemaEdit
from app.services.products import ProductsService

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post("/")
async def add_product(product: ProductsSchemaAdd, uow: UOWDependency) -> int:
    return await ProductsService().add(uow, product)


@router.get("/")
async def get_products(uow: UOWDependency):
    return await ProductsService().get_all(uow)


@router.get("/{product_id}")
async def get_product(product_id: int, uow: UOWDependency):
    return await ProductsService().get(uow, product_id)


@router.patch("/{product_id}")
async def update_product(
    product_id: int, product: ProductsSchemaEdit, uow: UOWDependency
):
    await ProductsService().update(uow, product_id, product)
    return {"message": "Product updated successfully"}


@router.delete("/{product_id}")
async def delete_product(product_id: int, uow: UOWDependency):
    await ProductsService().delete(uow, product_id)
    return {"message": "Product deleted successfully"}
