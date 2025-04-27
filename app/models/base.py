from datetime import datetime, timezone
from sqlmodel import Column, DateTime, Field, SQLModel, String, TIMESTAMP
from sqlalchemy.dialects import sqlite as sq
from sqlalchemy import func
from typing import Optional
import sqlalchemy as sa
import uuid


class IDMixin:
    """
    Mixin to add an ID primary key to a model.
    """
    
    id: str = Field(
        default_factory=lambda: uuid.uuid4().hex,
        sa_type=sa.String(50),
        primary_key=True,
        unique=True,
        nullable=False,
        
    )


class TimeStampMixin:
    """
    Mixin to add created_at and updated_at timestamps to a model.
    """
    
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=sa.TIMESTAMP(timezone=True),
        nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=sa.TIMESTAMP(timezone=True),
        nullable=False
    )
    