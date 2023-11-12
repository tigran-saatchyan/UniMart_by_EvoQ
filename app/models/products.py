from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import (
    BaseModel,
)
from app.schemas.products import ProductSchema


class Product(BaseModel):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[float] = mapped_column(
        Float(precision=2), server_default="0.00"
    )
    owner_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    owner: Mapped[int] = relationship("User", back_populates="products")
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )

    def to_pydantic_model(self):
        return ProductSchema.model_validate(self)
