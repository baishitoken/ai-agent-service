from pydantic import BaseModel, Field, root_validator, validator
from typing import Optional
import os

class ConfigSchema(BaseModel):
    """Configuration schema that validates settings and their values."""
    
    # MongoDB Configuration
    MONGODB_URI: str = Field(..., description="MongoDB URI to connect to the database")
    DATABASE_NAME: str = Field(..., description="The name of the database to use")

    # Security
    SECRET_KEY: str = Field(..., description="Secret key used for encryption, authentication, etc.")
    
    # Debugging
    DEBUG: bool = Field(True, description="Enable debugging mode. Set to False in production.")

    # Game-specific Configurations
    BLACKJACK_BETTING_LIMIT: int = Field(1000, ge=1, description="Maximum betting limit for blackjack games")
    CHESS_RATING_LIMIT: int = Field(2400, ge=1, description="Maximum rating for chess players to participate")
    EIGHTBALL_FOUL_LIMIT: int = Field(5, ge=1, description="Maximum fouls allowed in 8-ball game before it ends")
    
    # Logging configuration
    LOG_LEVEL: str = Field("INFO", description="Log level (e.g., DEBUG, INFO, WARNING, ERROR)")
    
    # Timeout
    TIMEOUT: int = Field(30, ge=1, description="Timeout setting for database or external service calls")

    # API Key (Optional)
    API_KEY: Optional[str] = None  # Placeholder for external API key if needed

    # Environment validation (ensure the environment variables are set)
    @root_validator(pre=True)
    def check_required_env_variables(cls, values):
        """Ensure environment variables are set correctly."""
        if 'SECRET_KEY' not in values or not values['SECRET_KEY']:
            raise ValueError('SECRET_KEY must be defined')
        if 'MONGODB_URI' not in values or not values['MONGODB_URI']:
            raise ValueError('MONGODB_URI must be defined')
        return values

    # Validate the value of `LOG_LEVEL`
    @validator('LOG_LEVEL')
    def validate_log_level(cls, v):
        valid_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_log_levels:
            raise ValueError(f"Invalid LOG_LEVEL: {v}. Choose from {', '.join(valid_log_levels)}.")
        return v.upper()

    class Config:
        env_file = ".env"  # Use `.env` file for environment variable overrides

# Example of how to use ConfigSchema

def validate_and_load_config():
    """Validate and load the config schema."""
    try:
        config = ConfigSchema()
        print(config.dict())  # Print or use the validated configuration values
    except Exception as e:
        print(f"Error in loading configuration: {e}")
        raise

if __name__ == "__main__":
    validate_and_load_config()
