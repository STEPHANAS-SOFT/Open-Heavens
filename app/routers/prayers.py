from fastapi import APIRouter
from app.models import PrayerRequestIn, PrayerRequestOut, PrayIn, PrayOut
from app import repos

router = APIRouter()

@router.post("/requests", response_model=PrayerRequestOut)
def create_prayer_request(p: PrayerRequestIn):
    new_id = repos.create_prayer_request(p)
    return {"id": new_id, **p.dict(), "created_at": None}

@router.get("/requests", response_model=list[PrayerRequestOut])
def list_prayer_requests():
    return repos.list_prayer_requests()

@router.post("/pray", response_model=PrayOut)
def create_pray(p: PrayIn):
    new_id = repos.create_pray(p)
    return {"id": new_id, **p.dict(), "created_at": None}
