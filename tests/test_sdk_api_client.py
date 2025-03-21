import pytest
from sdk.api_client import APIClient
from sdk.config import SDKConfig


# Test: Initialize API Client
def test_api_client_init():
    api_client = APIClient(SDKConfig.BASE_URL)
    assert api_client.base_url == SDKConfig.BASE_URL


# Test: API Client successfully processes data (assuming the server is up)
@pytest.mark.skip(reason="API server must be running for this test")
def test_api_client_process_game_data():
    game_data = {
        "players": [
            {"username": "player1", "games_played": 10, "games_won": 5}
        ]
    }
    api_client = APIClient(SDKConfig.BASE_URL)
    response = api_client.process_game_data("blackjack", game_data)
    assert response["status_code"] == 200
    assert "Data processed and stored successfully" in response["data"]


# Test: API Client handles API failure (assuming the server is down)
@pytest.mark.skip(reason="API server must be running for this test")
def test_api_client_failure():
    game_data = {
        "players": [
            {"username": "player1", "games_played": 10, "games_won": 5}
        ]
    }
    api_client = APIClient("http://invalid_url")
    response = api_client.process_game_data("blackjack", game_data)
    assert response["error"] == "API request failed"
