"""Tests for the product endpoints."""

from httpx import AsyncClient
from starlette import status

from tests.conftest import login_user


class TestProducts:
    @staticmethod
    async def test_add_product(ac: AsyncClient):
        """Test adding a new product.

        Args:
            ac (AsyncClient): The asynchronous HTTP client.

        Returns:
            None
        """
        auth_cookies = await login_user(ac)
        test_product = {
            "name": "Test product",
            "description": "Some description",
            "price": 1000,
        }

        response = await ac.post(
            "/products/",
            json=test_product,
            headers={
                "Content-Type": "application/json",
                "Cookie": "unimartcookie=" + auth_cookies["unimartcookie"],
            },
        )

        assert response.status_code == status.HTTP_201_CREATED
