from utils.logger import logger

def process_8ball_data(game_data):
    """Process game data specific to 8-ball pool.

    Args:
        game_data (dict): The raw game data.

    Returns:
        list: The processed game data for all players.
    """
    players = game_data.get("players", [])
    logger.info("Processing data for %d players in 8-ball.", len(players))

    for player in players:
        logger.info("Processing data for player: %s", player.get("username"))

        # firstTurn
        player["firstTurn"] = player["game_data"][0]["timestamp"] == min(
            p["game_data"][0]["timestamp"] for p in players
        )

        # Win rate
        games_won = player.get("games_won", 0)
        games = player.get("games", 0)
        player["winRate"] = games_won / games if games > 0 else 0

        # Ball potting accuracy
        total_shots = len(player.get("game_data", []))
        total_potted = sum(len(turn.get("balls_potted", [])) for turn in player.get("game_data", []))
        player["pottingAccuracy"] = total_potted / total_shots if total_shots > 0 else 0

        # Player stats
        player["games"] += 1
        player["games_won"] += 1 if player.get("result", "") == "win" else 0
        player["games_lost"] += 1 if player.get("result", "") == "loss" else 0
        player["balls_potted"] += total_potted
        logger.debug("Calculated stats for player %s: %s", player.get("username"), player)

        player["averagePower"] = sum(turn.get("power", 0) for turn in player.get("game_data", [])) / total_shots if total_shots > 0 else 0

    return players
