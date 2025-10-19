import logging
import sys
from config import settings
from scheduler import NotificationScheduler

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(settings.log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def main():
    try:
        scheduler = NotificationScheduler()
        scheduler.start()
        
        # Keep the script running
        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            scheduler.stop()
            
    except Exception as e:
        logger.error(f"Application failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()