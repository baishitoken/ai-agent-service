from utils.logger import logger
from datetime import datetime

def process_blackjack_data(game_data):
    """Process game data specific to blackjack."""
    players = game_data.get("players", [])
    logger.info("Processing data for %d players in blackjack.", len(players))

    if not players:
        logger.warning("No players data found.")
    
    for player in players:
        logger.info("Processing data for player: %s", player.get("username"))

        # Calculate win rate
        calculate_win_rate(player)

        # Total hands played
        calculate_total_hands_played(player)

        # Total bets and average bet size
        calculate_total_bet_and_average_bet(player)

        # Blackjack occurrences and bust rate
        calculate_blackjack_and_bust_rate(player)

        # Game history analysis
        analyze_game_history(player)

        # Streak analysis
        analyze_win_loss_streak(player)

        # Advanced strategy analysis
        analyze_advanced_strategies(player)

        # Additional Metrics
        calculate_bet_variance(player)
        calculate_average_hand_value(player)

        # Add custom player stats (e.g., recent trends)
        add_custom_player_stats(player)

        # Additional analyses
        calculate_average_bet_size(player)
        calculate_bet_ratio(player)
        calculate_hand_win_rate(player)
        track_recent_trends(player)
        calculate_hand_valuation(player)
        detect_trend_in_betting(player)
        assess_risk_level(player)
        track_blackjack_frequency(player)
        analyze_recent_blackjack_trends(player)
        generate_game_summary(player)

        logger.debug("Calculated advanced stats for player %s: %s", player.get("username"), player)
    
    logger.info("Finished processing blackjack data.")
    return players



def calculate_win_rate(player):
    """Calculate win rate for the player."""
    games_won = player.get("games_won", 0)
    games_played = player.get("games_played", 0)
    if games_played > 0:
        player["winRate"] = games_won / games_played
    else:
        player["winRate"] = 0
    logger.debug("Player %s win rate: %f", player.get("username"), player["winRate"])


def calculate_total_hands_played(player):
    """Calculate the total number of hands played by the player."""
    hands = player.get("hands", [])
    player["totalHandsPlayed"] = len(hands)
    logger.debug("Player %s total hands played: %d", player.get("username"), player["totalHandsPlayed"])


def calculate_total_bet_and_average_bet(player):
    """Calculate total bet and average bet size for the player."""
    hands = player.get("hands", [])
    total_bet = sum(hand.get("bet", 0) for hand in hands)
    player["totalBetAmount"] = total_bet
    player["averageBet"] = total_bet / len(hands) if hands else 0
    logger.debug("Player %s total bet: %f, average bet: %f", player.get("username"), player["totalBetAmount"], player["averageBet"])


def calculate_blackjack_and_bust_rate(player):
    """Calculate the number of blackjacks and bust rate for the player."""
    hands = player.get("hands", [])
    blackjacks = sum(1 for hand in hands if hand.get("blackjack", False))
    busts = sum(1 for hand in hands if hand.get("bust", False))
    player["blackjackCount"] = blackjacks
    player["bustRate"] = busts / len(hands) if hands else 0
    logger.debug("Player %s blackjacks: %d, bust rate: %f", player.get("username"), player["blackjackCount"], player["bustRate"])


def analyze_game_history(player):
    """Analyze the player's game history."""
    game_history = player.get("game_history", [])
    if game_history:
        last_game = game_history[-1]
        player["lastGameResult"] = last_game["result"]

        # Count wins, losses, and ties in the last 5 games
        last_5_games = game_history[-5:]
        player["recentWinCount"] = sum(1 for game in last_5_games if game["result"] == "win")
        player["recentLossCount"] = sum(1 for game in last_5_games if game["result"] == "loss")
        player["recentTieCount"] = sum(1 for game in last_5_games if game["result"] == "tie")

        logger.debug("Player %s recent game analysis: %s", player.get("username"), player)


def analyze_win_loss_streak(player):
    """Analyze the player's win and loss streaks."""
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


def analyze_advanced_strategies(player):
    """Analyze advanced strategies used by the player (doubling down, splitting)."""
    hands = player.get("hands", [])
    total_doubles = sum(1 for hand in hands if hand.get("double_down", False))
    total_splits = sum(1 for hand in hands if hand.get("split", False))
    player["doubleDownCount"] = total_doubles
    player["splitCount"] = total_splits
    logger.debug("Player %s double downs: %d, splits: %d", player.get("username"), total_doubles, total_splits)


def calculate_bet_variance(player):
    """Calculate the variance of the player's bets."""
    hands = player.get("hands", [])
    if len(hands) < 2:
        player["betVariance"] = 0
        return

    bets = [hand.get("bet", 0) for hand in hands]
    mean_bet = sum(bets) / len(bets)
    variance = sum((bet - mean_bet) ** 2 for bet in bets) / len(bets)
    player["betVariance"] = variance
    logger.debug("Player %s bet variance: %f", player.get("username"), player["betVariance"])


def calculate_average_hand_value(player):
    """Calculate the average hand value for the player."""
    hands = player.get("hands", [])
    total_value = sum(hand.get("value", 0) for hand in hands)
    player["averageHandValue"] = total_value / len(hands) if hands else 0
    logger.debug("Player %s average hand value: %f", player.get("username"), player["averageHandValue"])


def add_custom_player_stats(player):
    """Add custom stats to the player based on specific requirements."""
    player["isHighRoller"] = player["averageBet"] > 100
    player["recentActivityDate"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug("Player %s custom stats: %s", player.get("username"), player)


def validate_game_data(game_data):
    """Validate the integrity of the game data."""
    if not isinstance(game_data, dict):
        logger.error("Invalid game data format: Expected dictionary.")
        return False
    if "players" not in game_data:
        logger.error("Missing 'players' key in game data.")
        return False
    return True

def calculate_average_bet_size(player):
    """Calculate the average bet size for the player across all hands."""
    hands = player.get("hands", [])
    total_bet = sum(hand.get("bet", 0) for hand in hands)
    player["averageBetSize"] = total_bet / len(hands) if hands else 0
    logger.debug("Player %s average bet size: %f", player.get("username"), player["averageBetSize"])


def calculate_bet_ratio(player):
    """Calculate the ratio of total bet to total hands played."""
    total_bet = player.get("totalBetAmount", 0)
    total_hands = player.get("totalHandsPlayed", 0)
    player["betRatio"] = total_bet / total_hands if total_hands > 0 else 0
    logger.debug("Player %s bet ratio: %f", player.get("username"), player["betRatio"])


def calculate_hand_win_rate(player):
    """Calculate the win rate based on hands played."""
    hands = player.get("hands", [])
    total_wins = sum(1 for hand in hands if hand.get("win", False))
    player["handWinRate"] = total_wins / len(hands) if hands else 0
    logger.debug("Player %s hand win rate: %f", player.get("username"), player["handWinRate"])


def track_recent_trends(player):
    """Track the recent trends in the player's game results (win/loss ratio)."""
    game_history = player.get("game_history", [])
    if len(game_history) < 10:
        player["recentTrend"] = "Not enough games"
        return

    last_10_games = game_history[-10:]
    win_count = sum(1 for game in last_10_games if game["result"] == "win")
    loss_count = sum(1 for game in last_10_games if game["result"] == "loss")
    player["recentTrend"] = "Wins: %d, Losses: %d" % (win_count, loss_count)
    logger.debug("Player %s recent trends: %s", player.get("username"), player["recentTrend"])


def calculate_hand_valuation(player):
    """Calculate the hand valuation based on the cards and result."""
    hands = player.get("hands", [])
    hand_values = [sum(hand.get("card_values", [])) for hand in hands]
    player["averageHandValuation"] = sum(hand_values) / len(hand_values) if hands else 0
    logger.debug("Player %s average hand valuation: %f", player.get("username"), player["averageHandValuation"])


def detect_trend_in_betting(player):
    """Detect any significant trend in the player's betting pattern."""
    hands = player.get("hands", [])
    if len(hands) < 5:
        player["bettingTrend"] = "Insufficient data"
        return

    bets = [hand.get("bet", 0) for hand in hands]
    bet_changes = [bets[i] - bets[i - 1] for i in range(1, len(bets))]
    player["bettingTrend"] = "Increasing" if all(change > 0 for change in bet_changes) else "Decreasing"
    logger.debug("Player %s betting trend: %s", player.get("username"), player["bettingTrend"])


def assess_risk_level(player):
    """Assess the risk level based on betting size and win rate."""
    win_rate = player.get("winRate", 0)
    average_bet = player.get("averageBet", 0)
    if win_rate > 0.6 and average_bet > 50:
        player["riskLevel"] = "High"
    elif win_rate > 0.4 and average_bet > 20:
        player["riskLevel"] = "Medium"
    else:
        player["riskLevel"] = "Low"
    logger.debug("Player %s risk level: %s", player.get("username"), player["riskLevel"])


def track_blackjack_frequency(player):
    """Track how often the player gets a blackjack."""
    hands = player.get("hands", [])
    blackjacks = sum(1 for hand in hands if hand.get("blackjack", False))
    player["blackjackFrequency"] = blackjacks / len(hands) if hands else 0
    logger.debug("Player %s blackjack frequency: %f", player.get("username"), player["blackjackFrequency"])


def analyze_recent_blackjack_trends(player):
    """Analyze trends in the player's blackjack results."""
    hands = player.get("hands", [])
    blackjack_count = sum(1 for hand in hands if hand.get("blackjack", False))
    player["recentBlackjackTrend"] = "Frequent" if blackjack_count > len(hands) * 0.3 else "Infrequent"
    logger.debug("Player %s recent blackjack trend: %s", player.get("username"), player["recentBlackjackTrend"])


def generate_game_summary(player):
    """Generate a summary of the player's overall performance."""
    games_played = player.get("games_played", 0)
    games_won = player.get("games_won", 0)
    player["performanceSummary"] = {
        "Total Games Played": games_played,
        "Total Wins": games_won,
        "Win Rate": player.get("winRate", 0),
        "Average Bet": player.get("averageBet", 0),
        "Recent Trend": player.get("recentTrend", ""),
        "Max Win Streak": player.get("maxWinStreak", 0),
        "Max Loss Streak": player.get("maxLossStreak", 0)
    }
    logger.debug("Player %s performance summary: %s", player.get("username"), player["performanceSummary"])


def log_player_data(player):
    """Log detailed information for a player."""
    logger.info("Player details: %s", player)