from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
import uuid


class ReviewModel(BaseModel):
    id: str
    rating: int = Field(le=5)
    review_text: str
    user_id: Optional[str]
    book_id: Optional[str]
    created_at: datetime
    updated_at: datetime


class ReviewCreate(BaseModel):
    rating: int = Field(le=5)
    review_text: str
