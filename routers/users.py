from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.config import get_db
from database.models import Friendship, Users

from utils.auth import get_current_user


router = APIRouter(prefix="/users", tags=["Global Users"])


@router.get("/")
async def get_all_users(
    user=Depends(get_current_user), database: Session = Depends(get_db)
):
    db_users = database.query(Users).all()

    response = []

    for db_user in db_users:
        friendship = (
            database.query(Friendship)
            .filter(Friendship.user_id == user.id, Friendship.friend_id == db_user.id)
            .first()
        )

        response.append(
            {
                "first_name": db_user.first_name,
                "last_name": db_user.last_name,
                "username": db_user.username,
                "picture": db_user.picture,
                "friendship": False if friendship is None else True,
            }
        )

    return response
