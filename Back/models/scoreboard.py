from models.base import SQLModel
from sqlalchemy.orm import Mapped, mapped_column


class ScoreModel(SQLModel):
    __tablename__ = "scoreboard"

    row_id: Mapped[int] = mapped_column("row_id", primary_key=True, autoincrement=True)
    nickname: Mapped[str] = mapped_column("nickname")
    squares_number: Mapped[int] = mapped_column("squares_number")
    players_number: Mapped[int] = mapped_column("players_number")
    time: Mapped[int] = mapped_column("time")
    board: Mapped[str] = mapped_column("board")
