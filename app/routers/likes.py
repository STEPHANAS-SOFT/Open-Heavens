from fastapi import APIRouter
from app.models import LikeIn, LikeOut
from app import repos

router = APIRouter()

@router.post("/", response_model=LikeOut)
def create_like(l: LikeIn):
    new_id = repos.create_like(l)
    return {"id": new_id, **l.dict(), "created_at": None}

@router.get("/count/{open_heavens_id}")
def count_likes(open_heavens_id: int):
    return {"openHeavensId": open_heavens_id, "likes": repos.count_likes(open_heavens_id)}
