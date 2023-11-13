from app.models import Product
from app.utils.repository import BaseRepository


class ProductsRepository(BaseRepository):
    model = Product
