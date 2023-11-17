from httpx import AsyncClient
from starlette import status

from tests.conftest import login_user


class TestUsers:
    @staticmethod
    async def test_get_current_user(ac: AsyncClient):
        auth_cookies = await login_user(ac)
        response = await ac.get(
            "/users/me",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Cookie": "unimartcookie=" + auth_cookies["unimartcookie"],
            },
        )

        assert response.status_code == status.HTTP_200_OK
