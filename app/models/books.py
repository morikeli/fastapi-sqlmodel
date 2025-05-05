from datetime import date
from sqlmodel import Field, Relationship, SQLModel
from typing import List, Optional
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

    # relationships
    user: Optional["User"] = Relationship(back_populates="books")
    reviews: List["Review"] = Relationship(back_populates="books", sa_relationship_kwargs={'lazy': 'selectin'})



    def __repr__(self):
        return f"<Book(title={self.title}, author={self.author})>"


# Resolve forward reference
Book.model_rebuild()


class Review(SQLModel, TimeStampMixin, table=True):
    __tablename__ = "reviews"

    id: str = Field(
        default_factory=lambda: uuid.uuid4().hex,
        sa_type=sa.String(50),
        primary_key=True,
        unique=True,
        nullable=False,
    )
    review_text: str
    rating: int = Field(le=5)
    user_id: Optional[str] = Field(..., foreign_key='users.id') 
    book_id: Optional[str] = Field(..., foreign_key='books.id') 

    # relationship
    user: Optional["User"] = Relationship(back_populates="reviews")
    books: Optional["Book"] = Relationship(back_populates="reviews")


    def __repr__(self):
        return f"<Review(book_id={self.book_id}, user_id={self.user_id})>"
