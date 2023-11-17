from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.v1.dependencies import UOWDependency, current_user
from app.models import User
from app.schemas.products import ProductsCreate, ProductsUpdate
from app.services.products import ProductsService

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post("/")
async def add_product(
    user: Annotated[User, Depends(current_user)],
    product: ProductsCreate,
    uow: UOWDependency,
) -> int:
    return await ProductsService().add(uow, product, user)


@router.get("/")
async def get_products(
    uow: UOWDependency,
    user: Annotated[User, Depends(current_user)],
):
    return await ProductsService().get_all(uow, user)


@router.get("/{product_id}")
async def get_product(
    product_id: int,
    uow: UOWDependency,
    user: Annotated[User, Depends(current_user)],
):
    return await ProductsService().get(uow, product_id, user)


@router.patch("/{product_id}")
async def update_product(
    product_id: int,
    product: ProductsUpdate,
    uow: UOWDependency,
    user: Annotated[User, Depends(current_user)],
):
    await ProductsService().update(uow, product_id, product, user)
    return {"message": "Product updated successfully"}


@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    uow: UOWDependency,
    user: Annotated[User, Depends(current_user)],
):
    await ProductsService().delete(uow, product_id, user)
    return {"message": "Product deleted successfully"}
