"""Authentication routes for the FastAPI application."""

from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from app.models import User
from app.schemas.users import UserCreate, UserRead, UserUpdate
from app.services.managers import get_user_manager
from app.settings.auth import auth_backend

PREFIX = "/api/v1"
AUTH_TAG = "Authentication"


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


def set_up_auth_routes(application: FastAPI):
    """Set up authentication routes for the FastAPI application.

    Args:
        application (FastAPI): The FastAPI application instance.
    """
    application.include_router(
        fastapi_users.get_auth_router(auth_backend),
        prefix=f"{PREFIX}/jwt",
        tags=[AUTH_TAG],
    )
    application.include_router(
        fastapi_users.get_register_router(UserRead, UserCreate),
        prefix=PREFIX,
        tags=[AUTH_TAG],
    )
    application.include_router(
        fastapi_users.get_users_router(UserRead, UserUpdate),
        prefix="/users",
        tags=["Users"],
    )
