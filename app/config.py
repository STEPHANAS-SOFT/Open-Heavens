from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    database_url: str
    api_key: str
    api_keys: Optional[str] = None  # comma-separated additional keys
    uvicorn_host: str = "127.0.0.1"
    uvicorn_port: int = 8000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    s = Settings()
    # normalize API keys into a list if provided
    if s.api_keys:
        s.api_keys = [k.strip() for k in s.api_keys.split(",") if k.strip()]
    else:
        s.api_keys = []
    return s
