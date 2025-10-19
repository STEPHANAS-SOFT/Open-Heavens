from pydantic_settings import BaseSettings
from typing import Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    # PostgreSQL settings
    database_url: str
    
    # Firebase settings
    firebase_credentials_path: str
    firebase_database_url: Optional[str] = None
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "notifications.log"
    
    # Health check interval (in seconds)
    health_check_interval: int = 300  # 5 minutes
    
    class Config:
        env_file = ".env"

# Timezone groups
TIMEZONE_GROUPS = {
    "Africa": [
        "Africa/Lagos",
        "Africa/Cairo",
        "Africa/Nairobi",
        "Africa/Johannesburg"
    ],
    "Americas": [
        "America/Los_Angeles",
        "America/New_York"
    ],
    "Europe": [
        "Europe/London",
        "Europe/Paris"
    ],
    "Asia": [
        "Asia/Dubai",
        "Asia/Kolkata",
        "Asia/Singapore",
        "Asia/Tokyo"
    ],
    "Australia": [
        "Australia/Sydney"
    ]
}

settings = Settings()