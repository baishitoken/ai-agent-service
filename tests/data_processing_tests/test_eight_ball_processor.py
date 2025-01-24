import unittest
from utils.processors.eight_ball_processor import process_8ball_data

class TestEightBallProcessor(unittest.TestCase):
    def setUp(self):
        """Set up sample data for tests."""
        self.sample_data = {
            "players": [
                {
                    "username": "test_player",
                    "games_won": 5,
                    "games": 10,
                    "balls_potted": 20,
                    "fouls": 2,
                    "game_data": [
                        {"timestamp": 1, "power": 50, "balls_potted": [1, 2]},
                        {"timestamp": 2, "power": 30, "balls_potted": []},
                        {"timestamp": 3, "power": 60, "balls_potted": [3]},
                    ]
                }
            ]
        }

    def test_first_turn(self):
        """Test that the first turn is correctly identified."""
        processed = process_8ball_data(self.sample_data)
        player = processed[0]
        self.assertIn("firstTurn", player)
        self.assertTrue(player["firstTurn"])

    def test_win_rate(self):
        """Test that the win rate is calculated correctly."""
        processed = process_8ball_data(self.sample_data)
        player = processed[0]
        self.assertEqual(player["winRate"], 0.5)

    def test_potting_accuracy(self):
        """Test that the potting accuracy is calculated correctly."""
        processed = process_8ball_data(self.sample_data)
        player = processed[0]
        self.assertEqual(player["pottingAccuracy"], 0.6666666666666666)  # 2/3 pots

    def test_average_fouls(self):
        """Test that the average fouls are calculated correctly."""
        processed = process_8ball_data(self.sample_data)
        player = processed[0]
        self.assertIn("averageFouls", player)
        self.assertEqual(player["averageFouls"], 0.2)  # 2 fouls over 10 games

    def test_aggressive_shot_ratio(self):
        """Test that aggressive shot ratio is calculated correctly."""
        processed = process_8ball_data(self.sample_data)
        player = processed[0]
        self.assertIn("aggressiveShotRatio", player)
        self.assertEqual(player["aggressiveShotRatio"], 2 / 3)  # 2 shots with pots

    def test_defensive_shot_ratio(self):
        """Test that defensive shot ratio is calculated correctly."""
        processed = process_8ball_data(self.sample_data)
        player = processed[0]
        self.assertIn("defensiveShotRatio", player)
        self.assertEqual(player["defensiveShotRatio"], 1 / 3)  # 1 shot without pots

    def test_most_common_ball_hit(self):
        """Test that the most common ball hit is identified."""
        sample_data_with_hits = {
            "players": [
                {
                    "username": "test_player",
                    "games_won": 5,
                    "games": 10,
                    "game_data": [
                        {"timestamp": 1, "power": 50, "ball_hit": 8},
                        {"timestamp": 2, "power": 30, "ball_hit": 8},
                        {"timestamp": 3, "power": 60, "ball_hit": 7},
                    ]
                }
            ]
        }
        processed = process_8ball_data(sample_data_with_hits)
        player = processed[0]
        self.assertIn("mostCommonBallHit", player)
        self.assertEqual(player["mostCommonBallHit"], 8)

    def test_wall_hits(self):
        """Test that wall hits are calculated correctly."""
        sample_data_with_walls = {
            "players": [
                {
                    "username": "test_player",
                    "games_won": 5,
                    "games": 10,
                    "game_data": [
                        {"timestamp": 1, "walls_hit": [0, 1]},
                        {"timestamp": 2, "walls_hit": [1]},
                        {"timestamp": 3, "walls_hit": []},
                    ]
                }
            ]
        }
        processed = process_8ball_data(sample_data_with_walls)
        player = processed[0]
        self.assertIn("averageWallHits", player)
        self.assertEqual(player["averageWallHits"], 1.0)  # 3 wall hits over 3 shots

    def test_potting_streak(self):
        """Test that the maximum potting streak is calculated correctly."""
        processed = process_8ball_data(self.sample_data)
        player = processed[0]
        self.assertIn("maxPottingStreak", player)
        self.assertEqual(player["maxPottingStreak"], 1)  # Longest streak: 1 pot in a row

    def test_cue_position_analysis(self):
        """Test that the average cue ball position is calculated correctly."""
        sample_data_with_positions = {
            "players": [
                {
                    "username": "test_player",
                    "games_won": 5,
                    "games": 10,
                    "game_data": [
                        {"timestamp": 1, "cue_ball_position": [10, 20]},
                        {"timestamp": 2, "cue_ball_position": [30, 40]},
                        {"timestamp": 3, "cue_ball_position": [50, 60]},
                    ]
                }
            ]
        }
        processed = process_8ball_data(sample_data_with_positions)
        player = processed[0]
        self.assertIn("averageCuePosition", player)
        self.assertEqual(player["averageCuePosition"], {"x": 30.0, "y": 40.0})

if __name__ == "__main__":
    unittest.main()