from fastapi import APIRouter

from app.api.v1.dependencies import UOWDependency
from app.schemas.users import UsersSchemaAdd, UsersSchemaEdit
from app.services.users import UsersService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/register")
async def register_user(user: UsersSchemaAdd, uow: UOWDependency):
    return await UsersService().add(uow, user)


@router.post("/update/{user_id}")
async def register_user(
    user_id: int, user: UsersSchemaEdit, uow: UOWDependency
):
    result = await UsersService().update(uow, user_id, user)
    if not result:
        return {"detail": "Nothing to update"}
    return {"detail": "User updated"}
