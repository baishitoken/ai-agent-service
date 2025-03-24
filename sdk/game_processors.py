from models.blackjack import BlackjackGameData
from models.chess import ChessGameData
from models.eight_ball import EightBallGameData

def process_blackjack_data(game_data: dict) -> BlackjackGameData:
    """Process Blackjack game data."""
    # Process the game data and return a structured BlackjackGameData object
    return BlackjackGameData(players=game_data["players"])

def process_chess_data(game_data: dict) -> ChessGameData:
    """Process Chess game data."""
    # Process the game data and return a structured ChessGameData object
    return ChessGameData(players=game_data["players"])

def process_eight_ball_data(game_data: dict) -> EightBallGameData:
    """Process 8-ball game data."""
    # Process the game data and return a structured EightBallGameData object
    return EightBallGameData(players=game_data["players"])

def get_processor(game_type: str):
    """Get the processor function based on game type."""
    processors = {
        "blackjack": process_blackjack_data,
        "chess": process_chess_data,
        "eight_ball": process_eight_ball_data
    }
    return processors.get(game_type.lower())
