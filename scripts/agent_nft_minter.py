import os
import json
import hashlib
from typing import Dict

class AgentNFTMinter:
    """
    Creates a JSON-based NFT metadata file for an agent.
    """
    def __init__(
        self,
        agent_weights_path: str,
        profile_data: Dict,
        output_dir: str = "nft_mints"
    ):
        self.agent_weights_path = agent_weights_path
        self.profile = profile_data
        os.makedirs(output_dir, exist_ok=True)
        self.output_dir = output_dir

    def _hash_agent(self) -> str:
        with open(self.agent_weights_path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()

    def mint(self) -> str:
        metadata = {
            'player_id': self.profile['player_id'],
            'games_played': self.profile['games_played'],
            'avg_accuracy': round(self.profile['average_accuracy'], 4),
            'win_rate': round(self.profile['win_rate'], 4),
            'agent_hash': self._hash_agent()
        }
        filename = f"{metadata['player_id']}_nft.json"
        path = os.path.join(self.output_dir, filename)
        with open(path, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"Minted NFT metadata at {path}")
        return path