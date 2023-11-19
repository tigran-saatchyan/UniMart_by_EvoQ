"""Pytest configuration file for the application."""

import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from app.db import Base, get_async_session
from app.main import app
from app.settings import config

engine_test = create_async_engine(config.TEST_DATABASE_URI, poolclass=NullPool)
async_session_maker = async_sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)
Base.metadata.bind = engine_test

USER_EMAIL = "user3@example.com"
USER_PHONE = "+79999999999"
USER_PASSWORD = "Q1!string"

USER_DATA = {
    "email": USER_EMAIL,
    "password": USER_PASSWORD,
    "confirm_password": USER_PASSWORD,
    "first_name": "string",
    "last_name": "string",
    "telephone": USER_PHONE,
}


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Override the get_async_session dependency to use a testing session.

    Yields:
        AsyncSession: An asynchronous session for testing purposes.
    """
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(scope="function")
async def register_user(ac: AsyncClient):
    """Simulate user registration.

    Args:
        ac (AsyncClient): The asynchronous HTTP client.
    """
    await ac.post("/api/v1/register", json=USER_DATA)


@pytest.fixture(scope="function")
async def login_user(ac: AsyncClient):
    """Simulate user registration and login, returning the
        authentication cookies.

    Args:
        ac (AsyncClient): The asynchronous HTTP client.

    Returns:
        http.cookies: Authentication cookies.
    """
    response = await ac.post(
        "/api/v1/jwt/login",
        data={"username": USER_EMAIL, "password": USER_PASSWORD},
    )
    ac.cookies.update(response.cookies)

    return ac.cookies


@pytest.fixture(autouse=True, scope="class")
async def prepare_database():
    """Fixture to set up and tear down the test database."""
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    """AsyncClient fixture for testing asynchronous endpoints.

    Yields:
        AsyncClient: An asynchronous HTTP client for testing.
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
