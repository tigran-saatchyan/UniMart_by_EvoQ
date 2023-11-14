from fastapi import APIRouter

from app.api.v1.dependencies import UOWDependency
from app.schemas.users import UsersSchemaAdd
from app.services.users import UsersService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/register")
async def register_user(user: UsersSchemaAdd, uow: UOWDependency):
    return await UsersService().add(uow, user)


# router.post("/login")
