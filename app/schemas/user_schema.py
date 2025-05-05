from pydantic import BaseModel
from typing import List, Optional

from app.schemas.book_schemas import Book
from app.schemas.review_schema import ReviewModel


class UserResponse(BaseModel):
    id: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: str
    email: str
    is_verified: bool = False


class UserModel(UserResponse):
    books: List[Book]
    reviews: List[ReviewModel]
