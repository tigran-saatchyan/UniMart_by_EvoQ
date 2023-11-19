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
        assert response.json()["email"] == USER_EMAIL


class TestLoginLogout:
    async def test_login(self, register_user, ac: AsyncClient):
        """Test user login and logout endpoints.

        Args:
            ac (AsyncClient): The asynchronous HTTP client.

        Returns:
            None
        """
        login_response = await ac.post(
            "/api/v1/jwt/login",
            data={"username": USER_EMAIL, "password": USER_PASSWORD},
        )
        assert login_response.status_code == status.HTTP_204_NO_CONTENT
        assert "unimartcookie" in ac.cookies

    @staticmethod
    async def test_logout(register_user, login_user, ac: AsyncClient):
        logout_response = await ac.post(
            "/api/v1/jwt/logout",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Cookie": "unimartcookie=" + ac.cookies["unimartcookie"],
            },
        )
        assert logout_response.status_code == status.HTTP_204_NO_CONTENT
        assert "unimartcookie" not in ac.cookies
