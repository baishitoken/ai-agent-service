from pymongo import MongoClient
from sdk.config import SDKConfig
from utils.logger import logger
import datetime

# Initialize MongoDB client
client = MongoClient(SDKConfig.MONGODB_URI)
db = client[SDKConfig.DATABASE_NAME]
game_data_collection = db['game_data']

def store_game_data(player_id, game_type, win_loss, shot_type, foul, reaction_time):
    """Store the game data such as win/loss, shot type, foul, and reaction time in MongoDB."""
    data = {
        "player_id": player_id,
        "game_type": game_type,
        "win_loss": win_loss,
        "shot_type": shot_type,
        "foul": foul,
        "reaction_time": reaction_time,
        "timestamp": datetime.datetime.utcnow()
    }

    try:
        game_data_collection.insert_one(data)
        logger.info(f"Stored game data for player {player_id}")
    except Exception as e:
        logger.error(f"Error storing game data: {e}")
