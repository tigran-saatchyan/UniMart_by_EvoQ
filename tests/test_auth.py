"""Test authentication endpoints."""

from httpx import AsyncClient
from starlette import status

from tests.conftest import USER_DATA, USER_EMAIL, USER_PASSWORD


class TestAuth:
    @staticmethod
    async def test_register(ac: AsyncClient):
        """Test user registration endpoint.

        Args:
            ac (AsyncClient): The asynchronous HTTP client.

        Returns:
            None
        """
        response = await ac.post(
            "/api/v1/register",
            json=USER_DATA,
        )

        assert response.status_code == status.HTTP_201_CREATED


class TestLogin:
    async def test_login_and_logout(self, ac: AsyncClient):
        """Test user login and logout endpoints.

        Args:
            ac (AsyncClient): The asynchronous HTTP client.

        Returns:
            None
        """
        await ac.post(
            "/api/v1/register",
            json=USER_DATA,
        )

        login_response = await ac.post(
            "/api/v1/jwt/login",
            data={"username": USER_EMAIL, "password": USER_PASSWORD},
        )
        auth_cookies = login_response.cookies
        assert login_response.status_code == status.HTTP_204_NO_CONTENT

        logout_response = await ac.post(
            "/api/v1/jwt/logout",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Cookie": "unimartcookie=" + auth_cookies["unimartcookie"],
            },
        )
        assert logout_response.status_code == status.HTTP_204_NO_CONTENT
