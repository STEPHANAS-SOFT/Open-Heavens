from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.executors.pool import ThreadPoolExecutor
from datetime import datetime, timedelta
import pytz
import logging
from typing import Dict, Any

from config import settings, TIMEZONE_GROUPS
from firebase_manager import FirebaseManager
from database_manager import DatabaseManager

logger = logging.getLogger(__name__)

class NotificationScheduler:
    def __init__(self):
        self.scheduler = self._create_scheduler()
        self.firebase = FirebaseManager()
        self.db = DatabaseManager()
        
    def _create_scheduler(self) -> BackgroundScheduler:
        """Create and configure the scheduler"""
        executors = {
            'default': ThreadPoolExecutor(20)
        }
        
        scheduler = BackgroundScheduler(
            executors=executors,
            timezone=pytz.UTC
        )
        
        return scheduler
        
    def schedule_notifications(self):
        """Schedule notifications for all timezone groups"""
        for region, timezones in TIMEZONE_GROUPS.items():
            for tz in timezones:
                # Schedule for midnight in each timezone
                trigger = CronTrigger(
                    hour=0,
                    minute=0,
                    timezone=pytz.timezone(tz)
                )
                
                self.scheduler.add_job(
                    func=self.send_notifications,
                    trigger=trigger,
                    args=[tz],
                    name=f"devotional_notification_{tz}",
                    replace_existing=True
                )
                logger.info(f"Scheduled notifications for timezone: {tz}")
                
        # Add health check job
        self.scheduler.add_job(
            func=self.health_check,
            trigger='interval',
            seconds=settings.health_check_interval,
            name='health_check',
            replace_existing=True
        )
        
    def format_devotional_message(self, devotional: Dict[str, Any], hymn: Dict[str, Any] = None) -> Dict[str, str]:
        """Format devotional content for notification"""
        title = f"Open Heavens - {devotional['topic']}"
        
        body = (
            f"📖 Bible Reading: {devotional['bible_reading']}\n"
            f"💭 Memory Verse: {devotional['memory_verse']}\n\n"
            f"🙏 Action Point: {devotional['action_point']}"
        )
        
        data = {
            'devotional_id': str(devotional['id']),
            'date': str(devotional['date']),
            'type': 'devotional',
            'bible_reading_text': devotional['bible_reading_text'],
            'message': devotional['message']
        }
        
        if hymn:
            data['hymn_title'] = hymn['hymn_title']
            data['hymn_verse'] = hymn['hymn_verse']
            
        return {
            'title': title,
            'body': body,
            'data': data
        }
        
    def send_notifications(self, timezone: str):
        """Send notifications for a specific timezone"""
        try:
            # Get current date in the target timezone
            tz = pytz.timezone(timezone)
            target_date = datetime.now(tz).date()
            
            # Get devotional content
            devotional = self.db.get_devotional(target_date)
            if not devotional:
                logger.error(f"No devotional found for date: {target_date}")
                return
                
            # Get hymn if available
            hymn = None
            if devotional.get('hymn_id'):
                hymn = self.db.get_hymn(devotional['hymn_id'])
                
            # Format message
            message = self.format_devotional_message(devotional, hymn)
            
            # Get FCM tokens
            tokens = self.firebase.get_fcm_tokens()
            if not tokens:
                logger.warning("No FCM tokens found for notification")
                return
                
            # Send notifications
            self.firebase.send_bulk_notifications(
                tokens=tokens,
                title=message['title'],
                body=message['body'],
                data=message['data']
            )
            
            logger.info(f"Notifications sent successfully for timezone {timezone}")
            
        except Exception as e:
            logger.error(f"Failed to send notifications for timezone {timezone}: {e}")
            
    def health_check(self):
        """Perform health check on all components"""
        try:
            # Check database connection
            db_healthy = self.db.health_check()
            
            # Check Firebase connection by trying to fetch tokens
            firebase_healthy = bool(self.firebase.get_fcm_tokens() is not None)
            
            # Log health status
            logger.info(f"Health check - Database: {'OK' if db_healthy else 'FAIL'}, "
                       f"Firebase: {'OK' if firebase_healthy else 'FAIL'}")
            
            return db_healthy and firebase_healthy
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
            
    def start(self):
        """Start the notification scheduler"""
        try:
            self.db.connect()
            self.schedule_notifications()
            self.scheduler.start()
            logger.info("Notification scheduler started successfully")
        except Exception as e:
            logger.error(f"Failed to start notification scheduler: {e}")
            raise
            
    def stop(self):
        """Stop the notification scheduler"""
        try:
            self.scheduler.shutdown()
            self.db.close()
            logger.info("Notification scheduler stopped successfully")
        except Exception as e:
            logger.error(f"Error stopping notification scheduler: {e}")