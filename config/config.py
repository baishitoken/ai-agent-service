import os
from pydantic import BaseSettings

class Config(BaseSettings):
    """Configuration settings for the application."""
    
    # MongoDB configuration
    MONGODB_URI: str = "mongodb://localhost:27017/"  # Change this to your MongoDB URI
    DATABASE_NAME: str = "game_database"  # Change this to your database name

    # Secret keys and environment settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default_secret_key")  # Secret key for app (use environment variable for production)
    DEBUG: bool = True  # Set to False in production
    
    # Game configurations (can be extended for other games)
    BLACKJACK_BETTING_LIMIT: int = 1000  # Max betting amount for blackjack games
    CHESS_RATING_LIMIT: int = 2400  # Rating limit for chess players
    EIGHTBALL_FOUL_LIMIT: int = 5  # Max fouls before game ends for 8-ball
    
    # API keys or other integrations (can be added as needed)
    # For example, you can store external API keys here
    API_KEY: Optional[str] = None  # Placeholder for API key if needed

    # Log settings
    LOG_LEVEL: str = "INFO"  # Logging level for the app (e.g., DEBUG, INFO, WARNING, ERROR)
    
    # Customizable timeouts or other environment-specific settings
    TIMEOUT: int = 30  # Timeout for database connections, API calls, etc.
    
    class Config:
        env_file = ".env"  # Read values from a .env file for environment-specific overrides

# Example of how to access configuration variables
# In other files, you can access the config like:
# config = Config()
# print(config.MONGODB_URI)
