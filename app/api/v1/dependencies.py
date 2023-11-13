from typing import Annotated

from fastapi import Depends

from app.utils.unitofwork import IUnitOfWork, UnitOfWork

UOWDependency = Annotated[IUnitOfWork, Depends(UnitOfWork)]
