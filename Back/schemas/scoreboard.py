from pydantic import BaseModel


class ScoreRowSchema(BaseModel):
    row_id: int
    nickname: str
    squares_number: int
    players_number: int
    time: int
    board: str


class InputScoreRowSchema(BaseModel):
    nickname: str
    squares_number: int
    players_number: int
    time: int
