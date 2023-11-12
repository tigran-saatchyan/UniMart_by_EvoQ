import os
from pathlib import Path
from typing import ClassVar, Type

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "True")

    ACCESS_TOKEN_MINUTES = 60
    REFRESH_TOKEN_DAYS = 90

    # FastAPI settings
    FASTAPI_SETTINGS: ClassVar[dict[str, str | int | bool | dict]] = {
        "docs_url": "/docs",
        "redoc_url": "/",
        "debug": DEBUG,
    }

    # Email settings
    DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
    EMAIL_PORT = os.getenv("EMAIL_PORT")
    EMAIL_USE_TLS = True

    # Database
    POSTGRES_DB = os.getenv("POSTGRES_DB", "unimart_db")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

    DATABASE_DRIVER = os.getenv("DATABASE_DRIVER", "postgresql+asyncpg")
    DATABASE_LOGIN = f"://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    DATABASE_CONNECT = f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    DATABASE_URI = DATABASE_DRIVER + DATABASE_LOGIN + DATABASE_CONNECT

    # Allowed hosts
    ALLOWED_HOSTS: ClassVar = ["*"]

    ALL_HOSTS = "http://*"

    # CORS settings
    CORS_ALLOWED_ORIGINS: ClassVar = [
        os.getenv("CORS_ALLOWED_HOST", ALL_HOSTS)
    ]
    CORS_ALLOW_ALL_ORIGINS: ClassVar = os.getenv(
        "CORS_ALLOW_ALL_ORIGINS", "False"
    ).lower() in (
        "true",
        "1",
        "True",
    )

    # CSRF protection settings
    CSRF_TRUSTED_ORIGINS: ClassVar = [
        os.getenv("CSRF_TRUSTED_FRONTEND", ALL_HOSTS),
        os.getenv("CSRF_TRUSTED_BACKEND", ALL_HOSTS),
    ]

    # jwt secret and algorithm
    JWT_SECRET = "$CekpeTHo$"
    JWT_ALGORITHM = "HS256"

    # hashing parameters
    CRYPTOGRAPHIC_HASH_FUNCTION = "sha256"
    PWD_HASH_SALT = b"top_secret_salt_and_pepper"
    PWD_HASH_ITERATIONS = 100_000


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False


class ConfigFactory:
    fastapi_env = os.getenv("FASTAPI_ENV")

    @classmethod
    def get_config(cls) -> Type[Config]:
        if cls.fastapi_env == "development":
            env_config = DevelopmentConfig
        elif cls.fastapi_env == "production":
            env_config = ProductionConfig
        elif cls.fastapi_env == "testing":
            env_config = TestingConfig
        else:
            raise NotImplementedError

        return env_config


config = ConfigFactory.get_config()
