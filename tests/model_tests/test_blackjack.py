import unittest
from pydantic import ValidationError
from models.blackjack import BlackjackPayload, PlayerData, RoundData

class TestBlackjackModel(unittest.TestCase):
    def test_valid_blackjack_payload(self):
        valid_data = {
            "game": "blackjack",
            "players": [
                {
                    "username": "player1",
                    "games_won": 10,
                    "games_played": 20,
                    "total_bet_amount": 5000,
                    "game_history": [
                        {"result": "win", "bet": 200, "final_hand_value": 21, "bust": False},
                        {"result": "loss", "bet": 300, "final_hand_value": 22, "bust": True}
                    ]
                }
            ]
        }
        payload = BlackjackPayload(**valid_data)
        self.assertEqual(payload.game, "blackjack")
        self.assertEqual(len(payload.players), 1)
        self.assertEqual(payload.players[0].username, "player1")
        self.assertEqual(payload.players[0].winRate, 0.5)
        self.assertEqual(payload.players[0].bustRate, 0.5)

    def test_invalid_blackjack_payload(self):
        invalid_data = {
            "game": "blackjack",
            "players": [
                {
                    "username": "player2",
                    "games_won": "invalid",  # Should be int
                    "games_played": 20,
                    "total_bet_amount": "invalid",  # Should be float or int
                    "game_history": []
                }
            ]
        }
        with self.assertRaises(ValidationError):
            BlackjackPayload(**invalid_data)

    def test_missing_fields(self):
        missing_fields_data = {
            "game": "blackjack",
            "players": [
                {
                    "username": "player3",
                    "games_played": 20  # Missing required fields like games_won
                }
            ]
        }
        with self.assertRaises(ValidationError):
            BlackjackPayload(**missing_fields_data)

if __name__ == "__main__":
    unittest.main()
