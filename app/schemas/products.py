from datetime import datetime

from pydantic import BaseModel


class ProductSchema(BaseModel):
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


class ProductsSchemaAdd(BaseModel):
    name: str
    description: str
    price: float


class ProductsSchemaEdit(BaseModel):
    name: str
    description: str
    price: float
