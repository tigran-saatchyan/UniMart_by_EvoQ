"""Tests for the users endpoints."""

from httpx import AsyncClient
from starlette import status

from tests.conftest import login_user


class TestUsers:
    @staticmethod
    async def test_get_current_user(
        register_user, login_user, ac: AsyncClient
    ):
        """Test retrieving information about the current user.

        Args:
            ac (AsyncClient): The asynchronous HTTP client.

        Returns:
            None
        """
        response = await ac.get(
            "/users/me",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Cookie": "unimartcookie=" + ac.cookies["unimartcookie"],
            },
        )

        assert response.status_code == status.HTTP_200_OK
