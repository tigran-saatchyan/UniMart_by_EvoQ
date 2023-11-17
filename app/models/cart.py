"""Database model representing a shopping cart."""

from sqlalchemy import Boolean, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models import BaseModel
from app.schemas.cart import CartRead


class Cart(BaseModel):
    """Database model representing a shopping cart.

    Attributes:
        id (int): The primary key of the cart.
        price (float): The total price of the products in the cart.
        quantity (int): The quantity of the product in the cart.
        product_id (int): The foreign key referencing the associated
            product.
        owner_id (int): The foreign key referencing the owner (user)
            of the cart.
        is_active (bool): Indicates whether the cart is active.
        created_at (datetime): The timestamp when the cart was created.
        updated_at (datetime): The timestamp when the cart was last
            updated.
    """

    __tablename__ = "cart"

    price: Mapped[float] = mapped_column(
        Float(precision=2), server_default="0.00"
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("product.id"), nullable=False
    )
    owner_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id"), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )

    def to_pydantic_model(self):
        """Convert the database model to a Pydantic model (CartRead).

        Returns:
            CartRead: The Pydantic model representing the cart.
        """
        return CartRead(
            id=self.id,
            price=self.price,
            quantity=self.quantity,
            product_id=self.product_id,
            owner_id=self.owner_id,
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
