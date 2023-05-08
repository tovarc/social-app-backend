from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.config import get_db

from utils.auth import get_current_user


router = APIRouter(prefix="/photos", tags=["Photos"])


@router.get("/")
async def get_profile_photos(
    user=Depends(get_current_user), database: Session = Depends(get_db)
):
    return "Working"
