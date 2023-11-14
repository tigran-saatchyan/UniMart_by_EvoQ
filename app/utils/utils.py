import base64
import hashlib
import hmac

from app.settings import config


def hash_password(password, pwd_salt=config.PWD_HASH_SALT):
    password_hash = hashlib.pbkdf2_hmac(
        hash_name=config.CRYPTOGRAPHIC_HASH_FUNCTION,
        password=password.encode("utf-8"),
        salt=pwd_salt,
        iterations=config.PWD_HASH_ITERATIONS,
        dklen=config.DK_LEN,
    )
    password_hash = base64.b64encode(password_hash)
    pwd_salt = base64.b64encode(pwd_salt)
    return {"password_hash": password_hash, "password_salt": pwd_salt}


async def compare_passwords(db_pwd, received_pwd, pwd_salt) -> bool:
    received_pwd = hash_password(received_pwd, pwd_salt)["password_hash"]
    return hmac.compare_digest(db_pwd, received_pwd)
