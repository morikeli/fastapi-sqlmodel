from .base import TimeStampMixin
from sqlmodel import Column, Field, SQLModel
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.dialects.sqlite as sq
import uuid


class User(SQLModel, TimeStampMixin, table=True):
    """
    User model for authentication and user management.
    Inherits from SQLModel, IDMixin and TimeStampMixin to provide
    additional functionality such as automatic ID generation
    and timestamp management.
    """
    __tablename__ = "users"


    id: str = Field(
        default_factory=lambda: uuid.uuid4().hex,
        sa_type=sa.String(50),
        primary_key=True,
        unique=True,
        nullable=False,
        
    )
    first_name: Optional[str]
    last_name: Optional[str]
    username: str
    email: str
    password: str = Field(exclude=True)     # hide password in response data
    user_role: str = Field(sa_column=Column(
        sq.VARCHAR(10),
        nullable=False,
        server_default="user",
    ))
    is_verified: bool = False


    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"
