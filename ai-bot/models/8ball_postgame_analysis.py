import numpy as np
from utils.logger import logger
from utils.db_utils import get_collection, update_document
from sklearn.linear_model import LinearRegression

def generate_postgame_summary(player_id, game_data):
    """
    Generate a post-game summary for a given player after an 8-ball match.
    
    Args:
        player_id (str): Unique identifier for the player.
        game_data (dict): Dictionary containing shot accuracy, win/loss, fouls, etc.
    
    Returns:
        dict: Summary of post-game stats.
    """
    total_shots = len(game_data.get("shot_attempts", []))
    total_potted = len(game_data.get("balls_potted", []))
    accuracy = total_potted / total_shots if total_shots > 0 else 0
    fouls = game_data.get("fouls", 0)
    win = game_data.get("result", "") == "win"

    summary = {
        "player_id": player_id,
        "accuracy": accuracy,
        "total_shots": total_shots,
        "total_potted": total_potted,
        "fouls": fouls,
        "win": win,
        "game_time": game_data.get("game_time", 0),
        "aggressive_shots": game_data.get("aggressive_shots", 0),
        "defensive_shots": game_data.get("defensive_shots", 0),
        "bank_shots": game_data.get("bank_shots", 0),
        "combo_shots": game_data.get("combo_shots", 0),
    }

    logger.info(f"Generated post-game summary for player {player_id}: {summary}")
    return summary

def analyze_trends(player_id, last_n_games=5):
    """
    Analyze recent performance trends for a player over their last 'n' games.
    
    Args:
        player_id (str): Unique identifier for the player.
        last_n_games (int): Number of recent games to analyze.

    Returns:
        dict: A trend analysis summary.
    """
    collection = get_collection("eight_ball_game_data")
    recent_games = list(collection.find({"player_id": player_id}).sort("game_time", -1).limit(last_n_games))

    if not recent_games:
        logger.warning(f"No recent games found for player {player_id}.")
        return {}

    accuracy_trend = [game["accuracy"] for game in recent_games]
    fouls_trend = [game["fouls"] for game in recent_games]
    win_rate = sum(1 for game in recent_games if game["win"]) / last_n_games

    # Use regression to detect performance trends
    x_axis = np.arange(len(accuracy_trend)).reshape(-1, 1)
    accuracy_model = LinearRegression().fit(x_axis, accuracy_trend)
    fouls_model = LinearRegression().fit(x_axis, fouls_trend)

    trend_summary = {
        "accuracy_trend": accuracy_trend,
        "accuracy_improving": accuracy_model.coef_[0] > 0,  # Positive trend means improving
        "fouls_trend": fouls_trend,
        "fouls_decreasing": fouls_model.coef_[0] < 0,  # Negative trend means fewer fouls
        "win_rate": win_rate,
    }

    logger.info(f"Trend analysis for player {player_id}: {trend_summary}")
    return trend_summary

def update_ai_model(player_id, game_data):
    """
    Update AI model parameters based on player's recent performance trends.
    
    Args:
        player_id (str): Unique identifier for the player.
        game_data (dict): Game statistics.

    Returns:
        None
    """
    trend_analysis = analyze_trends(player_id)

    if not trend_analysis:
        return

    ai_adjustments = {}

    # Adjust AI difficulty based on win rate and accuracy trends
    if trend_analysis["win_rate"] > 0.7 and trend_analysis["accuracy_improving"]:
        ai_adjustments["difficulty"] = "increase"
    elif trend_analysis["win_rate"] < 0.3:
        ai_adjustments["difficulty"] = "decrease"

    # Adjust AI fouls to match player fouling trends
    if trend_analysis["fouls_decreasing"]:
        ai_adjustments["ai_foul_tolerance"] = "increase"

    logger.info(f"Updating AI model with adjustments: {ai_adjustments}")

    # Update player document in database with AI adjustments
    update_document("eight_ball_game_data", player_id, {"ai_behavior_adjustments": ai_adjustments})
