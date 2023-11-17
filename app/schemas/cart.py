"""Pydantic models representing the shopping cart."""

from datetime import datetime

from pydantic import BaseModel, Field


class CartRead(BaseModel):
    """Pydantic model representing a read-only view of a shopping cart item.

    Attributes:
        id (int): The unique identifier of the cart item.
        quantity (int): The quantity of the product in the cart.
        product_id (int): The ID of the associated product.
        price (float): The price of the cart item.
        owner_id (int): The ID of the owner (user) of the cart.
        is_active (bool): Indicates whether the cart item is active.
        created_at (datetime): The timestamp when the cart item was created.
        updated_at (datetime): The timestamp when the cart item was
            last updated.

    Config:
        from_attributes (bool): Enable attribute assignment from
            class attributes.
    """

    id: int
    quantity: int
    product_id: int
    price: float
    owner_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CartCreate(BaseModel):
    """Pydantic model representing the creation of a shopping cart item.

    Attributes:
        quantity (int): The quantity of the product in the cart
            (default: 1).
        product_id (int): The ID of the associated product.

    Config:
        ge (int): Quantity must be greater than or equal to 0.
    """

    quantity: int = Field(1, ge=0)
    product_id: int


class CartUpdate(BaseModel):
    """Pydantic model representing the update of a shopping cart item.

    Attributes:
        quantity (int): The new quantity of the product in the
            cart (default: 1).

    Config:
        gt (int): Quantity must be greater than 0.
    """

    quantity: int = Field(1, gt=0)
