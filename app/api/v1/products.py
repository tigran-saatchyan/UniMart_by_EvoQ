"""API endpoints for products."""

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
    """Add a new product.

    Args:
        user (User): The authenticated user.
        product (ProductsCreate): The product information to be added.
        uow (UOWDependency): Unit of Work dependency.

    Returns:
        int: The ID of the added product.
    """
    return await ProductsService().add(uow, product, user)


@router.get("/")
async def get_products(
    uow: UOWDependency,
    user: Annotated[User, Depends(current_user)],
):
    """Get all products.

    Args:
        uow (UOWDependency): Unit of Work dependency.
        user (User): The authenticated user.

    Returns:
        List: List of products.
    """
    return await ProductsService().get_all(uow, user)


@router.get("/{product_id}")
async def get_product(
    product_id: int,
    uow: UOWDependency,
    user: Annotated[User, Depends(current_user)],
):
    """Get details of a specific product.

    Args:
        product_id (int): ID of the product to retrieve.
        uow (UOWDependency): Unit of Work dependency.
        user (User): The authenticated user.

    Returns:
        dict: Details of the requested product.
    """
    return await ProductsService().get(uow, product_id, user)


@router.patch("/{product_id}")
async def update_product(
    product_id: int,
    product: ProductsUpdate,
    uow: UOWDependency,
    user: Annotated[User, Depends(current_user)],
):
    """Update a product.

    Args:
        product_id (int): ID of the product to update.
        product (ProductsUpdate): Updated product information.
        uow (UOWDependency): Unit of Work dependency.
        user (User): The authenticated user.

    Returns:
        dict: A message indicating the success of the update.
    """
    await ProductsService().update(uow, product_id, product, user)
    return {"message": "Product updated successfully"}


@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    uow: UOWDependency,
    user: Annotated[User, Depends(current_user)],
):
    """Delete a product.

    Args:
        product_id (int): ID of the product to delete.
        uow (UOWDependency): Unit of Work dependency.
        user (User): The authenticated user.

    Returns:
        dict: A message indicating the success of the deletion.
    """
    await ProductsService().delete(uow, product_id, user)
    return {"message": "Product deleted successfully"}
