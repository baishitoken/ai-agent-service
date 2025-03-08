from utils.logger import logger

def process_8ball_data(game_data):
    """Process game data specific to 8-ball pool."""
    players = game_data.get("players", [])
    logger.info("Processing data for %d players in 8-ball.", len(players))

    for player in players:
        logger.info("Processing data for player: %s", player.get("username"))

        # Calculate "firstTurn"
        player["firstTurn"] = player["game_data"][0]["timestamp"] == min(
            p["game_data"][0]["timestamp"] for p in players
        )

        # Calculate win rate
        games_won = player.get("games_won", 0)
        games = player.get("games", 0)
        player["winRate"] = games_won / games if games > 0 else 0

        # Calculate ball potting accuracy
        total_shots = len(player.get("game_data", []))
        total_potted = sum(len(turn.get("balls_potted", [])) for turn in player.get("game_data", []))
        player["pottingAccuracy"] = total_potted / total_shots if total_shots > 0 else 0

        # Update stats with current game data
        player["games"] += 1
        player["games_won"] += 1 if player.get("result", "") == "win" else 0
        player["games_lost"] += 1 if player.get("result", "") == "loss" else 0
        player["balls_potted"] += total_potted

        # Calculate fouls per game
        player["averageFouls"] = player.get("fouls", 0) / games if games > 0 else 0

        # Calculate aggressive vs defensive shots
        aggressive_shots = sum(1 for turn in player.get("game_data", []) if len(turn.get("balls_potted", [])) > 0)
        defensive_shots = total_shots - aggressive_shots
        player["aggressiveShotRatio"] = aggressive_shots / total_shots if total_shots > 0 else 0
        player["defensiveShotRatio"] = defensive_shots / total_shots if total_shots > 0 else 0

        # Determine most common ball hit
        ball_hit_counts = {}
        for turn in player.get("game_data", []):
            ball_hit = turn.get("ball_hit")
            if ball_hit is not None:
                ball_hit_counts[ball_hit] = ball_hit_counts.get(ball_hit, 0) + 1
        player["mostCommonBallHit"] = max(ball_hit_counts, key=ball_hit_counts.get, default=None)

        # Analyze wall hits
        total_wall_hits = sum(len(turn.get("walls_hit", [])) for turn in player.get("game_data", []))
        player["averageWallHits"] = total_wall_hits / total_shots if total_shots > 0 else 0

        # Identify streaks of successful pots
        max_potting_streak = 0
        current_streak = 0
        for turn in player.get("game_data", []):
            if len(turn.get("balls_potted", [])) > 0:
                current_streak += 1
                max_potting_streak = max(max_potting_streak, current_streak)
            else:
                current_streak = 0
        player["maxPottingStreak"] = max_potting_streak

        # Advanced analysis: Positional heatmaps for cue ball positions
        cue_positions = [turn.get("cue_ball_position", [0, 0]) for turn in player.get("game_data", [])]
        x_positions = [pos[0] for pos in cue_positions]
        y_positions = [pos[1] for pos in cue_positions]
        player["averageCuePosition"] = {
            "x": sum(x_positions) / len(x_positions) if x_positions else 0,
            "y": sum(y_positions) / len(y_positions) if y_positions else 0
        }

        # Advanced analysis: Game phase analysis
        mid_game_index = total_shots // 2
        early_game_pots = sum(len(player["game_data"][i].get("balls_potted", [])) for i in range(mid_game_index))
        late_game_pots = total_potted - early_game_pots
        player["earlyGamePots"] = early_game_pots
        player["lateGamePots"] = late_game_pots

        # Advanced analysis: Opponent-specific performance metrics
        opponents = [p for p in players if p != player]
        if opponents:
            opponent = opponents[0]
            player["performanceAgainstOpponent"] = {
                "ballsPotted": total_potted,
                "fouls": player.get("fouls", 0),
                "win": player.get("result", "") == "win"
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

        # Analyze behavior trends
        player["recentAggressiveBehavior"] = sum(
            1 for game in last_5_games if game["score_diff"] > 10 and game["result"] == "win"
        )
        player["recentDefensiveBehavior"] = sum(
            1 for game in last_5_games if game["score_diff"] < 5 and game["result"] == "win"
        )

        logger.debug("Calculated advanced stats for player %s: %s", player.get("username"), player)

    logger.info("Finished processing 8-ball data.")
    return players
