from utils.logger import logger
import random

class EightBallRLAgent:
    """
    RL agent.
    Uses Q-learning to refine AI bot behavior.
    """
    def __init__(self):
        self.q_table = {}
        self.learning_rate = 0.1
        self.discount_factor = 0.99
        self.exploration_rate = 0.1
        self.actions = ["aggressive_shot", "defensive_shot", "bank_shot", "combo_shot", "safety"]
        self.memory = []

    def get_state(self, player):
        """
        Get the state representation for the player.
        """
        return (
            round(player.get("winRate", 0), 2),
            round(player.get("pottingAccuracy", 0), 2),
            round(player.get("averageFouls", 0), 2),
        )

    def choose_action(self, state):
        """
        Epsilon-greedy policy for choosing an action based on Q-values.
        """
        if random.random() < self.exploration_rate:
            return random.choice(self.actions)
        else:
            return self.get_best_action(state)

    def get_best_action(self, state):
        """
        Returns the action with the highest Q-value for the given state.
        """
        if state not in self.q_table:
            self.q_table[state] = {a: 0.0 for a in self.actions}
        best_act = max(self.q_table[state], key=self.q_table[state].get)
        return best_act

    def observe(self, state, action, reward, next_state):
        """
        Store experience in memory for batch or incremental updates.
        """
        self.memory.append((state, action, reward, next_state))

    def update_q_value(self, state, action, reward, next_state):
        """
        Update Q-table using the Bellman equation for Q-learning.
        """
        if state not in self.q_table:
            self.q_table[state] = {a: 0.0 for a in self.actions}
        if next_state not in self.q_table:
            self.q_table[next_state] = {a: 0.0 for a in self.actions}

        current_q = self.q_table[state][action]
        max_next_q = max(self.q_table[next_state].values())
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_next_q - current_q)
        self.q_table[state][action] = new_q

    def train(self):
        """
        Train the agent on all stored experiences (simple approach).
        """
        for (state, action, reward, next_state) in self.memory:
            self.update_q_value(state, action, reward, next_state)
        self.memory = []

eight_ball_rl_agent = EightBallRLAgent()


def process_8ball_data(game_data):
    """Process game data specific to 8-ball pool."""
    players = game_data.get("players", [])
    logger.info("Processing data for %d players in 8-ball.", len(players))

    if not players:
        logger.warning("No players data found.")

    for player in players:
        logger.info("Processing data for player: %s", player.get("username"))

        # Standard analysis
        determine_first_turn(player, players)
        calculate_win_rate(player)
        calculate_potting_accuracy(player)
        update_game_data(player)
        calculate_average_fouls(player)
        calculate_shot_ratios(player)
        determine_most_common_ball_hit(player)
        analyze_wall_hits(player)
        identify_max_potting_streak(player)
        analyze_cue_ball_position(player)
        analyze_game_phases(player)
        analyze_opponent_performance(player, players)
        analyze_game_history(player)
        analyze_streaks(player)
        analyze_behavior_trends(player)
        analyze_shot_accuracy_trends(player)
        add_custom_player_stats(player)

        refine_ai_bot(player)

        logger.debug("Calculated advanced stats for player %s: %s", player.get("username"), player)

    logger.info("Finished processing 8-ball data.")
    return players

def refine_ai_bot(player):
    """
    A reinforcement learning function that refines an AI bot's 8-ball gameplay
    by analyzing the player's past matches. The bot should improve shot selection
    and decision-making over time.
    """
    current_state = eight_ball_rl_agent.get_state(player)

    chosen_action = eight_ball_rl_agent.choose_action(current_state)

    result = player.get("result", "")
    if result == "win":
        reward = 1.0
    elif result == "loss":
        reward = -0.5
    else:
        reward = 0.0

    next_state = current_state

    eight_ball_rl_agent.observe(current_state, chosen_action, reward, next_state)

    eight_ball_rl_agent.train()

    player["aiChosenAction"] = chosen_action
    logger.debug(
        "AI refined for player %s: state=%s, action=%s, reward=%.2f",
        player.get("username"), current_state, chosen_action, reward
    )

def determine_first_turn(player, players):
    """Determine if the player took the first turn in the game."""
    player["firstTurn"] = player["game_data"][0]["timestamp"] == min(
        p["game_data"][0]["timestamp"] for p in players
    )
    logger.debug("Player %s first turn: %s", player.get("username"), player["firstTurn"])


def calculate_win_rate(player):
    """Calculate win rate for the player."""
    games_won = player.get("games_won", 0)
    games = player.get("games", 0)
    player["winRate"] = games_won / games if games > 0 else 0
    logger.debug("Player %s win rate: %f", player.get("username"), player["winRate"])


def calculate_potting_accuracy(player):
    """Calculate potting accuracy for the player."""
    total_shots = len(player.get("game_data", []))
    total_potted = sum(len(turn.get("balls_potted", [])) for turn in player.get("game_data", []))
    player["pottingAccuracy"] = total_potted / total_shots if total_shots > 0 else 0
    logger.debug("Player %s potting accuracy: %f", player.get("username"), player["pottingAccuracy"])


def update_game_data(player):
    """Update the player's game data with the current game's results."""
    player["games"] += 1
    player["games_won"] += 1 if player.get("result", "") == "win" else 0
    player["games_lost"] += 1 if player.get("result", "") == "loss" else 0
    total_potted = sum(len(turn.get("balls_potted", [])) for turn in player.get("game_data", []))
    player["balls_potted"] += total_potted
    logger.debug("Player %s updated game data: games %d, wins %d, losses %d, balls potted %d", 
                 player.get("username"), player["games"], player["games_won"], player["games_lost"], player["balls_potted"])


def calculate_average_fouls(player):
    """Calculate average fouls per game for the player."""
    fouls = player.get("fouls", 0)
    games = player.get("games", 0)
    player["averageFouls"] = fouls / games if games > 0 else 0
    logger.debug("Player %s average fouls per game: %f", player.get("username"), player["averageFouls"])


def calculate_shot_ratios(player):
    """Calculate aggressive vs defensive shots."""
    aggressive_shots = sum(1 for turn in player.get("game_data", []) if len(turn.get("balls_potted", [])) > 0)
    total_shots = len(player.get("game_data", []))
    defensive_shots = total_shots - aggressive_shots
    player["aggressiveShotRatio"] = aggressive_shots / total_shots if total_shots > 0 else 0
    player["defensiveShotRatio"] = defensive_shots / total_shots if total_shots > 0 else 0
    logger.debug("Player %s aggressive shots: %f, defensive shots: %f", player.get("username"), player["aggressiveShotRatio"], player["defensiveShotRatio"])


def determine_most_common_ball_hit(player):
    """Determine the most common ball hit by the player."""
    ball_hit_counts = {}
    for turn in player.get("game_data", []):
        ball_hit = turn.get("ball_hit")
        if ball_hit is not None:
            ball_hit_counts[ball_hit] = ball_hit_counts.get(ball_hit, 0) + 1
    player["mostCommonBallHit"] = max(ball_hit_counts, key=ball_hit_counts.get, default=None)
    logger.debug("Player %s most common ball hit: %s", player.get("username"), player["mostCommonBallHit"])


def analyze_wall_hits(player):
    """Analyze wall hits by the player."""
    total_wall_hits = sum(len(turn.get("walls_hit", [])) for turn in player.get("game_data", []))
    total_shots = len(player.get("game_data", []))
    player["averageWallHits"] = total_wall_hits / total_shots if total_shots > 0 else 0
    logger.debug("Player %s average wall hits: %f", player.get("username"), player["averageWallHits"])


def identify_max_potting_streak(player):
    """Identify the longest streak of successful pots."""
    max_potting_streak = 0
    current_streak = 0
    for turn in player.get("game_data", []):
        if len(turn.get("balls_potted", [])) > 0:
            current_streak += 1
            max_potting_streak = max(max_potting_streak, current_streak)
        else:
            current_streak = 0
    player["maxPottingStreak"] = max_potting_streak
    logger.debug("Player %s max potting streak: %d", player.get("username"), player["maxPottingStreak"])


def analyze_cue_ball_position(player):
    """Analyze the cue ball positions during the game."""
    cue_positions = [turn.get("cue_ball_position", [0, 0]) for turn in player.get("game_data", [])]
    x_positions = [pos[0] for pos in cue_positions]
    y_positions = [pos[1] for pos in cue_positions]
    player["averageCuePosition"] = {
        "x": sum(x_positions) / len(x_positions) if x_positions else 0,
        "y": sum(y_positions) / len(y_positions) if y_positions else 0
    }
    logger.debug("Player %s average cue ball position: %s", player.get("username"), player["averageCuePosition"])


def analyze_game_phases(player):
    """Analyze game phases (early vs late) for the player."""
    total_shots = len(player.get("game_data", []))
    mid_game_index = total_shots // 2
    early_game_pots = sum(len(player["game_data"][i].get("balls_potted", [])) for i in range(mid_game_index))
    total_potted = sum(len(turn.get("balls_potted", [])) for turn in player.get("game_data", []))
    late_game_pots = total_potted - early_game_pots
    player["earlyGamePots"] = early_game_pots
    player["lateGamePots"] = late_game_pots
    logger.debug("Player %s early and late game pots: %d, %d", player.get("username"), player["earlyGamePots"], player["lateGamePots"])


def analyze_opponent_performance(player, players):
    """Analyze performance against opponents."""
    opponents = [p for p in players if p != player]
    if opponents:
        opponent = opponents[0]
        player["performanceAgainstOpponent"] = {
            "ballsPotted": sum(len(turn.get("balls_potted", [])) for turn in player.get("game_data", [])),
            "fouls": player.get("fouls", 0),
            "win": player.get("result", "") == "win"
        }
    logger.debug("Player %s performance against opponent: %s", player.get("username"), player.get("performanceAgainstOpponent"))


def analyze_game_history(player):
    """Analyze the game history for the player."""
    game_history = player.get("game_history", [])
    if game_history:
        last_game = game_history[-1]
        player["lastGameResult"] = last_game["result"]

        if last_game["result"] == "win" and last_game["score_diff"] <= 5:
            player["lastGameCloseWin"] = True
        else:
            player["lastGameCloseWin"] = False

        if last_game["result"] == "loss" and last_game["score_diff"] <= 5:
            player["lastGameCloseLoss"] = True
        else:
            player["lastGameCloseLoss"] = False

        last_5_games = game_history[-5:]
        player["recentWinCount"] = sum(1 for game in last_5_games if game["result"] == "win")
        player["recentLossCount"] = sum(1 for game in last_5_games if game["result"] == "loss")
        player["recentTieCount"] = sum(1 for game in last_5_games if game["result"] == "tie")
        player["recentAverageScoreDiff"] = sum(game["score_diff"] for game in last_5_games) / len(last_5_games) if last_5_games else 0
    logger.debug("Player %s game history analysis: %s", player.get("username"), player)


def analyze_streaks(player):
    """Analyze win/loss streaks from game history."""
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


def analyze_behavior_trends(player):
    """Analyze aggressive and defensive behavior trends."""
    last_5_games = player.get("game_history", [])[-5:]
    player["recentAggressiveBehavior"] = sum(1 for game in last_5_games if game["score_diff"] > 10 and game["result"] == "win")
    player["recentDefensiveBehavior"] = sum(1 for game in last_5_games if game["score_diff"] < 5 and game["result"] == "win")
    logger.debug("Player %s recent aggressive and defensive behavior: %d, %d", player.get("username"), player["recentAggressiveBehavior"], player["recentDefensiveBehavior"])


def analyze_shot_accuracy_trends(player):
    """Analyze trends in shot accuracy over time."""
    game_data = player.get("game_data", [])
    shot_accuracy = [len(turn.get("balls_potted", [])) / len(turn.get("shot_attempts", [])) if turn.get("shot_attempts") else 0 for turn in game_data]
    player["shotAccuracyTrend"] = shot_accuracy
    logger.debug("Player %s shot accuracy trends: %s", player.get("username"), player["shotAccuracyTrend"])


def add_custom_player_stats(player):
    """Add custom player stats based on specific behavior."""
    player["isAggressive"] = player["recentAggressiveBehavior"] > 2
    player["isDefensive"] = player["recentDefensiveBehavior"] > 2
    player["recentActivity"] = True if player["recentWinCount"] > 2 else False
    logger.debug("Player %s custom stats: %s", player.get("username"), player)