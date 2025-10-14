from fastapi import APIRouter, HTTPException
from app.models import CommentIn, CommentOut
from app import repos

router = APIRouter()

@router.post("/", response_model=CommentOut)
def create_comment(c: CommentIn):
    new_id = repos.create_comment(c)
    return {"id": new_id, **c.dict(), "created_at": None}

@router.get("/open_heavens/{open_heavens_id}", response_model=list[CommentOut])
def list_comments(open_heavens_id: int):
    return repos.list_comments(open_heavens_id)
