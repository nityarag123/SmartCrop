# config_dynamic.py - Enhanced configuration for dynamic data system
import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    DATABASE_URL = os.getenv('DATABASE_URL')  # e.g. postgresql://user:pass@host:5432/dbname
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://user:pass@localhost/dbname')  # For SQLAlchemy
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', '')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    MONGODB_ATLAS_USERNAME = os.getenv('MONGODB_ATLAS_USERNAME')
    MONGODB_ATLAS_PASSWORD = os.getenv('MONGODB_ATLAS_PASSWORD')
    MONGODB_ATLAS_CLUSTER = os.getenv('MONGODB_ATLAS_CLUSTER')
    MONGODB_DB_NAME = os.getenv('MONGODB_DB_NAME', 'smartcrop')
    MONGODB_URI = os.getenv('MONGODB_URI')

    # Dynamic Data System API Keys
    AGMARKNET_API_KEY = os.getenv('AGMARKNET_API_KEY', '579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')  # Optional for advanced caching

    # Cache settings (in seconds)
    CACHE_TIMEOUT_MARKET_PRICES = int(os.getenv('CACHE_TIMEOUT_MARKET_PRICES', '300'))  # 5 minutes
    CACHE_TIMEOUT_WEATHER = int(os.getenv('CACHE_TIMEOUT_WEATHER', '600'))  # 10 minutes
    CACHE_TIMEOUT_CROP_CALENDAR = int(os.getenv('CACHE_TIMEOUT_CROP_CALENDAR', '3600'))  # 1 hour

    # Background task intervals (in seconds)
    MARKET_PRICES_UPDATE_INTERVAL = int(os.getenv('MARKET_PRICES_UPDATE_INTERVAL', '1800'))  # 30 minutes
    WEATHER_UPDATE_INTERVAL = int(os.getenv('WEATHER_UPDATE_INTERVAL', '3600'))  # 60 minutes
    DATA_QUALITY_CHECK_INTERVAL = int(os.getenv('DATA_QUALITY_CHECK_INTERVAL', '14400'))  # 4 hours

    # Enable/disable features
    ENABLE_DYNAMIC_MARKET_PRICES = os.getenv('ENABLE_DYNAMIC_MARKET_PRICES', 'true').lower() == 'true'
    ENABLE_SMART_CROP_CALENDAR = os.getenv('ENABLE_SMART_CROP_CALENDAR', 'true').lower() == 'true'
    ENABLE_BACKGROUND_TASKS = os.getenv('ENABLE_BACKGROUND_TASKS', 'true').lower() == 'true'
