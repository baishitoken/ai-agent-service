import unittest
from utils.processors.blackjack_processor import process_blackjack_data

class TestBlackjackProcessor(unittest.TestCase):
    def setUp(self):
        self.sample_data = {
            "players": [
                {
                    "username": "player1",
                    "games_won": 10,
                    "games_played": 20,
                    "game_history": [
                        {"result": "win", "final_score": 21, "opponent_score": 18},
                        {"result": "loss", "final_score": 19, "opponent_score": 20},
                        {"result": "win", "final_score": 21, "opponent_score": 16},
                        {"result": "tie", "final_score": 20, "opponent_score": 20},
                        {"result": "win", "final_score": 21, "opponent_score": 17},
                    ],
                    "rounds": [
                        {"bet": 10, "result": "win", "final_hand": ["10H", "AD"]},
                        {"bet": 15, "result": "loss", "final_hand": ["8C", "5D", "7S"]},
                    ]
                }
            ]
        }

    def test_process_blackjack_data(self):
        processed_data = process_blackjack_data(self.sample_data)
        player = processed_data[0]

        self.assertIn("winRate", player)
        self.assertEqual(player["winRate"], 0.5)
        self.assertIn("averageBet", player)
        self.assertEqual(player["averageBet"], 12.5)
        self.assertIn("blackjackRate", player)
        self.assertEqual(player["blackjackRate"], 0.5)
        self.assertIn("maxWinStreak", player)
        self.assertIn("maxLossStreak", player)

if __name__ == "__main__":
    unittest.main()
