from utils.logger import logger

def process_chess_data(game_data):
    """Process game data specific to chess."""
    players = game_data.get("players", [])
    logger.info("Processing data for %d players in chess.", len(players))

    for player in players:
        logger.info("Processing data for player: %s", player.get("username"))

        # Calculate win rate
        games_won = player.get("games_won", 0)
        games_played = player.get("games_played", 0)
        player["winRate"] = games_won / games_played if games_played > 0 else 0

        # Analyze moves
        moves = player.get("moves", [])
        player["totalMoves"] = len(moves)
        player["averageMoveTime"] = sum(move.get("time", 0) for move in moves) / len(moves) if moves else 0

        # Categorize moves by phase
        early_game_moves = [move for move in moves if move.get("move_number") <= 10]
        middle_game_moves = [move for move in moves if 11 <= move.get("move_number") <= 30]
        late_game_moves = [move for move in moves if move.get("move_number") > 30]
        player["earlyGameMoves"] = len(early_game_moves)
        player["middleGameMoves"] = len(middle_game_moves)
        player["lateGameMoves"] = len(late_game_moves)

        # Analyze captured pieces
        captured_pieces = [move.get("captured_piece") for move in moves if move.get("captured_piece")]
        player["totalCapturedPieces"] = len(captured_pieces)
        player["mostCapturedPiece"] = max(set(captured_pieces), key=captured_pieces.count, default=None)

        # Analyze checks and checkmates
        player["totalChecks"] = sum(1 for move in moves if move.get("check", False))
        player["totalCheckmates"] = sum(1 for move in moves if move.get("checkmate", False))

        # Advanced analysis: Piece movement patterns
        piece_moves = {}
        for move in moves:
            piece = move.get("piece")
            if piece:
                if piece not in piece_moves:
                    piece_moves[piece] = 0
                piece_moves[piece] += 1
        player["pieceMovementPatterns"] = piece_moves

        # Advanced analysis: Positional preferences
        position_counts = {}
        for move in moves:
            to_square = move.get("to_square")
            if to_square:
                position_counts[to_square] = position_counts.get(to_square, 0) + 1
        player["positionalPreferences"] = {
            "mostCommonSquare": max(position_counts, key=position_counts.get, default=None),
            "squareFrequencies": position_counts
        }

        # Advanced analysis: Opening repertoire
        openings = [move.get("opening") for move in moves if move.get("opening")]
        player["openingPreferences"] = {
            "mostCommonOpening": max(set(openings), key=openings.count, default=None),
            "openingFrequencies": {opening: openings.count(opening) for opening in set(openings)}
        }

        # Advanced analysis: Elo-based performance metrics
        opponent_elo_differences = [move.get("opponent_elo") - player.get("rating", 0) for move in moves if move.get("opponent_elo")]
        player["averageOpponentEloDifference"] = sum(opponent_elo_differences) / len(opponent_elo_differences) if opponent_elo_differences else 0

        # Advanced analysis: Positional heatmaps for board control
        board_control = {}
        for move in moves:
            to_square = move.get("to_square")
            if to_square:
                board_control[to_square] = board_control.get(to_square, 0) + 1
        player["boardControlHeatmap"] = board_control

        # Advanced analysis: Opponent-specific performance metrics
        opponents = [p for p in players if p != player]
        if opponents:
            opponent = opponents[0]
            player["performanceAgainstOpponent"] = {
                "win": player.get("result", "") == "win",
                "captures": player["totalCapturedPieces"],
                "checks": player["totalChecks"],
                "checkmates": player["totalCheckmates"]
            }

        # Analyze game history
        game_history = player.get("game_history", [])

        if game_history:
            # Check result of the last game
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

        # Determine streaks from game history
        win_streak = 0
        loss_streak = 0
        current_streak = 0
        current_result = None

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

        # Analyze openings in game history
        openings = [game.get("opening") for game in game_history if game.get("opening")]
        player["mostCommonOpening"] = max(set(openings), key=openings.count, default=None) if openings else None
        player["openingDiversity"] = len(set(openings))

        # Behavioral analysis based on game history
        player["aggressiveGames"] = sum(1 for game in last_5_games if game["score_diff"] > 5 and game["result"] == "win")
        player["defensiveGames"] = sum(1 for game in last_5_games if game["score_diff"] <= 5 and game["result"] == "win")

        logger.debug("Calculated advanced stats for player %s: %s", player.get("username"), player)

    logger.info("Finished processing chess data.")
    return players
