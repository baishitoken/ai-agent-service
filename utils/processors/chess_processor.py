from utils.logger import logger

def process_chess_data(game_data):
    """Process game data specific to chess."""
    players = game_data.get("players", [])
    logger.info("Processing data for %d players in chess.", len(players))

    if not players:
        logger.warning("No players data found.")

    for player in players:
        logger.info("Processing data for player: %s", player.get("username"))

        # Calculate win rate
        calculate_win_rate(player)

        # Analyze moves
        analyze_moves(player)

        # Categorize moves by phase
        categorize_moves_by_phase(player)

        # Analyze captured pieces
        analyze_captured_pieces(player)

        # Analyze checks and checkmates
        analyze_checks_and_checkmates(player)

        # Advanced analysis: Piece movement patterns
        analyze_piece_movement_patterns(player)

        # Advanced analysis: Positional preferences
        analyze_positional_preferences(player)

        # Advanced analysis: Opening repertoire
        analyze_opening_repertoire(player)

        # Advanced analysis: Elo-based performance metrics
        analyze_elo_performance(player)

        # Advanced analysis: Positional heatmaps for board control
        analyze_board_control(player)

        # Advanced analysis: Opponent-specific performance metrics
        analyze_opponent_performance(player, players)

        # Analyze game history
        analyze_game_history(player)

        # Streak analysis
        analyze_streaks(player)

        # Opening analysis in game history
        analyze_openings_in_game_history(player)

        # Behavioral analysis based on game history
        analyze_behavioral_trends(player)

        # Additional analysis (e.g., total time spent)
        analyze_total_time_spent(player)

        # Add custom player stats (e.g., recent trends)
        add_custom_player_stats(player)

        logger.debug("Calculated advanced stats for player %s: %s", player.get("username"), player)

    logger.info("Finished processing chess data.")
    return players


def calculate_win_rate(player):
    """Calculate win rate for the player."""
    games_won = player.get("games_won", 0)
    games_played = player.get("games_played", 0)
    player["winRate"] = games_won / games_played if games_played > 0 else 0
    logger.debug("Player %s win rate: %f", player.get("username"), player["winRate"])


def analyze_moves(player):
    """Analyze the moves made by the player."""
    moves = player.get("moves", [])
    player["totalMoves"] = len(moves)
    player["averageMoveTime"] = sum(move.get("time", 0) for move in moves) / len(moves) if moves else 0
    logger.debug("Player %s total moves: %d, average move time: %f", player.get("username"), player["totalMoves"], player["averageMoveTime"])


def categorize_moves_by_phase(player):
    """Categorize moves made by the player into early, middle, and late game."""
    moves = player.get("moves", [])
    early_game_moves = [move for move in moves if move.get("move_number") <= 10]
    middle_game_moves = [move for move in moves if 11 <= move.get("move_number") <= 30]
    late_game_moves = [move for move in moves if move.get("move_number") > 30]
    player["earlyGameMoves"] = len(early_game_moves)
    player["middleGameMoves"] = len(middle_game_moves)
    player["lateGameMoves"] = len(late_game_moves)
    logger.debug("Player %s early, middle, and late game moves: %d, %d, %d", player.get("username"), player["earlyGameMoves"], player["middleGameMoves"], player["lateGameMoves"])


def analyze_captured_pieces(player):
    """Analyze the pieces captured by the player."""
    moves = player.get("moves", [])
    captured_pieces = [move.get("captured_piece") for move in moves if move.get("captured_piece")]
    player["totalCapturedPieces"] = len(captured_pieces)
    player["mostCapturedPiece"] = max(set(captured_pieces), key=captured_pieces.count, default=None)
    logger.debug("Player %s total captured pieces: %d, most captured piece: %s", player.get("username"), player["totalCapturedPieces"], player["mostCapturedPiece"])


def analyze_checks_and_checkmates(player):
    """Analyze checks and checkmates in the player's games."""
    moves = player.get("moves", [])
    player["totalChecks"] = sum(1 for move in moves if move.get("check", False))
    player["totalCheckmates"] = sum(1 for move in moves if move.get("checkmate", False))
    logger.debug("Player %s total checks: %d, total checkmates: %d", player.get("username"), player["totalChecks"], player["totalCheckmates"])


def analyze_piece_movement_patterns(player):
    """Analyze the movement patterns of the player's pieces."""
    moves = player.get("moves", [])
    piece_moves = {}
    for move in moves:
        piece = move.get("piece")
        if piece:
            piece_moves[piece] = piece_moves.get(piece, 0) + 1
    player["pieceMovementPatterns"] = piece_moves
    logger.debug("Player %s piece movement patterns: %s", player.get("username"), player["pieceMovementPatterns"])


def analyze_positional_preferences(player):
    """Analyze the player's positional preferences."""
    moves = player.get("moves", [])
    position_counts = {}
    for move in moves:
        to_square = move.get("to_square")
        if to_square:
            position_counts[to_square] = position_counts.get(to_square, 0) + 1
    player["positionalPreferences"] = {
        "mostCommonSquare": max(position_counts, key=position_counts.get, default=None),
        "squareFrequencies": position_counts
    }
    logger.debug("Player %s positional preferences: %s", player.get("username"), player["positionalPreferences"])


def analyze_opening_repertoire(player):
    """Analyze the player's opening repertoire."""
    moves = player.get("moves", [])
    openings = [move.get("opening") for move in moves if move.get("opening")]
    player["openingPreferences"] = {
        "mostCommonOpening": max(set(openings), key=openings.count, default=None),
        "openingFrequencies": {opening: openings.count(opening) for opening in set(openings)}
    }
    logger.debug("Player %s opening preferences: %s", player.get("username"), player["openingPreferences"])


def analyze_elo_performance(player):
    """Analyze Elo-based performance metrics."""
    moves = player.get("moves", [])
    opponent_elo_differences = [move.get("opponent_elo") - player.get("rating", 0) for move in moves if move.get("opponent_elo")]
    player["averageOpponentEloDifference"] = sum(opponent_elo_differences) / len(opponent_elo_differences) if opponent_elo_differences else 0
    logger.debug("Player %s average opponent Elo difference: %f", player.get("username"), player["averageOpponentEloDifference"])


def analyze_board_control(player):
    """Analyze positional heatmaps for board control."""
    moves = player.get("moves", [])
    board_control = {}
    for move in moves:
        to_square = move.get("to_square")
        if to_square:
            board_control[to_square] = board_control.get(to_square, 0) + 1
    player["boardControlHeatmap"] = board_control
    logger.debug("Player %s board control heatmap: %s", player.get("username"), player["boardControlHeatmap"])


def analyze_opponent_performance(player, players):
    """Analyze opponent-specific performance metrics."""
    opponents = [p for p in players if p != player]
    if opponents:
        opponent = opponents[0]  # Example: take first opponent in list
        player["performanceAgainstOpponent"] = {
            "win": player.get("result", "") == "win",
            "captures": player["totalCapturedPieces"],
            "checks": player["totalChecks"],
            "checkmates": player["totalCheckmates"]
        }
    logger.debug("Player %s performance against opponent: %s", player.get("username"), player.get("performanceAgainstOpponent"))


def analyze_game_history(player):
    """Analyze the game history of the player."""
    game_history = player.get("game_history", [])
    if game_history:
        last_game = game_history[-1]
        player["lastGameResult"] = last_game["result"]

        # Determine if last game was a close win/loss
        if last_game["result"] == "win" and last_game["score_diff"] <= 5:
            player["lastGameCloseWin"] = True
        else:
            player["lastGameCloseWin"] = False

        if last_game["result"] == "loss" and last_game["score_diff"] <= 5:
            player["lastGameCloseLoss"] = True
        else:
            player["lastGameCloseLoss"] = False

        # Count wins, losses, and ties in the last 5 games
        last_5_games = game_history[-5:]
        player["recentWinCount"] = sum(1 for game in last_5_games if game["result"] == "win")
        player["recentLossCount"] = sum(1 for game in last_5_games if game["result"] == "loss")
        player["recentTieCount"] = sum(1 for game in last_5_games if game["result"] == "tie")

        # Average score difference in the last 5 games
        player["recentAverageScoreDiff"] = sum(
            game["score_diff"] for game in last_5_games
        ) / len(last_5_games) if last_5_games else 0
    logger.debug("Player %s game history analysis: %s", player.get("username"), player)


def analyze_streaks(player):
    """Determine win/loss streaks from game history."""
    win_streak = 0
    loss_streak = 0
    current_streak = 0
    current_result = None

    game_history = player.get("game_history", [])
    for game in reversed(game_history):
        if current_result is None:
            current_result = game["result"]

        if game["result"] == current_result:
            current_streak += 1
            if game["result"] == "win":
                win_streak = max(win_streak, current_streak)
            elif game["result"] == "loss":
                loss_streak = max(loss_streak, current_streak)
        else:
            current_streak = 1
            current_result = game["result"]

    player["maxWinStreak"] = win_streak
    player["maxLossStreak"] = loss_streak
    logger.debug("Player %s win streak: %d, loss streak: %d", player.get("username"), win_streak, loss_streak)


def analyze_openings_in_game_history(player):
    """Analyze openings used in the player's game history."""
    game_history = player.get("game_history", [])
    openings = [game.get("opening") for game in game_history if game.get("opening")]
    player["mostCommonOpening"] = max(set(openings), key=openings.count, default=None) if openings else None
    player["openingDiversity"] = len(set(openings))
    logger.debug("Player %s most common opening: %s, opening diversity: %d", player.get("username"), player["mostCommonOpening"], player["openingDiversity"])


def analyze_behavioral_trends(player):
    """Analyze aggressive and defensive behavior in the player's recent games."""
    last_5_games = player.get("game_history", [])[-5:]
    player["aggressiveGames"] = sum(1 for game in last_5_games if game["score_diff"] > 5 and game["result"] == "win")
    player["defensiveGames"] = sum(1 for game in last_5_games if game["score_diff"] <= 5 and game["result"] == "win")
    logger.debug("Player %s aggressive and defensive games: %d, %d", player.get("username"), player["aggressiveGames"], player["defensiveGames"])


def analyze_total_time_spent(player):
    """Analyze the total time spent on moves by the player."""
    moves = player.get("moves", [])
    total_time = sum(move.get("time", 0) for move in moves)
    player["totalTimeSpent"] = total_time
    logger.debug("Player %s total time spent: %f seconds", player.get("username"), total_time)


def add_custom_player_stats(player):
    """Add custom player stats based on specific criteria."""
    player["isAggressive"] = player["aggressiveGames"] > 2
    player["isDefensive"] = player["defensiveGames"] > 2
    player["recentActivity"] = True if player["recentWinCount"] > 2 else False
    logger.debug("Player %s custom stats: %s", player.get("username"), player)
