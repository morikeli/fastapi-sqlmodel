from datetime import date, datetime
from pydantic import BaseModel, field_validator


class Book(BaseModel):
    id: str
    title: str
    author: str
    publisher: str
    published_date: date
    language: str
    page_count: int
    created_at: datetime
    updated_at: datetime


class BookCreateSchema(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str


    @field_validator("published_date", mode='before')
    def parse_published_date(cls, v):
        if isinstance(v, str):
            return datetime.strptime(v, "%Y-%m-%d").date()
        return v


class UpdateBookSchema(BaseModel):
    title: str
    author: str
    publisher: str
    language: str
    page_count: int
