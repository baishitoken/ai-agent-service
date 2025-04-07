import os
import json
from pymongo import MongoClient
from ai_agent import DuelingDQNAgent
from game_simulation import GameSimulator
from trend_analysis import TrendAnalyzer
from utils.visualization import Visualizer

class CaseStudyRunner:
    """
    Orchestrates end-to-end case study: simulation, profiling, trend analysis, and charting.
    """
    def __init__(
        self,
        mongo_uri: str = "mongodb://localhost:27017/",
        db_name: str = "ai_agent_case_study",
        results_dir: str = "results"
    ):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.results_dir = results_dir
        os.makedirs(self.results_dir, exist_ok=True)

        # Initialize agent and simulator
        self.agent = DuelingDQNAgent(
            state_size=5, action_size=3, use_per=True
        )
        self.simulator = GameSimulator(
            db=self.db,
            agent=self.agent,
            player_ids=["user123", "user456", "user789"],
            exploration_rate=0.2
        )

    def reset(self) -> None:
        """Clear stored profiles and reset agent weights."""
        self.db['player_profiles'].delete_many({})
        # reinitialize target network
        self.agent.update_target_model()

    def run(self, games_per_player: int = 50) -> None:
        """Execute simulations, save profiles, analyze trends, and generate charts."""
        self.reset()
        total_games = games_per_player * len(self.simulator.player_ids)
        results = self.simulator.run(total_games)

        # Save agent
        agent_path = os.path.join(self.results_dir, "agent_weights.h5")
        self.agent.save(agent_path)

        # Export profiles and trend summaries
        summary = {}
        for pid in self.simulator.player_ids:
            profile = self.db['player_profiles'].find_one({"player_id": pid})
            with open(os.path.join(self.results_dir, f"{pid}_profile.json"), 'w') as f:
                json.dump(profile, f, default=str, indent=2)

            analyzer = TrendAnalyzer(profile=type('P', (), {'data': profile}))
            summary[pid] = analyzer.analyze()

        with open(os.path.join(self.results_dir, "trend_summary.json"), 'w') as f:
            json.dump(summary, f, indent=2)

        # Generate Visuals
        viz = Visualizer(db=self.db, player_ids=self.simulator.player_ids)
        viz.generate_charts(self.results_dir)

        print(f"Case study complete! Results in {self.results_dir}/")