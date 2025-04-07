import logging
timport pymongo
import datetime
from typing import Any, Dict, List, Optional
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PlayerProfile:
    """
    Manages a player's performance profile, storing historical metrics
    and computing analytics such as trends, smoothed averages, and anomalies.
    """
    def __init__(
        self,
        player_id: str,
        db: pymongo.database.Database,
        cache_enabled: bool = True,
        cache_ttl_seconds: int = 300
    ):
        self.player_id = player_id
        self.db = db
        self.collection = db['player_profiles']
        self.cache_enabled = cache_enabled
        self.cache_ttl = datetime.timedelta(seconds=cache_ttl_seconds)
        self._cache_timestamp: Optional[datetime.datetime] = None
        self.data: Dict[str, Any] = {
            "player_id": player_id,
            "created_at": datetime.datetime.utcnow(),
            "last_updated": datetime.datetime.utcnow(),
            "games_played": 0,
            "average_accuracy": 0.0,
            "average_fouls": 0.0,
            "average_shot_power": 0.0,
            "aggressiveness_score": 0.0,
            "win_rate": 0.0,
            "total_wins": 0,
            "total_losses": 0,
            "consecutive_wins": 0,
            "highest_consecutive_wins": 0,
            "performance_trend": [],
            "accuracy_trend": [],
            "foul_trend": [],
            "win_trend": [],
            "shot_power_trend": [],
            "aggressiveness_trend": [],
            "streaks": []
        }
        self.load()

    def load(self) -> None:
        """
        Load profile from MongoDB, with optional simple in-memory cache.
        """
        now = datetime.datetime.utcnow()
        if self.cache_enabled and self._cache_timestamp:
            if now - self._cache_timestamp < self.cache_ttl:
                logger.debug("Using cached profile for %s", self.player_id)
                return
        doc = self.collection.find_one({"player_id": self.player_id})
        if doc:
            self.data.update(doc)
        self._cache_timestamp = now
        logger.info("Profile loaded for %s", self.player_id)

    def save(self) -> None:
        """
        Persist current profile state to MongoDB.
        """
        self.data["last_updated"] = datetime.datetime.utcnow()
        try:
            self.collection.update_one(
                {"player_id": self.player_id},
                {"$set": self.data},
                upsert=True
            )
            logger.info("Profile saved for %s", self.player_id)
        except Exception as e:
            logger.exception("Failed to save profile for %s: %s", self.player_id, e)

    def calculate_aggressiveness(self, aggressive_shots: int, defensive_shots: int) -> float:
        """
        Compute ratio of aggressive shots to total shots.
        """
        total = aggressive_shots + defensive_shots
        return aggressive_shots / total if total > 0 else 0.0

    def update_after_game(
        self,
        accuracy: float,
        fouls: int,
        shot_power: float,
        aggressive_shots: int,
        defensive_shots: int,
        win: bool
    ) -> None:
        """
        Incorporate a new game's stats, updating averages, trends, and win/loss metrics.
        """
        self.load()
        self.data["games_played"] += 1
        n = self.data["games_played"]

        # Update progressive averages
        self.data["average_accuracy"] = self._progressive_average(
            self.data["average_accuracy"], accuracy, n
        )
        self.data["average_fouls"] = self._progressive_average(
            self.data["average_fouls"], fouls, n
        )
        self.data["average_shot_power"] = self._progressive_average(
            self.data["average_shot_power"], shot_power, n
        )

        # Aggression and updated score
        aggression = self.calculate_aggressiveness(aggressive_shots, defensive_shots)
        self.data["aggressiveness_score"] = self._progressive_average(
            self.data["aggressiveness_score"], aggression, n
        )

        # Win/Loss logic with streaks
        if win:
            self.data["total_wins"] += 1
            self.data["consecutive_wins"] += 1
            self.data["highest_consecutive_wins"] = max(
                self.data["highest_consecutive_wins"],
                self.data["consecutive_wins"]
            )
        else:
            if self.data["consecutive_wins"] > 0:
                self.data["streaks"].append({
                    "streak": self.data["consecutive_wins"],
                    "ended_at_game": n,
                    "timestamp": datetime.datetime.utcnow()
                })
            self.data["consecutive_wins"] = 0
            self.data["total_losses"] += 1

        self.data["win_rate"] = self.data["total_wins"] / max(1, (self.data["total_wins"] + self.data["total_losses"]))

        # Append to performance history
        entry = {
            "game_number": n,
            "accuracy": accuracy,
            "fouls": fouls,
            "shot_power": shot_power,
            "aggression": aggression,
            "win": win,
            "timestamp": datetime.datetime.utcnow()
        }
        self.data["performance_trend"].append(entry)
        self.data["accuracy_trend"].append(accuracy)
        self.data["foul_trend"].append(fouls)
        self.data["shot_power_trend"].append(shot_power)
        self.data["aggressiveness_trend"].append(aggression)
        self.data["win_trend"].append(1 if win else 0)

        self.save()

    def _progressive_average(self, current_avg: float, new_value: float, n: int) -> float:
        return ((current_avg * (n - 1)) + new_value) / n

    def get_recent_performance(self, last_n_games: int = 10) -> List[Dict[str, Any]]:
        return self.data["performance_trend"][-last_n_games:]

    def get_smoothed_trends(
        self,
        window_size: int = 5,
        method: str = "simple"
    ) -> Dict[str, np.ndarray]:
        """
        Return smoothed versions of each trend using moving average or EWMA.
        """
        def ewma(series, alpha=0.3):
            s = []
            prev = series[0]
            for x in series:
                prev = alpha * x + (1 - alpha) * prev
                s.append(prev)
            return np.array(s)

        trends = {}
        for key in ["accuracy_trend", "foul_trend", "shot_power_trend", "aggressiveness_trend", "win_trend"]:
            data = self.data.get(key, [])
            if method == "ewma":
                trends[key] = ewma(data)
            else:
                trends[key] = np.convolve(data, np.ones(window_size)/window_size, mode='valid') if len(data) >= window_size else np.array(data)
        return trends

    def detect_anomalies(
        self,
        threshold: float = 3.0,
        metric: str = "accuracy_trend"
    ) -> List[int]:
        """
        Simple z-score anomaly detection on specified metric trend. Returns indices of anomalies.
        """
        data = np.array(self.data.get(metric, []))
        if len(data) < 2:
            return []
        z_scores = np.abs((data - data.mean()) / data.std(ddof=1))
        return z_scores[z_scores > threshold].tolist()