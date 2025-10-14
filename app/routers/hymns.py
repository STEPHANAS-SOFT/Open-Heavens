from fastapi import APIRouter, Depends, HTTPException, Query
from app.models import HymnIn, HymnOut, HymnPatch, PaginatedResult
from app import repos

router = APIRouter()

@router.post("/", response_model=HymnOut)
def create_hymn(h: HymnIn):
    new_id = repos.create_hymn(h)
    return {"id": new_id, **h.dict(), "created_at": None}

@router.get("/", response_model=PaginatedResult)
def get_hymns(limit: int = Query(20, ge=1, le=200), offset: int = Query(0, ge=0)):
    return repos.list_hymns_paginated(limit=limit, offset=offset)

@router.get("/{hymn_id}", response_model=HymnOut)
def get_hymn_by_id(hymn_id: int):
    hymn = repos.get_hymn_by_id(hymn_id)
    if not hymn:
        raise HTTPException(status_code=404, detail="Hymn not found")
    return hymn

@router.delete("/{hymn_id}")
def delete_hymn(hymn_id: int):
    ok = repos.delete_hymn(hymn_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Hymn not found")
    return {"deleted": hymn_id}



@router.put("/{hymn_id}")
def replace_hymn(hymn_id: int, h: HymnIn):
    # full replace
    data = {k: v for k, v in h.dict().items()}
    row = repos.update_hymn(hymn_id, data)
    if not row:
        raise HTTPException(status_code=404, detail="Hymn not found")
    return row


@router.patch("/{hymn_id}")
def patch_hymn(hymn_id: int, h: HymnPatch):
    patch = {k: v for k, v in h.dict().items() if v is not None}
    row = repos.update_hymn(hymn_id, patch)
    if not row:
        raise HTTPException(status_code=404, detail="Hymn not found")
    return row
