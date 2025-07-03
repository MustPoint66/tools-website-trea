from app.tasks.celery_app import celery_app
import os
from app.config import settings

# Create temp directory if it doesn't exist
os.makedirs(settings.TEMP_DIR, exist_ok=True)

if __name__ == "__main__":
    # This will start the Celery worker
    celery_app.worker_main(["worker", "--loglevel=info"])