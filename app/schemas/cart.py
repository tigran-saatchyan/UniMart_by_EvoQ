from datetime import datetime

from pydantic import BaseModel, Field


class CartRead(BaseModel):
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
    quantity: int = Field(1, ge=0)
    product_id: int


class CartUpdate(BaseModel):
    quantity: int = Field(1, gt=0)
