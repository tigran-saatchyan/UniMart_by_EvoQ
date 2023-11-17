"""Configuration classes for the application."""

import os
from pathlib import Path
from typing import ClassVar, Type

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    """Base configuration class for the application.

    Attributes:
        DEBUG (bool): Indicates whether the application is in debug mode.
        ACCESS_TOKEN_MINUTES (int): The expiration time for access
            tokens in minutes.
        REFRESH_TOKEN_DAYS (int): The expiration time for refresh
            tokens in days.
        FASTAPI_SETTINGS (ClassVar[dict]): FastAPI settings for the
            application.
        ... (Other attributes for email settings, database connection, etc.)

    """

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

    # Test database
    TEST_POSTGRES_DB = os.getenv("TEST_POSTGRES_DB")
    TEST_POSTGRES_USER = os.getenv("TEST_POSTGRES_USER")
    TEST_POSTGRES_PASSWORD = os.getenv("TEST_POSTGRES_PASSWORD")
    TEST_POSTGRES_HOST = os.getenv("TEST_POSTGRES_HOST")
    TEST_POSTGRES_PORT = os.getenv("TEST_POSTGRES_PORT")

    TEST_DATABASE_DRIVER = os.getenv("DATABASE_DRIVER", "postgresql+asyncpg")
    TEST_DATABASE_LOGIN = f"://{TEST_POSTGRES_USER}:{TEST_POSTGRES_PASSWORD}"
    TEST_DATABASE_CONNECT = (
        f"@{TEST_POSTGRES_HOST}:{TEST_POSTGRES_PORT}/{TEST_POSTGRES_DB}"
    )

    TEST_DATABASE_URI = (
        TEST_DATABASE_DRIVER + TEST_DATABASE_LOGIN + TEST_DATABASE_CONNECT
    )

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

    COOKIE_MAX_AGE = 3600

    # jwt secret and algorithm
    JWT_SECRET = "$CekpeTHo$"
    JWT_ALGORITHM = "HS256"

    # hashing parameters
    CRYPTOGRAPHIC_HASH_FUNCTION = "sha256"
    PWD_HASH_SALT = os.urandom(16)
    PWD_HASH_ITERATIONS = 100_000
    DK_LEN = 32


class DevelopmentConfig(Config):
    """Development-specific configuration class.

    Inherits from the base Config class.

    Attributes:
        DEBUG (bool): Indicates whether the application is in debug
            mode (set to True in development).
    """

    DEBUG = True


class TestingConfig(Config):
    """Testing-specific configuration class.

    Inherits from the base Config class.

    Attributes:
        DEBUG (bool): Indicates whether the application is in debug
            mode (set to True in testing).
        TESTING (bool): Indicates that the application is in testing mode.
    """

    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    """Production-specific configuration class.

    Inherits from the base Config class.

    Attributes:
        DEBUG (bool): Indicates whether the application is in debug
            mode (set to False in production).
    """

    DEBUG = False


class ConfigFactory:
    """Factory class for obtaining the appropriate configuration class
        based on the environment.

    Attributes:
        fastapi_env (str): The environment variable indicating the
            FastAPI environment.

    Methods:
        get_config(): Get the configuration class based on the
            FastAPI environment.

    Raises:
        NotImplementedError: If the FastAPI environment is not recognized.

    """

    fastapi_env = os.getenv("FASTAPI_ENV")

    @classmethod
    def get_config(cls) -> Type[Config]:
        """Get the configuration class based on the FastAPI environment.

        Returns:
            Type[Config]: The configuration class for the
                current environment.

        Raises:
            NotImplementedError: If the FastAPI environment is not recognized.
        """
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
