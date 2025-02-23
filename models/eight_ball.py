from pydantic import BaseModel, Field
from typing import List, Optional

class TurnData(BaseModel):
    timestamp: int
    cue_ball_position: List[int] = Field(..., min_items=2, max_items=2)
    power: float
    angle: float
    ball_hit: Optional[int]
    balls_collided: List[int]
    balls_potted: List[int]
    walls_hit: List[int]


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


class Game8BallPayload(BaseModel):
    game: str
    data: dict
