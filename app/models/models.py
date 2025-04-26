from datetime import date, datetime, timezone
from sqlmodel import Column, Field, SQLModel
from sqlalchemy import event
import sqlalchemy.dialects.sqlite as sq
import uuid


class Book(SQLModel, table=True):
    __tablename__ = "books"

    id: str = Field(sa_column=Column(sq.TEXT, nullable=False, primary_key=True, unique=True, default=lambda: uuid.uuid4().hex))
    title: str
    author: str
    publisher: str
    published_date: date
    language: str
    page_count: int
    created_at: datetime = Field(sa_column=Column(sq.TIMESTAMP, default=lambda: datetime.now(timezone.utc)))
    updated_at: datetime = Field(sa_column=Column(sq.TIMESTAMP, default=lambda: datetime.now(timezone.utc)))
    

    def __repr__(self):
        return f"<Book(title={self.title}, author={self.author})>"
    

@event.listens_for(Book, "before_update", propagate=True)
def update_timestamp(mapper, connection, target):
    """Automatically update the `updated_at` and `created_at` fields when a Book is updated."""
    target.updated_at = datetime.now(timezone.utc)
