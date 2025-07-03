import uvicorn
import os
from app.config import settings

# Create temp directory if it doesn't exist
os.makedirs(settings.TEMP_DIR, exist_ok=True)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )