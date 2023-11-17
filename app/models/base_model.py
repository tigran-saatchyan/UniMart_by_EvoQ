"""Base model class for all database models."""

from datetime import datetime

from sqlalchemy import TIMESTAMP, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class BaseModel(Base):
    """Base model class for all database models.

    Attributes:
        id (int): The primary key of the model.
        created_at (datetime): The timestamp when the model was created.
        updated_at (datetime): The timestamp when the model was last updated.
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
