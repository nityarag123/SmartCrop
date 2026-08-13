"""SmartCrop configuration.

All secrets are read from environment variables. Never commit real values.
Copy .env.example to .env and fill in your own keys.
"""
import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "smartcrop-dev-change-me")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = os.getenv("FLASK_ENV", "development") == "development"

    # MongoDB Atlas (primary database)
    MONGODB_URI = os.getenv("MONGODB_URI", "")
    MONGODB_DB_NAME = os.getenv("DATABASE_NAME", os.getenv("MONGODB_DB_NAME", "smartcrop"))

    # Optional Atlas connection split into parts (used if MONGODB_URI is empty)
    MONGODB_ATLAS_USERNAME = os.getenv("MONGODB_ATLAS_USERNAME", "")
    MONGODB_ATLAS_PASSWORD = os.getenv("MONGODB_ATLAS_PASSWORD", "")
    MONGODB_ATLAS_CLUSTER = os.getenv("MONGODB_ATLAS_CLUSTER", "")

    # When MongoDB is unreachable the app transparently falls back to a local
    # JSON store so every feature keeps working for demos and development.
    USE_LOCAL_FALLBACK = os.getenv("USE_LOCAL_FALLBACK", "true").lower() == "true"
    LOCAL_STORE_PATH = os.getenv("LOCAL_STORE_PATH", os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "instance", "smartcrop_store.json"
    ))

    # External APIs (optional). Without keys, endpoints return clearly
    # labelled demo data and never pretend it is live.
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
    LLM_API_KEY = os.getenv("LLM_API_KEY", os.getenv("OPENAI_API_KEY", ""))
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
    MARKET_API_KEY = os.getenv("MARKET_API_KEY", "")

    # Upload limits
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB
    ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "bmp"}
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "instance", "uploads"
    ))
