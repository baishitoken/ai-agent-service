from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class TurnData(BaseModel):
    timestamp: int
    cue_ball_position: List[int] = Field(..., min_items=2, max_items=2)
    power: float
    angle: float
    ball_hit: Optional[int]
    balls_collided: List[int]
    balls_potted: List[int]
    walls_hit: List[int]
    shot_type: Optional[str] = None  # Type of shot (e.g., break shot, bank shot)
    spin: Optional[str] = None  # Spin applied on the cue ball (e.g., top, bottom, left, right)
    shot_duration: Optional[float] = 0.0  # Duration of the shot in seconds
    is_foul: Optional[bool] = False  # Whether the shot was a foul or not
    power_rating: Optional[float] = 0.0  # Power of the shot, for player assessment
    angle_of_incidence: Optional[float] = None  # The angle at which the cue ball hits the object ball

class GameHistory(BaseModel):
    result: str  # win, loss, or draw
    opponent: str
    score_diff: int  # Difference in score
    timestamp: int  # Timestamp of the game
    total_shots: int  # Total shots taken during the game
    average_shot_duration: Optional[float] = 0.0  # Average shot time in the game
    game_duration: Optional[int] = 0  # Duration of the game in seconds
    game_event: Optional[str] = None  # Additional event related to the game (e.g., tournament)
    game_mode: Optional[str] = None  # Mode of the game (e.g., Practice, Tournament)
    is_break_shot: Optional[bool] = False  # Did the game start with a break shot?
    total_balls_potted: Optional[int] = 0  # Total balls potted in the game
    foul_count: Optional[int] = 0  # Number of fouls committed during the game

class PlayerStatistics(BaseModel):
    total_balls_potted: int
    total_games_played: int
    total_wins: int
    total_losses: int
    total_fouls: int
    total_eightballs_potted: int
    average_balls_potted_per_game: float
    total_shots_taken: int
    total_walls_hit: int
    total_shots_missed: int
    highest_score: int  # Highest score achieved in a game
    average_game_duration: float  # Average game duration
    total_fouls_committed: int  # Total fouls committed across all games
    average_shot_power: float  # Average shot power across all games
    shot_accuracy: float  # Percentage of successful shots
    longest_streak_of_balls_potted: int  # Longest streak of successful pots
    win_percentage: float  # Percentage of games won
    total_break_shots: int  # Number of successful break shots
    longest_game_duration: int  # Duration of the longest game played
    shot_types_used: Dict[str, int] = {}  # Dictionary of shot types and how often each was used
    favorite_ball: Optional[int] = None  # Most frequently potted ball
    current_rating: Optional[int] = Field(default=0, ge=0)  # Current player rating

class PlayerData(BaseModel):
    username: str
    rating: Optional[int] = Field(default=0, ge=0)
    games: int = Field(..., ge=0)
    games_won: int = Field(..., ge=0)
    games_lost: int = Field(..., ge=0)
    balls_potted: int = Field(..., ge=0)
    fouls: int = Field(..., ge=0)
    eightballs_potted: Optional[int] = Field(default=0, ge=0)
    favourite: Optional[str]
    game_data: List[TurnData]
    game_history: List[GameHistory] = []
    player_statistics: PlayerStatistics  # Nested player statistics
    last_game_timestamp: Optional[int] = None  # Timestamp of the last game played
    total_money_earned: float = 0.0  # Total earnings from winnings in the game
    total_bet_amount: float = 0.0  # Total amount of bets placed
    total_fouls_committed: int = 0  # Total fouls across all games
    total_break_shots: int = 0  # Total number of break shots performed
    total_walls_hit: int = 0  # Total number of times the walls were hit
    favorite_shot_type: Optional[str] = None  # Most commonly used shot type
    total_missed_shots: int = 0  # Total missed shots
    last_move: Optional[TurnData] = None  # Last move made by the player
    most_successful_shot_type: Optional[str] = None  # Most successful shot type (e.g., long pot, cross-corner pot)

class Game8BallData(BaseModel):
    players: List[PlayerData]  # List of players in the game
    game_start_timestamp: int  # Start timestamp of the game
    game_end_timestamp: Optional[int] = None  # End timestamp of the game
    total_moves: int = 0  # Total number of moves made in the game
    total_time_spent: Optional[float] = 0.0  # Total time spent by players in the game
    game_duration: Optional[int] = 0  # Duration of the game in seconds
    winner: Optional[str] = None  # Player who won the game
    game_result: Optional[str] = None  # Result of the game (win, loss, draw)
    opening: Optional[str] = None  # Opening or strategy played in the game
    game_mode: Optional[str] = None  # Game mode (e.g., Practice, Tournament)
    foul_count: Optional[int] = 0  # Total fouls committed in the game
    total_balls_potted: int = 0  # Total number of balls potted during the game
    total_walls_hit: int = 0  # Total number of wall hits during the game
    game_event: Optional[str] = None  # Event or tournament the game is part of
    game_metadata: Dict[str, str] = {}  # Additional metadata for the game (e.g., version, server info)
    player_statistics: Dict[str, PlayerStatistics] = {}  # Dictionary of player statistics

class GameEvent(BaseModel):
    event_type: str  # Event type (e.g., start, foul, shot)
    event_details: Dict[str, str]  # Details of the event (e.g., ball potted, foul type)
    timestamp: int  # Timestamp of the event

class GameEventLog(BaseModel):
    events: List[GameEvent]  # List of events during the game
    total_events: int  # Total number of events logged
    last_event_timestamp: int  # Timestamp of the last event

class GameSession(BaseModel):
    session_id: str  # Unique session ID
    game_data: List[Game8BallData]  # List of all games in the session
    event_log: GameEventLog  # Event log for the session
    session_start_timestamp: int  # Start timestamp of the session
    session_end_timestamp: Optional[int] = None  # End timestamp of the session
    session_duration: Optional[int] = 0  # Duration of the session in seconds
    total_games_played: int = 0  # Total games played in the session
    total_players: int = 0  # Total players in the session
    total_wins: int = 0  # Total wins in the session
    total_losses: int = 0  # Total losses in the session
    total_draws: int = 0  # Total draws in the session
    average_game_duration: float = 0.0  # Average game duration in seconds
    total_fouls: int = 0  # Total fouls in the session
    most_common_shot_type: Optional[str] = None  # Most common shot type in the session
    session_metadata: Dict[str, str] = {}  # Metadata for the session (e.g., tournament name)

class GameDatabase(BaseModel):
    sessions: List[GameSession]  # List of all sessions in the database
    total_sessions: int = 0  # Total number of sessions
    total_players: int = 0  # Total number of players
    total_games_played: int = 0  # Total number of games played
    total_balls_potted: int = 0  # Total number of balls potte
