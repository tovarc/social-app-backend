from fastapi import APIRouter, Body, Depends, HTTPException
from database.config import get_db
from database.models import Comments, Posts

from utils.auth import get_current_user


router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/")
async def create_comment(
    body=Body(...), user=Depends(get_current_user), database=Depends(get_db)
):
    db_post = database.query(Posts).filter(Posts.id == body["post_id"]).first()

    if db_post is None:
        raise HTTPException(status_code=404, detail="Post does not exist")

    comment = Comments(
        post_id=body["post_id"], author_id=user.id, content=body["content"]
    )

    database.add(comment)
    database.commit()
    database.refresh(comment)

    return {"comment": comment, "author": comment.author}
