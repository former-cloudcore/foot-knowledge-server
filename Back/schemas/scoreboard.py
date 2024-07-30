from pydantic import BaseModel
from typing import Optional

class ScoreRowSchema(BaseModel):
    row_id: int
    nickname: str
    squares_number: Optional[int] = None
    players_number: int
    shortest_path: Optional[int] = None
    time: int
    board: str


class InputScoreRowSchema(BaseModel):
    nickname: str
    squares_number: Optional[int] = None
    players_number: int
    shortest_path: Optional[int] = None
    time: int
