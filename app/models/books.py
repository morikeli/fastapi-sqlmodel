from datetime import date, datetime, timezone
from sqlmodel import Column, Field, Relationship, SQLModel
from sqlalchemy import event
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.dialects.sqlite as sq
import uuid

from app import models
from .base import TimeStampMixin


class Book(SQLModel, TimeStampMixin, table=True):
    __tablename__ = "books"

    id: str = Field(
        default_factory=lambda: uuid.uuid4().hex,
        sa_type=sa.String(50),
        primary_key=True,
        unique=True,
        nullable=False,
    )
    title: str
    author: str
    publisher: str
    published_date: date
    language: str
    user_id: Optional[str] = Field(..., foreign_key='users.id') 
    page_count: int
    

    def __repr__(self):
        return f"<Book(title={self.title}, author={self.author})>"
    

@event.listens_for(Book, "before_update", propagate=True)
def update_timestamp(mapper, connection, target):
    """Automatically update the `updated_at` and `created_at` fields when a Book is updated."""
    target.updated_at = datetime.now(timezone.utc)
