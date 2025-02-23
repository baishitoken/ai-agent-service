from utils.logger import logger


def process_chess_data(game_data):
    """Process game data specific to BAISHI chess."""
    players = game_data.get("players", [])
    logger.info("Processing data for %d players in chess.", len(players))

    for player in players:
        logger.info("Processing data for player: %s", player.get("username"))

        # Win rate
        games_won = player.get("games_won", 0)
        games_played = player.get("games_played", 0)
        player["winRate"] = games_won / games_played if games_played > 0 else 0

        # Total moves
        total_moves = len(player.get("moves", []))
        player["totalMoves"] = total_moves

        player["aggressiveMoves"] = sum(
            1 for move in player.get("moves", []) if move.get("captured_piece")
        )

        logger.debug("Calculated stats for player %s: %s", player.get("username"), player)

    logger.info("Finished processing chess data.")
    return players
