from typing import Annotated

from fastapi import Depends

from app.api.v1.auth import fastapi_users
from app.utils.unitofwork import IUnitOfWork, UnitOfWork

UOWDependency = Annotated[IUnitOfWork, Depends(UnitOfWork)]

current_user = fastapi_users.current_user()
