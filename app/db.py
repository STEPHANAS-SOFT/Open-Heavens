from typing import Optional
import logging
from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from app.config import get_settings

_settings = get_settings()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@contextmanager
def get_connection():
    try:
        conn = connect(_settings.database_url)
        conn.cursor_factory = RealDictCursor
        logger.debug("Database connection established successfully")
        try:
            yield conn
        finally:
            conn.close()
            logger.debug("Database connection closed")
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        raise
