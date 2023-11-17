"""Database model representing a product."""

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import BaseModel
from app.schemas.products import ProductRead


class Product(BaseModel):
    """Database model representing a product.

    Attributes:
        id (int): The primary key of the product.
        name (str): The name of the product.
        description (str): The description of the product.
        price (float): The price of the product.
        owner_id (int): The foreign key referencing the owner (user)
            of the product.
        is_active (bool): Indicates whether the product is active.
        created_at (datetime): The timestamp when the product was
            created.
        updated_at (datetime): The timestamp when the product was
            last updated.
    """

    __tablename__ = "product"

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[float] = mapped_column(Float, server_default="0.00")
    owner_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id"), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )

    def to_pydantic_model(self):
        """Convert the database model to a Pydantic model (ProductRead).

        Returns:
            ProductRead: The Pydantic model representing the product.
        """
        return ProductRead(
            id=self.id,
            name=self.name,
            description=self.description,
            price=self.price,
            owner_id=self.owner_id,
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
