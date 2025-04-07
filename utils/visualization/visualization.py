import os
import matplotlib.pyplot as plt
from player_profile import PlayerProfile
from typing import List

class Visualizer:
    """
    Generates and saves trend charts for players.
    """
    def __init__(
        self,
        db,
        player_ids: List[str]
    ):
        self.db = db
        self.player_ids = player_ids

    def generate_charts(self, save_dir: str = "charts") -> None:
        os.makedirs(save_dir, exist_ok=True)
        for pid in self.player_ids:
            profile = PlayerProfile(pid, self.db)
            self._plot(
                profile.data['accuracy_trend'],
                pid + '_accuracy',
                'Accuracy (%)',
                save_dir
            )
            self._plot(
                profile.data['foul_trend'],
                pid + '_fouls',
                'Fouls per Game',
                save_dir
            )

    def _plot(self, series: List[float], name: str, ylabel: str, save_dir: str) -> None:
        if not series:
            return
        plt.figure()
        plt.plot(range(1, len(series)+1), series, marker='o')
        plt.title(name.replace('_', ' ').title())
        plt.xlabel('Game')
        plt.ylabel(ylabel)
        plt.grid(True)
        path = os.path.join(save_dir, name + '.png')
        plt.savefig(path)
        plt.close()
        print(f"Saved {path}")