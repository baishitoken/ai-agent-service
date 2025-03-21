import pytest
from sdk.core import process_game_data
from sdk.utils import handle_exception
from sdk.exceptions import SDKError


# Test: Process valid game data (Blackjack)
def test_process_valid_blackjack_data():
    game_data = {
        "players": [
            {"username": "player1", "games_played": 10, "games_won": 5}
        ]
    }
    result = process_game_data("blackjack", game_data)
    assert result["status"] == "success"
    assert "Data for blackjack processed." in result["message"]


# Test: Handle invalid game type
def test_invalid_game_type():
    game_data = {
        "players": [
            {"username": "player1", "games_played": 10, "games_won": 5}
        ]
    }
    result = process_game_data("invalid_game", game_data)
    assert result["error"] == "No processor available for game type 'invalid_game'"


# Test: Handle exception correctly
def test_handle_exception():
    try:
        raise SDKError("Test error")
    except SDKError as e:
        result = handle_exception(e, "test handle exception")
        assert "Test error" in result["error"]
        assert "test handle exception" in result["error"]
