from datetime import date
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.dialects.sqlite as sq
import uuid

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

    # relationship
    user: Optional["User"] = Relationship(back_populates="books")


    def __repr__(self):
        return f"<Book(title={self.title}, author={self.author})>"


# 
Book.model_rebuild()
