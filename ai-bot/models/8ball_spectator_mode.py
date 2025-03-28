import time
from utils.logger import logger
from utils.db_utils import get_collection, store_processed_data
from ai_training.8ball_training import train_8ball_playstyle_classifier, classify_8ball_playstyle

class SpectatorMode:
    """
    The AI bot observes 5 games before unlocking itself.
    It collects data, refines predictions, and then starts competing.
    """
    
    def __init__(self):
        self.games_observed = 0
        self.max_observation_games = 5
        self.observation_data = []
        self.model, self.scaler = train_8ball_playstyle_classifier()  # Train the classifier at initialization
    
    def observe_game(self, game_data):
        """
        Observe and store game data for AI learning before unlocking the bot.
        
        Args:
            game_data (dict): Game statistics including shot power, accuracy, fouls.
        """
        if self.games_observed < self.max_observation_games:
            logger.info(f"Observing game {self.games_observed + 1}/{self.max_observation_games}")
            self.observation_data.append(game_data)
            self.games_observed += 1
        else:
            logger.info("AI has completed its observations and will now play.")
            self.unlock_ai()
    
    def unlock_ai(self):
        """
        Unlock the AI to start competing after observing enough games.
        """
        logger.info("AI unlocked and ready to play.")
        
        # Process collected data for playstyle analysis
        for game in self.observation_data:
            shot_power = game.get("shot_power", 50)
            accuracy = game.get("accuracy", 0.7)
            foul_rate = game.get("foul_rate", 0.1)

            playstyle = classify_8ball_playstyle(self.model, self.scaler, shot_power, accuracy, foul_rate)
            logger.info(f"AI learned from observed game: {game['game_id']} - Predicted Playstyle: {playstyle}")

        # Store AI training data into MongoDB for future refinement
        store_processed_data(self.observation_data, "eight_ball_training")
    
    def process_spectator_mode(self, player_id):
        """
        Query recent games and observe them before unlocking AI.
        
        Args:
            player_id (str): Unique identifier for the player.
        """
        collection = get_collection("eight_ball_game_data")
        recent_games = list(collection.find({"player_id": player_id}).sort("game_time", -1).limit(self.max_observation_games))

        if not recent_games:
            logger.warning(f"No games found for player {player_id}. Cannot enter spectator mode.")
            return

        for game in recent_games:
            self.observe_game(game)
        
        # If all observations are complete, unlock the AI
        if self.games_observed >= self.max_observation_games:
            self.unlock_ai()
