from pydantic import BaseModel, Field
from typing import List, Optional

class MoveData(BaseModel):
    move_number: int
    player: str
    from_square: str
    to_square: str
    piece: str
    captured_piece: Optional[str]
    check: bool = False
    checkmate: bool = False
    time: Optional[float]

class GameHistory(BaseModel):
    result: str
    opponent: str
    score_diff: int
    opening: Optional[str]
    timestamp: int

class PlayerData(BaseModel):
    username: str
    rating: Optional[int] = Field(default=0, ge=0)
    games_played: int = Field(..., ge=0)
    games_won: int = Field(..., ge=0)
    games_lost: int = Field(..., ge=0)
    games_drawn: int = Field(..., ge=0)
    moves: List[MoveData]
    game_history: List[GameHistory] = []

class GameChessPayload(BaseModel):
    game: str
    data: dict