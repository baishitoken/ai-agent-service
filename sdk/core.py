from utils.data_processing import get_processor
from utils.db_utils import store_processed_data
from models import GamePayload
from pydantic import ValidationError
from utils.logger import logger

def process_game_data(game_type, game_data):
    """Process and store game data."""
    try:
        logger.info(f"Processing game data for {game_type}")
        processor = get_processor(game_type)
        
        if not processor:
            raise ValueError(f"No processor available for game type '{game_type}'")
        
        processed_data = processor(game_data)
        store_processed_data(processed_data, game_type)
        
        logger.info(f"Game data for {game_type} processed and stored successfully.")
        return {"status": "success", "message": f"Data for {game_type} processed."}
    
    except ValidationError as e:
        logger.warning(f"Validation failed for game data: {e.errors()}")
        return {"error": "Invalid data", "details": e.errors()}
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return {"error": str(e)}
