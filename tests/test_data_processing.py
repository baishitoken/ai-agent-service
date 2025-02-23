import unittest
from utils.processors.eight_ball_processor import process_8ball_data

class TestEightBallProcessor(unittest.TestCase):
    def test_process_8ball_data(self):
        sample_data = {
            "players": [
                {
                    "username": "test_player",
                    "games_won": 5,
                    "games": 10,
                    "game_data": [
                        {"timestamp": 1, "power": 50, "balls_potted": [1, 2]},
                        {"timestamp": 2, "power": 30, "balls_potted": []},
                    ]
                }
            ]
        }
        processed = process_8ball_data(sample_data)
        player = processed[0]

        self.assertIn("firstTurn", player)
        self.assertEqual(player["winRate"], 0.5)
        self.assertEqual(player["pottingAccuracy"], 1.0)

if __name__ == "__main__":
    unittest.main()
