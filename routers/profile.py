import os

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session

from database.config import get_db
from database.models import Users
from database.schemas import ProfileResponse, UserBaseUpdate
from utils.auth import get_current_user


router = APIRouter(prefix="/profile", tags=["Profile - Information"])


@router.post("/picture")
async def set_profile_picture(
    file: UploadFile,
    user=Depends(get_current_user),
    database: Session = Depends(get_db),
):
    """Function to set user profile picture"""

    content = await file.read()

    if file.filename:
        with open(os.path.join("pictures", file.filename), "wb") as pictures_folder:
            pictures_folder.write(content)

            database.query(Users).filter(Users.id == user.id).update(
                {"picture": file.filename}
            )
            database.commit()
            database.flush()

    return {"filename": file.filename}


@router.get("/{username}", response_model=ProfileResponse)
def get_profile(username: str, database: Session = Depends(get_db)):
    """Function to get user profile"""

    user_profile = database.query(Users).filter(Users.username == username).first()

    return user_profile


@router.get("/", response_model=ProfileResponse)
def get_current_profile(
    user=Depends(get_current_user), database: Session = Depends(get_db)
):
    """Function to get user profile logged in by JWT token"""
    # test

    user_profile = database.query(Users).filter(Users.id == user.id).first()

    return user_profile


#
# @router.get('/')
# async def test_profile():
#     return "hello world"
#
@router.post("/")
def update_profile(
    body: UserBaseUpdate,
    user=Depends(get_current_user),
    database: Session = Depends(get_db),
):
    database.query(Users).filter(Users.id == user.id).update(
        {
            "first_name": body.first_name,
            "last_name": body.last_name,
            "username": body.username,
            "about": body.about,
        }
    )

    database.commit()
