from models.blackjack_model import BlackjackGameData
from models.chess import ChessGameData
from models.eight_ball import EightBallGameData

def process_blackjack_data(game_data):
    """Process Blackjack game data."""
    # Here, implement the Blackjack-specific processing logic
    return BlackjackGameData(players=game_data['players'])

def process_chess_data(game_data):
    """Process Chess game data."""
    # Implement Chess-specific processing logic
    return ChessGameData(players=game_data['players'])

def process_eight_ball_data(game_data):
    """Process 8-ball game data."""
    # Implement 8-ball-specific processing logic
    return EightBallGameData(players=game_data['players'])

def get_processor(game_type):
    """Get the processor function based on game type."""
    processors = {
        "blackjack": process_blackjack_data,
        "chess": process_chess_data,
        "eight_ball": process_eight_ball_data
    }
    return processors.get(game_type)
