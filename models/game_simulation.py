import random
import numpy as np
from typing import Dict, Any
from player_profile import PlayerProfile

class GameSimulator:
    """
    Simulates realistic games for players, feeding AI decisions and
    updating player profiles in MongoDB.
    """
    def __init__(
        self,
        db,
        agent,
        player_ids: list,
        exploration_rate: float = 0.1
    ):
        self.db = db
        self.agent = agent
        self.player_ids = player_ids
        self.exploration_rate = exploration_rate

    def _derive_state(self, profile: PlayerProfile) -> np.ndarray:
        acc = np.clip(random.gauss(profile.data['average_accuracy'], 0.05), 0, 1)
        fouls = profile.data['average_fouls'] / 10.0
        power = np.clip(random.uniform(0.3, 0.9), 0, 1)
        agg = profile.data['aggressiveness_score']
        wr = profile.data['win_rate']
        return np.array([acc, fouls, power, agg, wr])

    def simulate_game(self, player_id: str) -> Dict[str, Any]:
        profile = PlayerProfile(player_id, self.db)
        state = self._derive_state(profile)
        action = self.agent.act(state, explore=(random.random() < self.exploration_rate))

        win_prob = np.clip(0.4 + state[0]*0.6 + (state[3]-0.5)*0.2, 0.05, 0.95)
        win = random.random() < win_prob
        reward = 1.0 if win else -1.0

        next_state = np.clip(state + np.random.normal(0, 0.02, state.shape), 0, 1)
        self.agent.remember(state, action, reward, next_state, done=win)
        profile.update_after_game(
            accuracy=state[0],
            fouls=int(state[1]*10),
            shot_power=state[2]*100,
            aggressive_shots=random.randint(5, 15),
            defensive_shots=random.randint(5, 15),
            win=win
        )
        return {
            'player_id': player_id,
            'action': action,
            'win': win,
            'reward': reward
        }

    def run(self, games: int = 100) -> list:
        results = []
        for _ in range(games):
            pid = random.choice(self.player_ids)
            res = self.simulate_game(pid)
            self.agent.replay()
            results.append(res)
        return results