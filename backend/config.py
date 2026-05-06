import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))


class Config:
    """Application configuration loaded from environment variables."""

    # Flask
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-dev-key")
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB

    # MongoDB
    MONGO_URI = os.getenv("MONGO_URI", "")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "syllabussnap")

    # CORS
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:5174").split(",")

    # Uploads
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')