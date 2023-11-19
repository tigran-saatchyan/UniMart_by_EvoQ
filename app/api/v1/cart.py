"""Cart API endpoints."""

from typing import Annotated, List, Union

from fastapi import APIRouter, Depends
from starlette import status

from app.api.v1.dependencies import UOWDependency, current_user
from app.models import User
from app.schemas.cart import CartCreate, CartUpdate
from app.services.cart import CartService

router = APIRouter(
    prefix="/cart",
    tags=["Cart"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_product_to_cart(
    user: Annotated[User, Depends(current_user)],
    product: Union[CartCreate, List[CartCreate]],
    uow: UOWDependency,
) -> Union[int, List[int]]:
    """Add one or multiple products to the user's cart.

    Args:
        user (User): The authenticated user.
        product (Union[CartCreate, List[CartCreate]]): The product(s)
            to be added to the cart.
        uow (UOWDependency): Unit of Work dependency.

    Returns:
        Union[int, List[int]]: The ID(s) of the added product(s) in the cart.
    """
    return await CartService().add(uow, product, user)


@router.get("/get_all/", status_code=status.HTTP_200_OK)
async def get_all_products_from_cart(
    uow: UOWDependency,
    user: Annotated[User, Depends(current_user)],
):
    """Get all products from the user's cart.

    Args:
        uow (UOWDependency): Unit of Work dependency.
        user (User): The authenticated user.

    Returns:
        List: List of products in the user's cart.
    """
    return await CartService().get_all(uow, user)


@router.get("/{product_id}", status_code=status.HTTP_200_OK)
async def get_one_product_from_cart(
    uow: UOWDependency,
    product_id: int,
    user: Annotated[User, Depends(current_user)],
):
    """Get details of a specific product in the user's cart.

    Args:
        uow (UOWDependency): Unit of Work dependency.
        product_id (int): ID of the product to retrieve.
        user (User): The authenticated user.

    Returns:
        dict: Details of the requested product in the cart.
    """
    return await CartService().get(uow, product_id, user)


@router.patch("/{product_id}", status_code=status.HTTP_200_OK)
async def update_product_quantity(
    uow: UOWDependency,
    product_id: int,
    product: CartUpdate,
    user: Annotated[User, Depends(current_user)],
):
    """Update the quantity of a product in the user's cart.

    Args:
        uow (UOWDependency): Unit of Work dependency.
        product_id (int): ID of the product to update.
        product (CartUpdate): Updated product information.
        user (User): The authenticated user.

    Returns:
        dict: Details of the updated product in the cart.
    """
    return await CartService().update(uow, product_id, product, user)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_product_from_cart(
    uow: UOWDependency,
    product_id: int,
    user: Annotated[User, Depends(current_user)],
):
    """Remove a product from the user's cart.

    Args:
        uow (UOWDependency): Unit of Work dependency.
        product_id (int): ID of the product to remove.
        user (User): The authenticated user.

    Returns:
        bool: True if the product is successfully removed.
    """
    return await CartService().delete(uow, product_id, user)


@router.delete("/clear_cart/", status_code=status.HTTP_204_NO_CONTENT)
async def clear_cart(
    uow: UOWDependency,
    user: Annotated[User, Depends(current_user)],
):
    """Clear all products from the user's cart.

    Args:
        uow (UOWDependency): Unit of Work dependency.
        user (User): The authenticated user.

    Returns:
        bool: True if the cart is successfully cleared.
    """
    return await CartService().delete_all(uow, user)


@router.get("/total_price/", status_code=status.HTTP_200_OK)
async def get_total_cart_price(
    user: Annotated[User, Depends(current_user)],
    uow: UOWDependency,
) -> float:
    """Get the total price of all products in the user's cart.

    Args:
        user (User): The authenticated user.
        uow (UOWDependency): Unit of Work dependency.

    Returns:
        float: The total price of all products in the cart.
    """
    return await CartService().get_total_price(uow, user)
