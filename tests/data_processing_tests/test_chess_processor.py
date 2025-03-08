import unittest
from utils.processors.chess_processor import process_chess_data

class TestChessProcessor(unittest.TestCase):
    def setUp(self):
        """Set up sample data for tests."""
        self.sample_data = {
            "players": [
                {
                    "username": "chess_master",
                    "rating": 1500,
                    "games_played": 20,
                    "games_won": 15,
                    "games_lost": 5,
                    "moves": [
                        {"move_number": 1, "player": "white", "from_square": "e2", "to_square": "e4", "piece": "pawn"},
                        {"move_number": 2, "player": "black", "from_square": "e7", "to_square": "e5", "piece": "pawn"},
                        {"move_number": 3, "player": "white", "from_square": "d2", "to_square": "d4", "piece": "pawn"},
                    ]
                }
            ]
        }

    def test_win_rate(self):
        """Test that the win rate is calculated correctly."""
        processed = process_chess_data(self.sample_data)
        player = processed[0]
        self.assertEqual(player["winRate"], 0.75)

    def test_total_moves(self):
        """Test that total moves are counted correctly."""
        processed = process_chess_data(self.sample_data)
        player = processed[0]
        self.assertEqual(player["totalMoves"], 3)

    def test_average_move_time(self):
        """Test average move time calculation."""
        sample_data_with_time = {
            "players": [
                {
                    "username": "chess_master",
                    "rating": 1500,
                    "games_played": 20,
                    "games_won": 15,
                    "moves": [
                        {"move_number": 1, "player": "white", "time": 10},
                        {"move_number": 2, "player": "black", "time": 20},
                        {"move_number": 3, "player": "white", "time": 30},
                    ]
                }
            ]
        }
        processed = process_chess_data(sample_data_with_time)
        player = processed[0]
        self.assertEqual(player["averageMoveTime"], 20.0)

    def test_captured_pieces(self):
        """Test captured piece analysis."""
        sample_data_with_captures = {
            "players": [
                {
                    "username": "chess_master",
                    "rating": 1500,
                    "games_played": 20,
                    "games_won": 15,
                    "moves": [
                        {"move_number": 1, "player": "white", "captured_piece": "pawn"},
                        {"move_number": 2, "player": "black"},
                        {"move_number": 3, "player": "white", "captured_piece": "knight"},
                    ]
                }
            ]
        }
        processed = process_chess_data(sample_data_with_captures)
        player = processed[0]
        self.assertEqual(player["totalCapturedPieces"], 2)
        self.assertEqual(player["mostCapturedPiece"], "pawn")

    def test_check_and_checkmate(self):
        """Test analysis of checks and checkmates."""
        sample_data_with_checks = {
            "players": [
                {
                    "username": "chess_master",
                    "rating": 1500,
                    "games_played": 20,
                    "games_won": 15,
                    "moves": [
                        {"move_number": 1, "player": "white", "check": True},
                        {"move_number": 2, "player": "black"},
                        {"move_number": 3, "player": "white", "checkmate": True},
                    ]
                }
            ]
        }
        processed = process_chess_data(sample_data_with_checks)
        player = processed[0]
        self.assertEqual(player["totalChecks"], 1)
        self.assertEqual(player["totalCheckmates"], 1)

    def test_piece_movement_patterns(self):
        """Test piece movement pattern analysis."""
        processed = process_chess_data(self.sample_data)
        player = processed[0]
        self.assertIn("pieceMovementPatterns", player)
        self.assertEqual(player["pieceMovementPatterns"], {"pawn": 3})

    def test_positional_preferences(self):
        """Test positional preference analysis."""
        processed = process_chess_data(self.sample_data)
        player = processed[0]
        self.assertIn("positionalPreferences", player)
        self.assertEqual(player["positionalPreferences"], {
            "mostCommonSquare": "e4",
            "squareFrequencies": {"e4": 1, "e5": 1, "d4": 1}
        })

    def test_opening_preferences(self):
        """Test opening repertoire analysis."""
        sample_data_with_openings = {
            "players": [
                {
                    "username": "chess_master",
                    "rating": 1500,
                    "games_played": 20,
                    "games_won": 15,
                    "moves": [
                        {"move_number": 1, "player": "white", "opening": "Ruy Lopez"},
                        {"move_number": 2, "player": "black"},
                        {"move_number": 3, "player": "white", "opening": "Ruy Lopez"},
                    ]
                }
            ]
        }
        processed = process_chess_data(sample_data_with_openings)
        player = processed[0]
        self.assertEqual(player["openingPreferences"], {
            "mostCommonOpening": "Ruy Lopez",
            "openingFrequencies": {"Ruy Lopez": 2}
        })

if __name__ == "__main__":
    unittest.main()
