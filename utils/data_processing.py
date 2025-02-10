from utils.processors.eight_ball_processor import process_8ball_data
from utils.processors.chess_processor import process_chess_data
from utils.processors.blackjack_processor import process_blackjack_data

def get_processor(game):
    """Get the appropriate data processor for the specified game.

    Args:
        game (str): The type of game.

    Returns:
        function: The processing function for the specified game, or None if not found.
    """
    processors = {
        "8ball": process_8ball_data,
        "chess": process_chess_data,
        "blackjack": process_blackjack_data
        # Add other games here, e.g., "chess": process_chess_data
    }
    return processors.get(game)
