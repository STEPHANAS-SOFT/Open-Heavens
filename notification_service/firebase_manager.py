import firebase_admin
from firebase_admin import credentials, messaging, db
from typing import List, Dict, Any
import logging
from config import settings

logger = logging.getLogger(__name__)

class FirebaseManager:
    def __init__(self):
        self.initialize_firebase()
        
    def initialize_firebase(self):
        """Initialize Firebase Admin SDK"""
        try:
            cred = credentials.Certificate(settings.firebase_credentials_path)
            firebase_admin.initialize_app(cred, {
                'databaseURL': settings.firebase_database_url
            })
            logger.info("Firebase Admin SDK initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Firebase Admin SDK: {e}")
            raise
    
    def get_fcm_tokens(self) -> List[str]:
        """Fetch FCM tokens from Firebase Realtime Database"""
        try:
            tokens_ref = db.reference('fcm_tokens')
            tokens_data = tokens_ref.get()
            if not tokens_data:
                return []
            return [token for token in tokens_data.values() if token]
        except Exception as e:
            logger.error(f"Failed to fetch FCM tokens: {e}")
            return []
    
    def send_notification(self, token: str, title: str, body: str, data: Dict[str, Any] = None) -> bool:
        """Send notification to a specific device token"""
        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                data=data or {},
                token=token
            )
            
            response = messaging.send(message)
            logger.info(f"Successfully sent message: {response}")
            return True
        except messaging.ApiCallError as e:
            logger.error(f"Failed to send message to token {token}: {e}")
            return False
    
    def send_bulk_notifications(self, tokens: List[str], title: str, body: str, data: Dict[str, Any] = None) -> None:
        """Send notifications to multiple devices in batches"""
        if not tokens:
            logger.warning("No tokens provided for bulk notification")
            return
        
        # Process in batches of 500 (FCM limit)
        batch_size = 500
        for i in range(0, len(tokens), batch_size):
            batch = tokens[i:i + batch_size]
            messages = [
                messaging.Message(
                    notification=messaging.Notification(
                        title=title,
                        body=body
                    ),
                    data=data or {},
                    token=token
                ) for token in batch
            ]
            
            try:
                responses = messaging.send_all(messages)
                logger.info(f"Batch notification results: success={responses.success_count}, failure={responses.failure_count}")
            except Exception as e:
                logger.error(f"Failed to send batch notifications: {e}")
                
    def cleanup_invalid_tokens(self, tokens: List[str]) -> None:
        """Remove invalid tokens from Firebase database"""
        try:
            tokens_ref = db.reference('fcm_tokens')
            current_tokens = tokens_ref.get()
            
            # Find tokens to remove
            for key, token in current_tokens.items():
                if token not in tokens:
                    tokens_ref.child(key).delete()
                    logger.info(f"Removed invalid token: {token}")
        except Exception as e:
            logger.error(f"Failed to cleanup invalid tokens: {e}")