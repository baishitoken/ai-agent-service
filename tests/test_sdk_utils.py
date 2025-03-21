import pytest
from sdk.utils import log_request, log_response, validate_json, sanitize_input
from sdk.exceptions import SDKError
from sdk.models import GamePayload


# Test: Validate JSON data using the schema
def test_validate_json_valid():
    valid_data = {
        "game": "blackjack",
        "data": {
            "players": [{"username": "player1", "games_played": 10, "games_won": 5}]
        }
    }
    result = validate_json(valid_data, GamePayload)
    assert result is True


# Test: Handle invalid JSON data
def test_validate_json_invalid():
    invalid_data = {
        "game": "blackjack"
    }
    result = validate_json(invalid_data, GamePayload)
    assert result is False


# Test: Sanitize input data
def test_sanitize_input():
    input_data = {
        "username": "player1",
        "password": "secret_password",
        "secret": "sensitive_data"
    }
    sanitized_data = sanitize_input(input_data)
    assert "password" not in sanitized_data
    assert "secret" not in sanitized_data
    assert "username" in sanitized_data


# Test: Handle exception logging
def test_handle_exception():
    try:
        raise SDKError("Test error")
    except SDKError as e:
        result = handle_exception(e, "test handle exception")
        assert "Test error" in result["error"]
        assert "test handle exception" in result["error"]
