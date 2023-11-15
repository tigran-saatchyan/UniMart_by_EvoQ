from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.v1.dependencies import UOWDependency, current_user
from app.models import User
from app.schemas.products import ProductsSchemaAdd, ProductsSchemaEdit
from app.services.products import ProductsService

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post("/")
async def add_product(
    user: Annotated[User, Depends(current_user)],
    product: ProductsSchemaAdd,
    uow: UOWDependency,
) -> int:
    return await ProductsService().add(uow, product, user)


@router.get("/", dependencies=[Depends(current_user)])
async def get_products(uow: UOWDependency):
    return await ProductsService().get_all(uow)


@router.get("/{product_id}", dependencies=[Depends(current_user)])
async def get_product(product_id: int, uow: UOWDependency):
    return await ProductsService().get(uow, product_id)


@router.patch("/{product_id}", dependencies=[Depends(current_user)])
async def update_product(
    product_id: int, product: ProductsSchemaEdit, uow: UOWDependency
):
    await ProductsService().update(uow, product_id, product)
    return {"message": "Product updated successfully"}


@router.delete("/{product_id}", dependencies=[Depends(current_user)])
async def delete_product(product_id: int, uow: UOWDependency):
    await ProductsService().delete(uow, product_id)
    return {"message": "Product deleted successfully"}
