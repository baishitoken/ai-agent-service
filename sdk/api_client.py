import requests
from sdk.config import SDKConfig
from utils.logger import logger

class APIClient:
    def __init__(self, base_url: str = SDKConfig.BASE_URL):
        self.base_url = base_url

    def process_game_data(self, game_type: str, game_data: dict):
        """Send a request to the API to process game data."""
        url = f"{self.base_url}/api/v1/process-game-data"
        payload = {"game": game_type, "data": game_data}
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            logger.info(f"API request successful: {response.status_code}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return {"error": "API request failed", "details": str(e)}
