"""Pydantic models representing the products schema."""

from datetime import datetime

from pydantic import BaseModel


class ProductRead(BaseModel):
    """Pydantic model representing a read-only view of a product.

    Attributes:
        id (int): The unique identifier of the product.
        name (str): The name of the product.
        description (str): The description of the product.
        price (float): The price of the product.
        owner_id (int): The ID of the owner (user) of the product.
        is_active (bool): Indicates whether the product is active.
        created_at (datetime): The timestamp when the product was
            created.
        updated_at (datetime): The timestamp when the product was
            last updated.

    Config:
        from_attributes (bool): Enable attribute assignment from
            class attributes.
    """

    id: int
    name: str
    description: str
    price: float
    owner_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductsCreate(BaseModel):
    """Pydantic model representing the creation of a product.

    Attributes:
        name (str): The name of the product.
        description (str): The description of the product.
        price (float): The price of the product.
    """

    name: str
    description: str
    price: float


class ProductsUpdate(BaseModel):
    """Pydantic model representing the update of a product.

    Attributes:
        name (str): The new name of the product.
        description (str): The new description of the product.
        price (float): The new price of the product.
    """

    name: str
    description: str
    price: float
