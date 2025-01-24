import unittest
from pydantic import ValidationError
from models.chess import GameChessPayload, PlayerData, MoveData

class TestModelsChess(unittest.TestCase):
    def test_valid_payload(self):
        # Example of a valid chess payload
        valid_payload = {
            "game": "chess",
            "data": {
                "players": [
                    {
                        "username": "player1",
                        "rating": 1500,
                        "games_played": 50,
                        "games_won": 25,
                        "games_lost": 20,
                        "games_drawn": 5,
                        "moves": [
                            {
                                "move_number": 1,
                                "player": "white",
                                "from_square": "e2",
                                "to_square": "e4",
                                "piece": "pawn",
                                "captured_piece": None,
                                "check": False,
                                "checkmate": False,
                            },
                            {
                                "move_number": 2,
                                "player": "black",
                                "from_square": "e7",
                                "to_square": "e5",
                                "piece": "pawn",
                                "captured_piece": None,
                                "check": False,
                                "checkmate": False,
                            },
                        ],
                    }
                ]
            },
        }

        # Validate payload
        validated_payload = GameChessPayload(**valid_payload)
        self.assertEqual(validated_payload.game, "chess")
        self.assertEqual(validated_payload.data["players"][0]["username"], "player1")

    def test_invalid_payload_missing_field(self):
        # Example of an invalid chess payload (missing "games_played" field)
        invalid_payload = {
            "game": "chess",
            "data": {
                "players": [
                    {
                        "username": "player1",
                        "rating": 1500,
                        "games_won": 25,
                        "games_lost": 20,
                        "games_drawn": 5,
                        "moves": [
                            {
                                "move_number": 1,
                                "player": "white",
                                "from_square": "e2",
                                "to_square": "e4",
                                "piece": "pawn",
                                "captured_piece": None,
                                "check": False,
                                "checkmate": False,
                            }
                        ],
                    }
                ]
            },
        }

        # Validate payload and expect an error
        with self.assertRaises(ValidationError) as context:
            GameChessPayload(**invalid_payload)

        self.assertIn("field required", str(context.exception))
        self.assertIn("games_played", str(context.exception))


if __name__ == "__main__":
    unittest.main()
