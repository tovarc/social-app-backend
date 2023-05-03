from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str


# Base class is schema for request body
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    birthday: str
    gender: str
    username: str


class UserBaseUpdate(BaseModel):
    first_name: str
    last_name: str
    username: str
    about: str


# Schema class is schema for response body and db object
class UserSchema(UserBase):
    id: int

    # allows conversion between Pydantic and ORMs
    class Config:
        orm_mode = True


class ProfileResponse(BaseModel):
    first_name: str
    last_name: str
    email: str
    birthday: str
    username: str
    picture: Optional[str]
    about: Optional[str]

    class Config:
        orm_mode = True
