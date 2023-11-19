"""Tests for the cart endpoints."""

from httpx import AsyncClient
from starlette import status

from tests.conftest import login_user


class TestCart:
    @staticmethod
    async def test_add_to_cart(register_user, login_user, ac: AsyncClient):
        """Test adding a product to the user's cart.

        Args:
            ac (AsyncClient): The asynchronous HTTP client.

        Returns:
            None
        """
        test_product = {
            "name": "Test product",
            "description": "Some description",
            "price": 1000,
        }

        product = await ac.post(
            "/products/",
            json=test_product,
            headers={
                "Content-Type": "application/json",
                "Cookie": "unimartcookie=" + ac.cookies["unimartcookie"],
            },
        )

        response = await ac.post(
            "/cart/",
            json={"product_id": int(product.text), "quantity": 1},
            headers={
                "Content-Type": "application/json",
                "Cookie": "unimartcookie=" + ac.cookies["unimartcookie"],
            },
        )

        assert response.status_code == status.HTTP_201_CREATED

    @staticmethod
    async def test_get_all_from_cart(
        register_user, login_user, ac: AsyncClient
    ):
        """Test retrieving all products from the user's cart.

        Args:
            ac (AsyncClient): The asynchronous HTTP client.

        Returns:
            None
        """
        response = await ac.get(
            "/cart/get_all/",
            headers={
                "Content-Type": "application/json",
                "Cookie": "unimartcookie=" + ac.cookies["unimartcookie"],
            },
        )

        assert response.status_code == status.HTTP_200_OK
