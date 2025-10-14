from typing import List, Optional, Dict, Any
from psycopg2.extras import RealDictCursor
from app.db import get_connection
from app.models import (
    HymnIn, OpenHeavenIn, OpenHeavenTeenIn, CommentIn,
    LikeIn, PrayerRequestIn, PrayIn
)

def _row_to_dict(row) -> Optional[Dict[str, Any]]:
    if row is None:
        return None
    try:
        return dict(row)
    except Exception:
        return row

# Hymns
def create_hymn(h: HymnIn) -> int:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'INSERT INTO hymns (hymn_title, hymn_verse) VALUES (%s,%s) RETURNING id',
                (h.hymn_title, h.hymn_verse),
            )
            row = cur.fetchone()
            conn.commit()
            return row["id"] if isinstance(row, dict) else row[0]

def get_hymn_by_id(hymn_id: int) -> Optional[dict]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM hymns WHERE id = %s', (hymn_id,))
            row = cur.fetchone()
            return _row_to_dict(row)

def list_hymns_paginated(limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT count(*) FROM hymns')
            result = cur.fetchone()
            total = result['count'] if isinstance(result, dict) else result[0]
            cur.execute('SELECT * FROM hymns ORDER BY created_at DESC LIMIT %s OFFSET %s', (limit, offset))
            items = cur.fetchall()
            return {"items": items, "total": total, "limit": limit, "offset": offset}

def update_hymn(hymn_id: int, data: dict) -> Optional[dict]:
    if not data:
        return None
    allowed = {"hymn_title", "hymn_verse"}
    set_parts = []
    values = []
    for k, v in data.items():
        if k not in allowed:
            continue
        set_parts.append(f'{k} = %s')
        values.append(v)
    if not set_parts:
        return None
    values.append(hymn_id)
    sql = f'UPDATE hymns SET {",".join(set_parts)} WHERE id=%s RETURNING *'
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, tuple(values))
            row = cur.fetchone()
            conn.commit()
            return _row_to_dict(row)

def delete_hymn(hymn_id: int) -> bool:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM hymns WHERE id=%s RETURNING id', (hymn_id,))
            row = cur.fetchone()
            conn.commit()
            return bool(row)

# Open Heavens
def create_open_heaven(o: OpenHeavenIn) -> int:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'INSERT INTO open_heavens (topic, date, bible_reading, bible_reading_text, memory_verse, message, action_type, hymn_id, bible1_year, bible1_year_text, action_point) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id',
                (o.topic, o.date, o.bible_reading, o.bible_reading_text, o.memory_verse, o.message, o.action_type, o.hymn_id, o.bible1_year, o.bible1_year_text, o.action_point)
            )
            row = cur.fetchone()
            conn.commit()
            return row["id"] if isinstance(row, dict) else row[0]

def get_open_heaven_by_id(open_heaven_id: int) -> Optional[Dict[str, Any]]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM open_heavens WHERE id = %s', (open_heaven_id,))
            row = cur.fetchone()
            return _row_to_dict(row)

# Open Heavens Teenagers
def create_open_heaven_teen(o: OpenHeavenTeenIn) -> int:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'INSERT INTO open_heavens_teenagers (title, date, memories, read, bible_reading, message, hymn_title, hymn, bible_in_one_year_verse, bible_in_one_year, action_text, action_types, hymnal) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id',
                (o.title, o.date, o.memories, o.read, o.bible_reading, o.message, o.hymn_title, o.hymn, o.bible_in_one_year_verse, o.bible_in_one_year, o.action_text, o.action_types, o.hymnal))
            row = cur.fetchone()
            conn.commit()
            return row["id"] if isinstance(row, dict) else row[0]

def list_open_heavens_teen_paginated(limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT count(*) FROM open_heavens_teenagers')
            result = cur.fetchone()
            total = result['count'] if isinstance(result, dict) else result[0]
            cur.execute('SELECT * FROM open_heavens_teenagers ORDER BY date DESC NULLS LAST LIMIT %s OFFSET %s', (limit, offset))
            items = cur.fetchall()
            return {"items": items, "total": total, "limit": limit, "offset": offset}

def update_open_heaven_teen(teen_id: int, data: dict) -> Optional[dict]:
    if not data:
        return None
    allowed = {
        "title", "date", "memories", "read", "bible_reading", "message",
        "hymn_title", "hymn", "bible_in_one_year_verse", "bible_in_one_year",
        "action_text", "action_types", "hymnal"
    }
    set_parts = []
    values = []
    for k, v in data.items():
        if k not in allowed:
            continue
        set_parts.append(f'{k} = %s')
        values.append(v)
    if not set_parts:
        return None
    values.append(teen_id)
    sql = f'UPDATE open_heavens_teenagers SET {",".join(set_parts)} WHERE id=%s RETURNING *'
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, tuple(values))
            row = cur.fetchone()
            conn.commit()
            return _row_to_dict(row)

def delete_open_heaven_teen(teen_id: int) -> bool:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM open_heavens_teenagers WHERE id=%s RETURNING id', (teen_id,))
            row = cur.fetchone()
            conn.commit()
            return bool(row)

def list_open_heavens_paginated(limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT count(*) FROM open_heavens')
            result = cur.fetchone()
            total = result['count'] if isinstance(result, dict) else result[0]
            cur.execute('SELECT * FROM open_heavens ORDER BY date DESC NULLS LAST LIMIT %s OFFSET %s', (limit, offset))
            items = cur.fetchall()
            return {"items": items, "total": total, "limit": limit, "offset": offset}

def update_open_heaven(open_heaven_id: int, data: dict) -> Optional[dict]:
    if not data:
        return None
    allowed = {
        "topic", "date", "bible_reading", "bible_reading_text", "memory_verse",
        "message", "action_type", "hymn_id", "bible1_year", "bible1_year_text",
        "action_point"
    }
    set_parts = []
    values = []
    for k, v in data.items():
        if k not in allowed:
            continue
        set_parts.append(f'{k} = %s')
        values.append(v)
    if not set_parts:
        return None
    values.append(open_heaven_id)
    sql = f'UPDATE open_heavens SET {",".join(set_parts)} WHERE id=%s RETURNING *'
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, tuple(values))
            row = cur.fetchone()
            conn.commit()
            return _row_to_dict(row)

def delete_open_heaven(open_heaven_id: int) -> bool:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM open_heavens WHERE id=%s RETURNING id', (open_heaven_id,))
            row = cur.fetchone()
            conn.commit()
            return bool(row)

# Comments
def create_comment(c: CommentIn) -> int:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO comments (open_heavens_id, comment, name) VALUES (%s,%s,%s) RETURNING id',
                        (c.open_heavens_id, c.comment, c.name))
            row = cur.fetchone()
            conn.commit()
            return row["id"] if isinstance(row, dict) else row[0]

def list_comments(open_heavens_id: int) -> List[dict]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM comments WHERE open_heavens_id=%s ORDER BY created_at DESC', (open_heavens_id,))
            return cur.fetchall()

# Likes
def create_like(l: LikeIn) -> int:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO likes (open_heavens_id, "like", liked) VALUES (%s,%s,%s) RETURNING id',
                        (l.open_heavens_id, l.like, l.liked))
            row = cur.fetchone()
            conn.commit()
            return row["id"] if isinstance(row, dict) else row[0]

def count_likes(open_heavens_id: int) -> int:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT count(*) FROM likes WHERE open_heavens_id=%s AND liked = true', (open_heavens_id,))
            result = cur.fetchone()
            return result['count'] if isinstance(result, dict) else result[0]

# Prayers
def create_prayer_request(p: PrayerRequestIn) -> int:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO prayer_requests (name, user_ref, request_content, disabled) VALUES (%s,%s,%s,%s) RETURNING id',
                        (p.name, p.user_ref, p.request_content, p.disabled))
            row = cur.fetchone()
            conn.commit()
            return row["id"] if isinstance(row, dict) else row[0]

def list_prayer_requests() -> List[dict]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM prayer_requests ORDER BY created_at DESC')
            return cur.fetchall()

def create_pray(p: PrayIn) -> int:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'INSERT INTO pray (prayer_content, prayer_request_id, name) VALUES (%s,%s,%s) RETURNING id',
                (p.prayer_content, p.prayer_request_id, p.name)
            )
            row = cur.fetchone()
            conn.commit()
            return row["id"] if isinstance(row, dict) else row[0]