import os

from fastapi import APIRouter, Body, Depends, Form, UploadFile
from sqlalchemy.orm import Session

from database.config import get_db
from database.models import Posts
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