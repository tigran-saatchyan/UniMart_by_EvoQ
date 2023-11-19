"""Tests for the product endpoints."""

from httpx import AsyncClient
from starlette import status


class TestProducts:
    @staticmethod
    async def test_add_product(register_user, login_user, ac: AsyncClient):
        """Test adding a new product.

        Args:
            ac (AsyncClient): The asynchronous HTTP client.

        Returns:
            None
        """
        test_product = {
            "name": "Test product",
            "description": "Some description",
            "price": 1000.0,
        }

        response = await ac.post(
            "/products/",
            json=test_product,
            headers={
                "Content-Type": "application/json",
                "Cookie": "unimartcookie=" + ac.cookies["unimartcookie"],
            },
        )
        product_data = response.json()
        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in product_data
        assert product_data["name"] == test_product["name"]
        assert product_data["description"] == test_product["description"]
        assert product_data["price"] == test_product["price"]
