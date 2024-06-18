from typing import List

from models.scoreboard import ScoreModel
from schemas.scoreboard import ScoreRowSchema, InputScoreRowSchema
from services.base import (
    BaseDataManager,
    BaseService,
)
from sqlalchemy import select, delete


class ScoreBoardService(BaseService):
    async def get_scoreboard_by_board(
            self, board: str = "grid"
    ) -> List[ScoreRowSchema]:
        """Select scoreboard by board name. Default is grid"""

        return await ScoreBoardDataManager(self.session).get_scoreboard_by_board(board)

    async def add_score(self, score_row: InputScoreRowSchema, board: str = "grid") -> List[ScoreRowSchema]:
        """Add score to scoreboard and return updated"""

        return await ScoreBoardDataManager(self.session).add_grid_score(score_row, board)


class ScoreBoardDataManager(BaseDataManager):
    async def get_scoreboard_by_board(self, board: str) -> List[ScoreRowSchema]:
        stmt = (
            select(ScoreModel)
            .where(ScoreModel.board == board)
            .order_by(ScoreModel.squares_number.desc())
        )

        result = await self.session.execute(stmt)
        models = result.scalars().all()

        schemas = [ScoreRowSchema(**model.to_dict()) for model in models]
        return schemas

    async def add_grid_score(self, score_row: InputScoreRowSchema, board: str) -> List[ScoreRowSchema]:
        schemas: List[ScoreRowSchema] = await self.get_scoreboard_by_board(
            board
        )

        if len(schemas) < 10:
            # if scoreboard is not full
            score_row = await self.add_score(score_row, board)
            schemas.append(score_row)
            schemas.sort(key=lambda x: x.squares_number, reverse=True)
        elif schemas[-1].squares_number < score_row.squares_number or (
                schemas[-1].squares_number == score_row.squares_number
                and schemas[-1].time
                < score_row.time  # check if this is the condition that we want
        ):
            # if new score is better than the last one
            await self.remove_score(schemas[-1].row_id)
            schemas.pop()
            score_row = await self.add_score(score_row, board)
            schemas.append(score_row)
            schemas.sort(key=lambda x: x.squares_number, reverse=True)

        return schemas

    async def add_score(self, score_row: InputScoreRowSchema, board: str) -> ScoreRowSchema:
        new_score = ScoreModel(
            nickname=score_row.nickname,
            squares_number=score_row.squares_number,
            players_number=score_row.players_number,
            time=score_row.time,
            board=board
        )
        self.session.add(new_score)
        await self.session.commit()
        await self.session.refresh(new_score)  # To fetch the generated ID
        return new_score

    async def remove_score(self, row_id: int) -> None:
        stmt = delete(ScoreModel).where(ScoreModel.row_id == row_id)
        await self.session.execute(stmt)
        await self.session.commit()
