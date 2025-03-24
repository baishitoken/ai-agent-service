from sdk.game_processors import get_processor
from sdk.utils import handle_exception, log_request, log_response
from sdk.exceptions import SDKError
from utils.db_utils import store_processed_data
from models import GamePayload
from pydantic import ValidationError
from utils.logger import logger

def process_game_data(game_type: str, game_data: dict):
    """Process and store game data."""
    try:
        # Log the incoming request
        log_request(game_data)
        
        # Check if the game type is valid
        if not check_game_type_validity(game_type):
            return handle_exception("Invalid game type", "game type validation")
        
        # Validate game data
        if not validate_json(game_data, GamePayload):
            return {"error": "Invalid data format."}

        # Process the data using the appropriate processor
        processor = get_processor(game_type)
        if processor is None:
            raise SDKError(f"No processor available for game type '{game_type}'")
        
        processed_data = processor(game_data)

        # Store processed data in the database
        store_processed_data(processed_data, game_type)
        
        # Log and return response
        response = {"message": f"Game data for {game_type} processed successfully."}
        log_response(response)
        return response

    except SDKError as e:
        return handle_exception(e, "SDKError during game data processing")
    except ValidationError as e:
        return handle_exception(e, "ValidationError during game data processing")
    except Exception as e:
        return handle_exception(e, "Unknown error during game data processing")

def check_game_type_validity(game_type: str) -> bool:
    """Check if the provided game type is valid."""
    valid_game_types = ["blackjack", "chess", "eight_ball"]
    if game_type.lower() not in valid_game_types:
        logger.error(f"Invalid game type: {game_type}")
        return False
    return True
