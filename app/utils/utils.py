"""Utility functions for the application."""

import base64
import hashlib
import hmac

from app.settings import config


def hash_password(password, pwd_salt=config.PWD_HASH_SALT):
    """Hash a password using PBKDF2-HMAC with a specified hash function,
    salt, and number of iterations.

    Args:
        password (str): The password to be hashed.
        pwd_salt (bytes): The salt to be used in the hashing process.

    Returns:
        dict: A dictionary containing the hashed password and salt.
    """
    hashed_password = hashlib.pbkdf2_hmac(
        hash_name=config.CRYPTOGRAPHIC_HASH_FUNCTION,
        password=password.encode("utf-8"),
        salt=pwd_salt,
        iterations=config.PWD_HASH_ITERATIONS,
        dklen=config.DK_LEN,
    )
    hashed_password = base64.b64encode(hashed_password)
    pwd_salt = base64.b64encode(pwd_salt)
    return {"hashed_password": hashed_password, "password_salt": pwd_salt}


async def compare_passwords(db_pwd, received_pwd, pwd_salt) -> bool:
    """Compare a stored hashed password with a newly hashed password.

    Args:
        db_pwd (str): The stored hashed password.
        received_pwd (str): The newly hashed password to be compared.
        pwd_salt (bytes): The salt used in the original hashing process.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    received_pwd = hash_password(received_pwd, pwd_salt)["hashed_password"]
    return hmac.compare_digest(db_pwd, received_pwd)
