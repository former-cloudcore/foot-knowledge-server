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
        match board:
            case "grid":
                return await ScoreBoardDataManager(self.session).get_scoreboard_by_board(board, "squares_number")
            case "connections":
                return await ScoreBoardDataManager(self.session).get_scoreboard_by_board(board, "shortest_path")

    async def add_score(self, score_row: InputScoreRowSchema, board: str = "grid") -> List[ScoreRowSchema]:
        """Add score to scoreboard and return updated"""
        match board:
            case "grid":
                return await ScoreBoardDataManager(self.session).add_grid_score(score_row, board)
            case "connections":
                return await ScoreBoardDataManager(self.session).add_connections_score(score_row, board)


class ScoreBoardDataManager(BaseDataManager):
    def sort_key(self, item, property_name, ascending=True):
        value = getattr(item, property_name)
        return value if value is not None else (float('inf') if ascending else float('-inf'))
    
    async def get_scoreboard_by_board(self, board: str, sortBy: str, ascending=True) -> List[ScoreRowSchema]:
        stmt = (
            select(ScoreModel)
            .where(ScoreModel.board == board)
            .order_by(getattr(ScoreModel, sortBy).asc() if ascending else getattr(ScoreModel, sortBy).desc())
        )

        result = await self.session.execute(stmt)
        models = result.scalars().all() if result else []

        schemas = [ScoreRowSchema(**model.to_dict()) for model in models]
        return schemas

    async def add_grid_score(self, score_row: InputScoreRowSchema, board: str) -> List[ScoreRowSchema]:
        ascending = False
        schemas: List[ScoreRowSchema] = await self.get_scoreboard_by_board(
            board, "squares_number", ascending
        )

        if len(schemas) < 10:
            # if scoreboard is not full
            score_row = await self.add_score(score_row, board)
            schemas.append(score_row)
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

        sorted_schemas = schemas.sort(key=lambda x: self.sort_key(x, "squares_number", ascending))
        return  sorted_schemas if sorted_schemas else []
    
    async def add_connections_score(self, score_row: InputScoreRowSchema, board: str) -> List[ScoreRowSchema]:
        ascending = True
        print(score_row)
        schemas: List[ScoreRowSchema] = await self.get_scoreboard_by_board(
            board, "shortest_path", ascending
        )
        
        if len(schemas) < 10:
            # if scoreboard is not full
            score_row = await self.add_score(score_row, board)
            schemas.append(score_row)
        elif schemas[-1].shortest_path < score_row.shortest_path or (
                schemas[-1].shortest_path == score_row.shortest_path
                and schemas[-1].time
                < score_row.time  # check if this is the condition that we want
        ):
            # if new score is better than the last one
            await self.remove_score(schemas[-1].row_id)
            schemas.pop()
            score_row = await self.add_score(score_row, board)
            schemas.append(score_row)

        sorted_schemas = schemas.sort(key=lambda x: self.sort_key(x, "shortest_path", ascending))
        return  sorted_schemas if sorted_schemas else []

    async def add_score(self, score_row: InputScoreRowSchema, board: str) -> ScoreRowSchema:
        new_score = ScoreModel(
            nickname=score_row.nickname,
            shortest_path=score_row.shortest_path,
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
    


