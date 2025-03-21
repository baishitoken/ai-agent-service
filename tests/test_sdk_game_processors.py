import pytest
from sdk.game_processors import process_blackjack_data, process_chess_data, process_eight_ball_data
from models.blackjack_model import BlackjackGameData
from models.chess import ChessGameData
from models.eight_ball import EightBallGameData


# Test: Process Blackjack data
def test_process_blackjack_game_data():
    game_data = {
        "players": [
            {"username": "player1", "games_played": 10, "games_won": 5}
        ]
    }
    result = process_blackjack_data(game_data)
    assert isinstance(result, BlackjackGameData)
    assert len(result.players) == 1


# Test: Process Chess data
def test_process_chess_game_data():
    game_data = {
        "players": [
            {"username": "player1", "games_played": 50, "games_won": 25}
        ]
    }
    result = process_chess_data(game_data)
    assert isinstance(result, ChessGameData)
    assert len(result.players) == 1


# Test: Process 8-ball data
def test_process_eight_ball_game_data():
    game_data = {
        "players": [
            {"username": "player1", "games": 10, "games_won": 5}
        ]
    }
    result = process_eight_ball_data(game_data)
    assert isinstance(result, EightBallGameData)
    assert len(result.players) == 1
