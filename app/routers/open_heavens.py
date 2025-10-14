from fastapi import APIRouter, HTTPException, Query
from app.models import OpenHeavenIn, OpenHeavenOut, OpenHeavenPatch, PaginatedResult
from app import repos

router = APIRouter()

@router.post("/", response_model=OpenHeavenOut)
def create_open_heaven(o: OpenHeavenIn):
    new_id = repos.create_open_heaven(o)
    return {"id": new_id, **o.dict(), "created_at": None}

@router.get("/", response_model=PaginatedResult)
def list_open_heavens(limit: int = Query(20, ge=1, le=200), offset: int = Query(0, ge=0)):
    return repos.list_open_heavens_paginated(limit=limit, offset=offset)

@router.get("/{open_heaven_id}", response_model=OpenHeavenOut)
def get_open_heaven_by_id(open_heaven_id: int):
    open_heaven = repos.get_open_heaven_by_id(open_heaven_id)
    if not open_heaven:
        raise HTTPException(status_code=404, detail="Open Heavens entry not found")
    return open_heaven

@router.delete("/{open_heaven_id}")
def delete_open_heaven(open_heaven_id: int):
    ok = repos.delete_open_heaven(open_heaven_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Open Heavens entry not found")
    return {"deleted": open_heaven_id}


@router.put("/{open_heaven_id}")
def replace_open_heaven(open_heaven_id: int, o: OpenHeavenIn):
    data = {k: v for k, v in o.dict().items()}
    row = repos.update_open_heaven(open_heaven_id, data)
    if not row:
        raise HTTPException(status_code=404, detail="Open Heavens entry not found")
    return row


@router.patch("/{open_heaven_id}")
def patch_open_heaven(open_heaven_id: int, o: OpenHeavenPatch):
    patch = {k: v for k, v in o.dict().items() if v is not None}
    row = repos.update_open_heaven(open_heaven_id, patch)
    if not row:
        raise HTTPException(status_code=404, detail="Open Heavens entry not found")
    return row
