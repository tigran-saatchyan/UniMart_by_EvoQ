"""Database module."""

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from app.settings import config

engine = create_async_engine(config.DATABASE_URI)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()


async def get_async_session():
    """Get an asynchronous database session.

    Yields:
        Session: An asynchronous database session.
    """
    async with async_session_maker() as session:
        yield session
