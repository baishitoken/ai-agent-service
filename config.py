import os

class Config:
    """Centralized configuration for the application."""
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    DATABASE_NAME = "game_data_db"
    FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))
