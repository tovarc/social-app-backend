from enum import Enum as PyEnum
from typing import List

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import Enum

from .config import Base


class GenderEnum(PyEnum):
    MALE = "male"
    FEMALE = "female"


GenderType = Enum(
    GenderEnum,
    name="gender_type",
    values_callable=lambda obj: [item.value for item in obj],
)


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    first_name = Column(String)
    last_name = Column(String)
    email = Column(String(length=40), unique=True)
    password = Column(String)
    username = Column(String(length=30), unique=True)
    birthday = Column(String)
    gender = Column(GenderType)
    about = Column(String)
    picture = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    posts: Mapped[List["Posts"]] = relationship(back_populates="user")


class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    content = Column(String)
    picture = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["Users"] = relationship(back_populates="posts")
