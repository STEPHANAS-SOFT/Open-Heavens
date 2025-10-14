from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class HymnIn(BaseModel):
    hymn_title: Optional[str] = ""
    hymn_verse: Optional[str] = ""

class HymnOut(HymnIn):
    id: int
    created_at: datetime


class HymnPatch(BaseModel):
    hymnTitle: Optional[str] = None
    hymnVerse: Optional[str] = None

class OpenHeavenIn(BaseModel):
    topic: Optional[str]
    date: Optional[date]
    bible_reading: Optional[str]
    bible_reading_text: Optional[str]
    memory_verse: Optional[str]
    message: Optional[str]
    action_type: Optional[str]
    hymn_id: int
    bible1_year: Optional[str]
    bible1_year_text: Optional[str]
    action_point: Optional[str]

class OpenHeavenOut(OpenHeavenIn):
    id: int
    created_at: datetime

class OpenHeavenTeenIn(BaseModel):
    title: Optional[str]
    date: Optional[date]
    memories: Optional[str]
    read: Optional[str]
    bible_reading: Optional[str]
    message: Optional[str]
    hymn_title: Optional[str]
    hymn: Optional[str]
    bible_in_one_year_verse: Optional[str]
    bible_in_one_year: Optional[str]
    action_text: Optional[str]
    action_types: Optional[str]
    hymnal: Optional[str]

class OpenHeavenTeenOut(OpenHeavenTeenIn):
    id: int
    created_at: datetime


class OpenHeavenPatch(BaseModel):
    topic: Optional[str] = None
    date: Optional[date] = None
    bibleReading: Optional[str] = None
    bibleReadingText: Optional[str] = None
    memoryVerse: Optional[str] = None
    message: Optional[str] = None
    actionType: Optional[str] = None
    hymn: Optional[int] = None
    bible1Year: Optional[str] = None
    bible1YearText: Optional[str] = None
    actionPoint: Optional[str] = None


class PaginatedResult(BaseModel):
    items: list
    total: int
    limit: int
    offset: int

class CommentIn(BaseModel):
    open_heavens_id: int
    comment: Optional[str]
    name: Optional[str]

class CommentOut(CommentIn):
    id: int
    created_at: datetime

class LikeIn(BaseModel):
    open_heavens_id: int
    like: Optional[int] = 1
    liked: bool = True

class LikeOut(LikeIn):
    id: int
    created_at: datetime

class PrayerRequestIn(BaseModel):
    name: Optional[str]
    user_ref: Optional[str]
    request_content: Optional[str]
    disabled: Optional[bool] = False

class PrayerRequestOut(PrayerRequestIn):
    id: int
    created_at: datetime

class PrayIn(BaseModel):
    prayer_content: Optional[str]
    prayer_request_id: Optional[int]
    name: Optional[str]

class PrayOut(PrayIn):
    id: int
    created_at: datetime
