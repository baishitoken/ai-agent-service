import os

class Config:
    """Centralized configuration for the application."""

    # MongoDB configuration
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "game_data_db")

    # Flask configuration
    FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))
    FLASK_DEBUG = bool(int(os.getenv("FLASK_DEBUG", 1)))

    # Logging configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
    LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")

    # Performance and feature toggles
    ENABLE_STRUCTURED_LOGS = bool(int(os.getenv("ENABLE_STRUCTURED_LOGS", 1)))
    ENABLE_METRICS_LOGGING = bool(int(os.getenv("ENABLE_METRICS_LOGGING", 1)))

    # Additional environment-based configurations
    ENV = os.getenv("ENV", "development")
    IS_PRODUCTION = ENV == "production"
