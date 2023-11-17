from typing import Annotated, List, Union

from fastapi import APIRouter, Depends

from app.api.v1.dependencies import UOWDependency, current_user
from app.models import User
from app.schemas.cart import CartCreate, CartUpdate
from app.services.cart import CartService

router = APIRouter(
    prefix="/cart",
    tags=["Cart"],
)


@router.post("/")
async def add_product_to_cart(
    user: Annotated[User, Depends(current_user)],
    product: Union[CartCreate, List[CartCreate]],
    uow: UOWDependency,
) -> Union[int, List[int]]:
    return await CartService().add(uow, product, user)


@router.get("/get_all/")
async def get_all_products_from_cart(
    uow: UOWDependency,
    user: Annotated[User, Depends(current_user)],
):
    return await CartService().get_all(uow, user)


@router.get("/{product_id}")
async def get_one_product_from_cart(
    uow: UOWDependency,
    product_id: int,
    user: Annotated[User, Depends(current_user)],
):
    return await CartService().get(uow, product_id, user)


@router.patch("/{product_id}")
async def update_product_quantity(
    uow: UOWDependency,
    product_id: int,
    product: CartUpdate,
    user: Annotated[User, Depends(current_user)],
):
    return await CartService().update(uow, product_id, product, user)


@router.delete("/{product_id}")
async def remove_product_from_cart(
    uow: UOWDependency,
    product_id: int,
    user: Annotated[User, Depends(current_user)],
):
    return await CartService().delete(uow, product_id, user)


@router.delete("/clear_cart/")
async def clear_cart(
    uow: UOWDependency,
    user: Annotated[User, Depends(current_user)],
):
    return await CartService().delete_all(uow, user)


@router.get("/total_price/")
async def get_total_cart_price(
    user: Annotated[User, Depends(current_user)],
    uow: UOWDependency,
) -> float:
    return await CartService().get_total_price(uow, user)
