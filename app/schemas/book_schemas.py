from pydantic import BaseModel


class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: str
    language: str
    page_count: int
    

class UpdateBookSchema(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str
