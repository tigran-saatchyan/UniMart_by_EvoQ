import re

from fastapi import HTTPException
from starlette import status


class PasswordValidator:
    def __call__(self, password: str, confirm_password: str):
        if not re.search(r"^(?=.*[A-Z])(?=.*[$%&!]).{8,}$", password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The password is not valid",
            )
        if password != confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Passwords do not match",
            )
        return True


class TelephoneValidator:
    def __call__(self, telephone: str):
        if not re.search(r"^\+7\d{10}$", telephone):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The telephone number is not valid",
            )
        return True
