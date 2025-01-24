import unittest
from unittest.mock import patch, MagicMock
from utils.db_utils import store_processed_data

class TestDbUtils(unittest.TestCase):
    @patch("utils.db_utils.get_db_connection")
    def test_store_processed_data_single(self, mock_get_db_connection):
        mock_client = MagicMock()
        mock_db = mock_client["game_data_db"]
        mock_collection = mock_db["8ball_game_data"]
        mock_get_db_connection.return_value = mock_client

        data = {
            "username": "player1",
            "games": 10,
            "winRate": 0.5
        }

        store_processed_data(data, "8ball")

        mock_collection.insert_one.assert_called_once_with(data)

    @patch("utils.db_utils.get_db_connection")
    def test_store_processed_data_multiple(self, mock_get_db_connection):
        mock_client = MagicMock()
        mock_db = mock_client["game_data_db"]
        mock_collection = mock_db["8ball_game_data"]
        mock_get_db_connection.return_value = mock_client

        data = [
            {"username": "player1", "games": 10, "winRate": 0.5},
            {"username": "player2", "games": 15, "winRate": 0.6}
        ]

        store_processed_data(data, "8ball")

        mock_collection.insert_many.assert_called_once_with(data)

if __name__ == "__main__":
    unittest.main()
