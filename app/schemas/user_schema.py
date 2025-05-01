from pydantic import BaseModel
from typing import Optional


class UserResponse(BaseModel):
    id: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: str
    email: str
    is_verified: bool = False
