from httpx import AsyncClient
from starlette import status

from tests.conftest import login_user


class TestCart:
    @staticmethod
    async def test_add_to_cart(ac: AsyncClient):
        auth_cookies = await login_user(ac)
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
                "Cookie": "unimartcookie=" + auth_cookies["unimartcookie"],
            },
        )

        response = await ac.post(
            "/cart/",
            json={"product_id": int(product.text), "quantity": 1},
            headers={
                "Content-Type": "application/json",
                "Cookie": "unimartcookie=" + auth_cookies["unimartcookie"],
            },
        )

        assert response.status_code == status.HTTP_200_OK

    @staticmethod
    async def test_get_all_from_cart(ac: AsyncClient):
        auth_cookies = await login_user(ac)

        response = await ac.get(
            "/cart/get_all/",
            headers={
                "Content-Type": "application/json",
                "Cookie": "unimartcookie=" + auth_cookies["unimartcookie"],
            },
        )

        assert response.status_code == status.HTTP_200_OK
