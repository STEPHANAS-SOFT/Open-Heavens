from typing import Optional, Dict, Any
import psycopg2
from psycopg2.extras import RealDictCursor
import logging
from datetime import date
from config import settings

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.conn = None
        
    def connect(self):
        """Establish database connection"""
        try:
            self.conn = psycopg2.connect(
                settings.database_url,
                cursor_factory=RealDictCursor
            )
            logger.info("Database connection established successfully")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise
            
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None
            
    def get_devotional(self, target_date: date) -> Optional[Dict[str, Any]]:
        """Fetch devotional content for a specific date"""
        try:
            if not self.conn:
                self.connect()
                
            with self.conn.cursor() as cur:
                cur.execute("""
                    SELECT 
                        id,
                        topic,
                        date,
                        bible_reading,
                        bible_reading_text,
                        memory_verse,
                        message,
                        action_point,
                        hymn_id
                    FROM open_heavens 
                    WHERE date = %s
                """, (target_date,))
                
                result = cur.fetchone()
                if result:
                    # Convert to dict if using RealDictCursor
                    return dict(result) if hasattr(result, 'items') else result
                return None
                
        except Exception as e:
            logger.error(f"Failed to fetch devotional for date {target_date}: {e}")
            return None
            
    def get_hymn(self, hymn_id: int) -> Optional[Dict[str, Any]]:
        """Fetch hymn details by ID"""
        try:
            if not self.conn:
                self.connect()
                
            with self.conn.cursor() as cur:
                cur.execute("""
                    SELECT 
                        id,
                        hymn_title,
                        hymn_verse
                    FROM hymns 
                    WHERE id = %s
                """, (hymn_id,))
                
                result = cur.fetchone()
                if result:
                    return dict(result) if hasattr(result, 'items') else result
                return None
                
        except Exception as e:
            logger.error(f"Failed to fetch hymn ID {hymn_id}: {e}")
            return None
            
    def health_check(self) -> bool:
        """Perform database health check"""
        try:
            if not self.conn:
                self.connect()
                
            with self.conn.cursor() as cur:
                cur.execute('SELECT 1')
                return bool(cur.fetchone())
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False