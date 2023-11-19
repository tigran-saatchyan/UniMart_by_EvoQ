"""Repository for interacting with the Product model in the database."""

from app.models import Product
from app.repositories.repository import BaseRepository


class ProductsRepository(BaseRepository):
    """Repository for interacting with the Product model in the database.

    Attributes:
        model: The Product model.
        session: The database session.
    """

    model = Product
