import os

from fastapi import APIRouter, Body, Depends, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from database.config import get_db
from database.models import Posts, Users
from utils.auth import get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/")
async def create_post(
    content=Form(...),
    file: UploadFile = Form(...),
    user=Depends(get_current_user),
    database: Session = Depends(get_db),
):
    """Function to create a post in database with picture"""

    picture = await file.read()

    if file.filename:
        with open(os.path.join("pictures", file.filename), "wb") as pictures_folder:
            pictures_folder.write(picture)
        post = Posts(content=content, picture=file.filename, user_id=user.id)

        database.add(post)
        database.commit()
        database.refresh(post)

        return post


@router.get("/{username}")
async def get_posts_by_username(username: str, database: Session = Depends(get_db)):
    """Function to get all posts in database by username"""

    user = database.query(Users).filter(Users.username == username).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User does not exist.")

    posts = database.query(Posts).filter(Posts.user_id == user.id).all()

    response = []

    for post in posts:
        comments = []

        for comment in post.comments:
            comment_author = (
                database.query(Users).filter(Users.id == comment.author_id).first()
            )

            if comment_author:
                comments.append(
                    {
                        "created_at": comment.created_at,
                        "post_id": comment.post_id,
                        "author_id": comment_author.id,
                        "first_name": comment_author.first_name,
                        "last_name": comment_author.last_name,
                        "username": comment_author.username,
                        "picture": comment_author.picture,
                    }
                )

        response.append({"post": post, "comments": comments})

    return response


#
# @router.get('/')
# async def get_posts(user= Depends(get_current_user), database=Depends(get_db)):
#
#
