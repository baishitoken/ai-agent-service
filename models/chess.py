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


class PlayerData(BaseModel):
    username: str
    rating: int = Field(..., ge=0)
    games_played: int = Field(..., ge=0)
    games_won: int = Field(..., ge=0)
    games_lost: int = Field(..., ge=0)
    games_drawn: int = Field(..., ge=0)
    moves: List[MoveData]


class GameChessPayload(BaseModel):
    game: str
    data: dict
