import time
import random
from pymongo import MongoClient
from player_profile import PlayerProfile

class BlockchainMockListener:
    """
    Polls a mock chain to trigger profile updates on events.
    """
    def __init__(
        self,
        mongo_uri: str = "mongodb://localhost:27017/",
        db_name: str = "ai_agent_case_study",
        interval: float = 2.0
    ):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.interval = interval
        self.events = ['game_played', 'game_won', 'game_lost']

    def _simulate_event(self) -> None:
        evt = random.choice(self.events)
        pid = random.choice([d['player_id'] for d in self.db['player_profiles'].find()])
        acc = random.uniform(0.4, 0.95)
        fouls = random.randint(0, 3)
        power = random.uniform(30, 90)
        aggr = random.randint(4, 12)
        deff = random.randint(3, 10)
        win = (evt != 'game_lost')
        profile = PlayerProfile(pid, self.db)
        profile.update_after_game(
            accuracy=acc,
            fouls=fouls,
            shot_power=power,
            aggressive_shots=aggr,
            defensive_shots=deff,
            win=win
        )
        print(f"[Event: {evt}] Updated {pid}")

    def start(self) -> None:
        print("Starting mock listener...")
        try:
            while True:
                self._simulate_event()
                time.sleep(self.interval)
        except KeyboardInterrupt:
            print("Listener stopped.")