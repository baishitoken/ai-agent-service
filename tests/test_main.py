import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from main import app

class TestMain(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch("utils.data_processing.get_processor")
    @patch("utils.db_utils.store_processed_data")
    def test_process_game_data_success(self, mock_store_processed_data, mock_get_processor):
        mock_processor = MagicMock()
        mock_processor.return_value = [{"username": "player1", "winRate": 0.5}]
        mock_get_processor.return_value = mock_processor

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

        response = self.app.post(
            "/process-game-data",
            json=post_data,
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Data processed and stored successfully", response.get_json().get("message"))
        mock_processor.assert_called_once_with(post_data["data"])
        mock_store_processed_data.assert_called_once_with(
            mock_processor.return_value, "8ball"
        )

    @patch("utils.data_processing.get_processor")
    def test_process_game_data_invalid_game(self, mock_get_processor):
        mock_get_processor.return_value = None

        post_data = {
            "game": "invalid_game",
            "data": {
                "players": []
            }
        }

        response = self.app.post(
            "/process-game-data",
            json=post_data,
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("No processor available for game type", response.get_json().get("error"))

    def test_process_game_data_missing_fields(self):
        post_data = {
            "data": {
                "players": []
            }
        }

        response = self.app.post(
            "/process-game-data",
            json=post_data,
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid request. 'game' and 'data' fields are required", response.get_json().get("error"))

if __name__ == "__main__":
    unittest.main()
