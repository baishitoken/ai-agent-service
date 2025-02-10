import logging
import json
from typing import Any

# Initialize the logger for the SDK
logger = logging.getLogger("SDK")
logger.setLevel(logging.DEBUG)

def log_request(request_data: dict):
    """Helper function to log the request details."""
    logger.debug("Received request with data: %s", json.dumps(request_data, indent=2))

def log_response(response_data: dict):
    """Helper function to log the response details."""
    logger.debug("Sending response with data: %s", json.dumps(response_data, indent=2))

def validate_json(request_data: dict, schema_class: Any) -> bool:
    """Helper function to validate JSON data against a Pydantic model/schema."""
    try:
        schema_class(**request_data)  # Validate using the schema class
        logger.debug("Request data validated successfully.")
        return True
    except Exception as e:
        logger.error("Validation failed: %s", str(e))
        return False

def parse_json(json_data: str) -> dict:
    """Helper function to safely parse JSON strings into Python dictionaries."""
    try:
        return json.loads(json_data)
    except json.JSONDecodeError as e:
        logger.error("JSON parsing error: %s", e)
        return {}

def sanitize_input(data: dict) -> dict:
    """Sanitize incoming data to avoid issues with malformed or unwanted fields."""
    # Example: Removing any potentially dangerous fields or sensitive data.
    sanitized_data = {k: v for k, v in data.items() if k not in ["password", "secret"]}
    logger.debug("Sanitized input data: %s", sanitized_data)
    return sanitized_data

def handle_exception(e: Exception, context: str):
    """Centralized exception handler for logging and debugging."""
    logger.error("Exception occurred during %s: %s", context, str(e))
    return {"error": str(e)}

def format_response(data: dict, status_code: int) -> dict:
    """Format the response data for consistency."""
    return {"status_code": status_code, "data": data}

def check_game_type_validity(game_type: str) -> bool:
    """Helper function to check if the provided game type is valid."""
    valid_game_types = ["blackjack", "chess", "eight_ball"]
    if game_type.lower() not in valid_game_types:
        logger.error("Invalid game type: %s. Valid types are %s", game_type, ", ".join(valid_game_types))
        return False
    return True
