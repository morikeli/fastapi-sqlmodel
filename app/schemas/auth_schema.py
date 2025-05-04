from pydantic import BaseModel, Field
from typing import List


class UserCreate(BaseModel):
    username: str = Field(max_length=10)
    email: str = Field(max_length=40)
    password: str = Field(min_length=8)


class UserLogin(BaseModel):
    email: str
    password: str


class EmailModel(BaseModel):
    email_addresses: List[str]


class PasswordResetModel(BaseModel):
    email: str


class ConfirmResetPasswordModel(BaseModel):
    new_password: str
    confirm_new_password: str
