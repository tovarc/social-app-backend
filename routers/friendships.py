from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from database.config import get_db
from database.models import FriendRequest, Friendship, Users
from utils.auth import get_current_user


router = APIRouter(prefix="/friendships", tags=["Friendship - Information"])


@router.post("/send")
async def send_friend_request(
    username: str,
    user=Depends(get_current_user),
    database: Session = Depends(get_db),
):
    db_username = database.query(Users).filter(Users.username == username).first()

    if not db_username:
        raise HTTPException(status_code=409, detail="User does not exist.")

    request_exists = (
        database.query(FriendRequest)
        .filter(
            FriendRequest.sender_id == user.id,
            FriendRequest.receiver_id == db_username.id,
        )
        .first()
    )

    if request_exists:
        raise HTTPException(status_code=409, detail="Friend request is already sent.")

    friendship_request = FriendRequest(sender_id=user.id, receiver_id=db_username.id)

    database.add(friendship_request)
    database.commit()
    database.refresh(friendship_request)

    return friendship_request


@router.post("/accept")
async def accept_friend_request(
    username: str, user=Depends(get_current_user), database: Session = Depends(get_db)
):
    db_username = database.query(Users).filter(Users.username == username).first()

    if db_username is None:
        raise HTTPException(status_code=409, detail="User does not exist.")

    db_friend_request = (
        database.query(FriendRequest)
        .filter(
            FriendRequest.sender_id == db_username.id,
            FriendRequest.receiver_id == user.id,
        )
        .first()
    )

    if db_friend_request is None:
        raise HTTPException(status_code=404, detail="Friend request does not exist.")

    db_friend_request.status = "accepted"

    friendship_1 = Friendship(user_id=user.id, friend_id=db_username.id)
    friendship_2 = Friendship(user_id=db_username.id, friend_id=user.id)

    database.add(friendship_1)
    database.add(friendship_2)
    database.commit()
    database.refresh(db_friend_request)

    return db_friend_request


@router.get("/requests")
async def get_friend_requests(user=Depends(get_current_user), database=Depends(get_db)):
    requests = (
        database.query(FriendRequest).filter(FriendRequest.receiver_id == user.id).all()
    )

    return requests


@router.get("/")
async def get_profile_friends(
    user=Depends(get_current_user), database: Session = Depends(get_db)
):
    friends = database.query(Friendship).filter(Friendship.user_id == user.id).all()

    return friends
