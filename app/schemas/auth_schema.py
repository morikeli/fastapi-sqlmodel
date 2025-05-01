from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(max_length=10)
    email: str = Field(max_length=40)
    password: str = Field(min_length=8)


class UserLogin(BaseModel):
    email: str
    password: str
