"""Validators for checking the validity of data."""

import re

from fastapi import HTTPException
from starlette import status


class PasswordValidator:
    """Validator for checking the validity of passwords.

    Args:
        password (str): The password to validate.
        confirm_password (str): The confirmation password.

    Raises:
        HTTPException: If the password is not valid or passwords do not match.
    """

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
    """Validator for checking the validity of telephone numbers.

    Args:
        telephone (str): The telephone number to validate.

    Raises:
        HTTPException: If the telephone number is not valid.
    """

    def __call__(self, telephone: str):
        if not re.search(r"^\+7\d{10}$", telephone):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The telephone number is not valid",
            )
        return True


class ProductInCartValidator:
    """Validator for checking if a product is already in the cart.

    Args:
        product: The product to check.

    Raises:
        HTTPException: If the product is already in the cart.
    """

    def __call__(self, product):
        if product is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product is already in cart",
            )
        return True
