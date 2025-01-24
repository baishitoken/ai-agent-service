import unittest
from unittest.mock import patch, MagicMock
from config import Config
from flask import Flask
from main import app

class TestMain(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_flask_port_config(self):
        self.assertEqual(Config.FLASK_PORT, 5000)

    @patch("utils.data_processing.get_processor")
    @patch("utils.db_utils.store_processed_data")
    def test_process_game_data_success(self, mock_store_processed_data, mock_get_processor):
        # Mock the processor function
        mock_processor = MagicMock()
        mock_processor.return_value = [{"username": "player1", "winRate": 0.5}]
        mock_get_processor.return_value = mock_processor

        # Example POST data
        post_data = {
            "game": "8ball",
            "data": {
                "players": [
                    {
                        "username": "player1",
                        "games": 10,
                        "games_won": 5,
                        "game_data": []
                    }
                ]
            }
        }

        # Make POST request
        response = self.app.post(
            "/process-game-data",
            json=post_data,
            content_type="application/json"
        )

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertIn("Data processed and stored successfully", response.get_json().get("message"))
        mock_processor.assert_called_once_with(post_data["data"])
        mock_store_processed_data.assert_called_once_with(
            mock_processor.return_value, "8ball"
        )

    @patch("utils.data_processing.get_processor")
    def test_process_game_data_invalid_game(self, mock_get_processor):
        # Return None for invalid game
        mock_get_processor.return_value = None

        # Example POST data
        post_data = {
            "game": "invalid_game",
            "data": {
                "players": []
            }
        }

        # Make POST request
        response = self.app.post(
            "/process-game-data",
            json=post_data,
            content_type="application/json"
        )

        # Assertions
        self.assertEqual(response.status_code, 400)
        self.assertIn("No processor available for game type", response.get_json().get("error"))

    def test_process_game_data_missing_fields(self):
        # Missing "game" field in POST data
        post_data = {
            "data": {
                "players": []
            }
        }

        # Make POST request
        response = self.app.post(
            "/process-game-data",
            json=post_data,
            content_type="application/json"
        )

        # Assertions
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid request. 'game' and 'data' fields are required", response.get_json().get("error"))

    @patch("utils.db_utils.store_processed_data")
    @patch("utils.data_processing.get_processor")
    def test_process_game_data_store_failure(self, mock_get_processor, mock_store_processed_data):
        # Mock processor function
        mock_processor = MagicMock()
        mock_processor.return_value = [{"username": "player1", "winRate": 0.5}]
        mock_get_processor.return_value = mock_processor

        # Simulate failure in storing data
        mock_store_processed_data.side_effect = Exception("Database error")

        # Example POST data
        post_data = {
            "game": "chess",
            "data": {
                "players": [
                    {
                        "username": "player1",
                        "games": 10,
                        "games_won": 5,
                        "moves": []
                    }
                ]
            }
        }

        # Make POST request
        response = self.app.post(
            "/process-game-data",
            json=post_data,
            content_type="application/json"
        )

        # Assertions
        self.assertEqual(response.status_code, 500)
        self.assertIn("Database error", response.get_json().get("error"))

if __name__ == "__main__":
    unittest.main()
