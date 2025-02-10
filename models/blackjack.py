from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class BlackjackMove(BaseModel):
    action: str
    card_received: Optional[str]
    hand_value: int
    timestamp: int
    is_blackjack: Optional[bool] = False  # Is this move a Blackjack?
    is_bust: Optional[bool] = False       # Is this move a bust?
    bet_amount: Optional[float] = 0.0     # Bet amount for the move
    move_duration: Optional[int] = 0      # Duration of the move in seconds

class BlackjackGameHistory(BaseModel):
    result: str
    final_hand_value: int
    dealer_hand_value: int
    bet_amount: float
    timestamp: int
    score_difference: Optional[int] = None  # Difference in points
    is_final_round: Optional[bool] = False  # Is this the last round of the game?
    duration: Optional[int] = 0             # Duration of the game in seconds
    hand_history: Optional[List[BlackjackMove]] = []  # History of moves in the game

class PlayerStatistics(BaseModel):
    total_bets: float
    total_wins: int
    total_losses: int
    total_pushes: int
    total_blackjacks: int
    total_busts: int
    total_hands_played: int
    win_rate: float
    average_bet_size: float
    highest_bet: float
    lowest_bet: float
    total_payouts: float
    average_hand_value: float
    max_win_streak: int
    max_loss_streak: int
    average_bet_duration: float
    player_rank: Optional[int] = None  # Optional rank of the player in the overall leaderboard

class BlackjackPlayerData(BaseModel):
    username: str
    games_played: int
    games_won: int
    games_lost: int
    games_push: int
    moves: List[BlackjackMove]
    game_history: List[BlackjackGameHistory]
    player_statistics: PlayerStatistics  # Nested stats for the player
    last_game_timestamp: Optional[int] = None  # Timestamp of the last game played
    total_money_earned: float = 0.0  # Total money earned by the player
    total_bet_amount: float = 0.0    # Total bet amount across all games
    total_blackjack_count: int = 0   # Total number of blackjacks in history
    total_bust_count: int = 0        # Total number of busts in history
    average_hand_value_overall: float = 0.0  # Overall average hand value across all games
    hands_in_pushes: int = 0         # Number of hands that ended in a push
    last_move: Optional[BlackjackMove] = None  # Last recorded move
    total_strategies_used: Dict[str, int] = {}  # Key: strategy name, Value: times used
    favorite_card: Optional[str] = None  # Most frequently received card
    blackjack_frequency: float = 0.0  # Frequency of blackjacks per game played
    bust_rate: float = 0.0  # Percentage of games ending in a bust

class BlackjackGameData(BaseModel):
    players: List[BlackjackPlayerData]
    dealer: BlackjackPlayerData  # Dealer's data
    game_duration: Optional[int] = 0  # Total duration of the game in seconds
    game_start_time: int  # Start timestamp for the game
    game_end_time: Optional[int] = None  # End timestamp for the game
    total_bets_placed: float = 0.0  # Total amount of bets placed by all players
    total_wins: int = 0  # Total wins across all players
    total_losses: int = 0  # Total losses across all players
    total_pushes: int = 0  # Total pushes across all players
    dealer_hand_value: Optional[int] = None  # Dealer's final hand value
    dealer_wins: int = 0  # Number of games the dealer won
    player_avg_hand_value: float = 0.0  # Average hand value across all players
    most_common_final_result: Optional[str] = None  # Most common result for the game ("win", "loss", "push")
    game_ended_in_blackjack: bool = False  # Did the game end in a blackjack?
    dealer_blackjack: bool = False  # Did the dealer get a blackjack?
    strategies_used_in_game: Dict[str, int] = {}  # Strategies used by players during the game
    game_history: List[BlackjackGameHistory] = []  # History of all games played in this session
    game_metadata: Dict[str, str] = {}  # Additional metadata (e.g., version, environment)

class GameEvent(BaseModel):
    event_type: str
    event_details: Dict[str, str]
    timestamp: int

class BlackjackEventLog(BaseModel):
    events: List[GameEvent]
    total_events: int
    last_event_timestamp: int

class BlackjackSession(BaseModel):
    session_id: str  # Unique session ID
    game_data: List[BlackjackGameData]  # List of all games in this session
    event_log: BlackjackEventLog  # Event log for the session
    session_start_time: int  # Session start timestamp
    session_end_time: Optional[int] = None  # Session end timestamp
    total_duration: Optional[int] = 0  # Duration of the session in seconds
    total_games_played: int = 0  # Total number of games played in the session
    total_players: int = 0  # Total number of players in the session
    total_wins: int = 0  # Total wins in the session
    total_losses: int = 0  # Total losses in the session
    total_pushes: int = 0  # Total pushes in the session
    average_bet_size: float = 0.0  # Average bet size for the session
    average_game_duration: float = 0.0  # Average duration of a game in the session
    most_common_move: Optional[str] = None  # Most common move made across all games
    session_metadata: Dict[str, str] = {}  # Additional metadata (e.g., player behavior analytics)

class BlackjackDatabase(BaseModel):
    sessions: List[BlackjackSession]  # List of all sessions in the database
    total_sessions: int = 0  # Total number of sessions
    total_players: int = 0  # Total number of players across all sessions
    total_games_played: int = 0  # Total number of games across all sessions
    total_blackjacks: int = 0  # Total number of blackjacks
    total_busts: int = 0  # Total number of busts
    total_wins: int = 0  # Total wins across all sessions
    total_losses: int = 0  # Total losses across all sessions
    total_pushes: int = 0  # Total pushes across all sessions
    overall_player_stats: Dict[str, PlayerStatistics] = {}  # Key: player username, value: player statistics
    global_metadata: Dict[str, str] = {}  # Global metadata (e.g., game version, server info)
