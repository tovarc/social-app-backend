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


class FriendshipStatusEnum(PyEnum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DENIED = "denied"


FriendshipStatusType = Enum(
    FriendshipStatusEnum,
    name="friendship_status_type",
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

    posts = relationship("Posts", back_populates="author")
    comments = relationship("Comments", back_populates="author")


class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    content = Column(String)
    picture = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # user: Mapped["Users"] = relationship(back_populates="posts")

    author = relationship("Users", back_populates="posts")
    comments = relationship("Comments", back_populates="post")


class Friendship(Base):
    __tablename__ = "friendship"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    friend_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


class FriendRequest(Base):
    __tablename__ = "friend_requests"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    receiver_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(FriendshipStatusType, default="pending")


class Comments(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    post_id = Column(Integer, ForeignKey("posts.id"))
    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("Users", back_populates="comments")
    post = relationship("Posts", back_populates="comments")
