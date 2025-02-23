import unittest
from pydantic import ValidationError
from models.eight_ball import Game8BallPayload, PlayerData, TurnData

class TestModels8Ball(unittest.TestCase):
    def test_valid_payload(self):
        # Example of a valid payload
        valid_payload = {
            "game": "8ball",
            "data": {
                "players": [
                    {
                        "username": "player1",
                        "rating": 1000,
                        "games": 10,
                        "games_won": 5,
                        "games_lost": 5,
                        "balls_potted": 50,
                        "fouls": 2,
                        "eightballs_potted": 3,
                        "favourite": "striped",
                        "game_data": [
                            {
                                "timestamp": 1737678409,
                                "cue_ball_position": [21, 302],
                                "power": 30.5,
                                "angle": 45.0,
                                "ball_hit": 9,
                                "balls_collided": [1, 2, 3],
                                "balls_potted": [3],
                                "walls_hit": [0, 1]
                            }
                        ]
                    }
                ]
            }
        }

        # Validate payload
        validated_payload = Game8BallPayload(**valid_payload)
        self.assertEqual(validated_payload.game, "8ball")
        self.assertEqual(validated_payload.data["players"][0]["username"], "player1")

    def test_invalid_payload_missing_field(self):
        # Example of an invalid payload (missing "games" field for a player)
        invalid_payload = {
            "game": "8ball",
            "data": {
                "players": [
                    {
                        "username": "player1",
                        "rating": 1000,
                        "games_won": 5,
                        "games_lost": 5,
                        "balls_potted": 50,
                        "fouls": 2,
                        "eightballs_potted": 3,
                        "favourite": "striped",
                        "game_data": [
                            {
                                "timestamp": 1737678409,
                                "cue_ball_position": [21, 302],
                                "power": 30.5,
                                "angle": 45.0,
                                "ball_hit": 9,
                                "balls_collided": [1, 2, 3],
                                "balls_potted": [3],
                                "walls_hit": [0, 1]
                            }
                        ]
                    }
                ]
            }
        }

        # Validate payload and expect an error
        with self.assertRaises(ValidationError) as context:
            Game8BallPayload(**invalid_payload)

        self.assertIn("field required", str(context.exception))
        self.assertIn("games", str(context.exception))

if __name__ == "__main__":
    unittest.main()
