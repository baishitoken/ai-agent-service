from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class MoveData(BaseModel):
    move_number: int
    player: str
    from_square: str
    to_square: str
    piece: str
    captured_piece: Optional[str]
    check: bool = False
    checkmate: bool = False
    time: Optional[float]  # Time taken for this move in seconds
    move_duration: Optional[int] = 0  # Duration of the move in seconds
    castling: Optional[bool] = False  # Indicates if the move was a castling
    en_passant: Optional[bool] = False  # Indicates if the move was an en passant

class GameHistory(BaseModel):
    result: str  # win, loss, or draw
    opponent: str
    score_diff: int  # Difference in points
    opening: Optional[str]  # The opening used in the game
    timestamp: int  # Timestamp of the game
    total_moves: int  # Total number of moves in the game
    average_move_time: Optional[float] = 0.0  # Average time per move
    game_duration: Optional[int] = 0  # Duration of the game in seconds
    is_bullet_game: Optional[bool] = False  # Was the game a bullet game?
    game_mode: Optional[str] = None  # Type of game (e.g., Blitz, Rapid, Classical)
    game_event: Optional[str] = None  # Additional event related to the game (e.g., Tournament)
    winner: Optional[str] = None  # Player who won the game (if available)

class PlayerStatistics(BaseModel):
    total_wins: int
    total_losses: int
    total_draws: int
    total_checkmates: int
    total_stalemates: int
    total_castling: int
    total_en_passant: int
    total_forks: int
    total_pins: int
    total_material_lost: int  # Total value of material lost during the game
    average_game_duration: float  # Average game duration in seconds
    total_blunders: int  # Number of blunders made
    total_check_threats: int  # Number of times a check threat was made
    win_percentage: float  # Percentage of games won
    highest_rating: int  # Highest rating reached by the player
    current_rating: int  # Current rating of the player
    longest_win_streak: int  # Longest streak of wins
    longest_loss_streak: int  # Longest streak of losses
    longest_draw_streak: int  # Longest streak of draws
    average_rating_change: float  # Average rating change per game

class PlayerData(BaseModel):
    username: str
    rating: Optional[int] = Field(default=0, ge=0)
    games_played: int = Field(..., ge=0)
    games_won: int = Field(..., ge=0)
    games_lost: int = Field(..., ge=0)
    games_drawn: int = Field(..., ge=0)
    moves: List[MoveData]  # List of moves made by the player
    game_history: List[GameHistory] = []  # History of games played
    player_statistics: PlayerStatistics  # Nested player statistics
    last_game_timestamp: Optional[int] = None  # Timestamp of the last game played
    total_blunders: int = 0  # Total blunders made by the player
    total_forks: int = 0  # Total forks executed by the player
    total_pins: int = 0  # Total pins executed by the player
    opening_preferences: Optional[Dict[str, int]] = {}  # Most common openings played
    favorite_piece: Optional[str] = None  # Player's favorite piece (e.g., Knight, Queen)
    total_checkmates: int = 0  # Total checkmates performed by the player
    total_check_threats: int = 0  # Total check threats made by the player
    most_common_checkmate_method: Optional[str] = None  # Most common way the player delivers checkmate
    game_mode_stats: Dict[str, int] = {}  # Game mode statistics (e.g., Blitz, Classical)

class ChessGameData(BaseModel):
    players: List[PlayerData]  # List of players in the game
    game_start_timestamp: int  # Start timestamp of the game
    game_end_timestamp: Optional[int] = None  # End timestamp of the game
    total_moves: int = 0  # Total number of moves made in the game
    total_time_spent: Optional[float] = 0.0  # Total time spent by players in the game
    game_duration: Optional[int] = 0  # Duration of the game in seconds
    winner: Optional[str] = None  # Player who won the game
    game_result: Optional[str] = None  # Result of the game (win, loss, draw)
    opening: Optional[str] = None  # Opening played in the game
    game_mode: Optional[str] = None  # Game mode (e.g., Blitz, Rapid)
    is_blitz_game: Optional[bool] = False  # Is the game a Blitz game?
    total_checkmates: int = 0  # Total number of checkmates performed in the game
    total_stalemates: int = 0  # Total number of stalemates in the game
    game_event: Optional[str] = None  # Event or tournament the game is part of
    player_statistics: Dict[str, PlayerStatistics] = {}  # Dictionary of player statistics

class ChessEvent(BaseModel):
    event_type: str  # Event type (e.g., move, check, checkmate)
    event_details: Dict[str, str]  # Detailed information about the event
    timestamp: int  # Timestamp of when the event occurred

class ChessEventLog(BaseModel):
    events: List[ChessEvent]  # List of events during the game
    total_events: int  # Total number of events logged
    last_event_timestamp: int  # Timestamp of the last event

class ChessSession(BaseModel):
    session_id: str  # Unique identifier for the session
    game_data: List[ChessGameData]  # List of games in the session
    event_log: ChessEventLog  # Event log for the session
    session_start_timestamp: int  # Start timestamp of the session
    session_end_timestamp: Optional[int] = None  # End timestamp of the session
    session_duration: Optional[int] = 0  # Duration of the session in seconds
    total_games_played: int = 0  # Total games played in the session
    total_players: int = 0  # Total players in the session
    total_wins: int = 0  # Total wins in the session
    total_losses: int = 0  # Total losses in the session
    total_draws: int = 0  # Total draws in the session
    average_game_duration: float = 0.0  # Average game duration in seconds
    total_checkmates: int = 0  # Total checkmates in the session
    most_common_opening: Optional[str] = None  # Most common opening played in the session
    session_metadata: Dict[str, str] = {}  # Metadata for the session (e.g., tournament name)

class ChessDatabase(BaseModel):
    sessions: List[ChessSession]  # List of all sessions in the database
    total_sessions: int = 0  # Total number of sessions in the database
    total_players: int = 0  # Total number of players across all sessions
    total_games_played: int = 0  # Total number of games played across all sessions
    total_checkmates: int = 0  # Total checkmates across all sessions
    total_stalemates: int = 0  # Total stalemates across all sessions
    overall_player_stats: Dict[str, PlayerStatistics] = {}  # Player stats aggregated across all sessions
    global_metadata: Dict[str, str] = {}  # Metadata for the global database (e.g., version, server info)
