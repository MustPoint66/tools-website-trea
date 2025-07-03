from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional
import os

class Settings(BaseSettings):
    # Required settings
    OPENAI_API_KEY: Optional[str] = None
    DEFAULT_MODEL: str = "gpt-4-vision-preview"
    
    # Application settings
    DEBUG: bool = True
    SECRET_KEY: str = "your-secret-key-change-in-production"
    
    # Redis and Celery settings
    REDIS_URL: str = "redis://redis:6379/0"
    CELERY_BROKER_URL: str = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/0"
    
    # File handling
    TEMP_DIR: str = "./temp"
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE: int = 50000000
    
    # API URLs
    BACKEND_URL: str = "http://localhost:8000"
    NEXT_PUBLIC_BACKEND_URL: str = "http://localhost:8000"
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  # This allows extra fields in .env to be ignored
    )

settings = Settings()
