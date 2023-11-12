from pydantic import BaseModel


class ProductSchema(BaseModel):
    name: str
    description: str
    price: float
    is_active: bool

    class Config:
        from_attributes = True
