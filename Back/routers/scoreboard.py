from typing import List

from backend.session import create_session
from fastapi import APIRouter, Depends
from schemas.scoreboard import ScoreRowSchema, InputScoreRowSchema
from services.scoreboard import ScoreBoardService
from sqlalchemy.orm import Session

router = APIRouter(prefix="/scoreboard")


@router.get("/grid", response_model=List[ScoreRowSchema])
async def get_grid_scores(
        session: Session = Depends(create_session),
) -> List[ScoreRowSchema]:
    return await ScoreBoardService(session).get_scoreboard_by_board("grid")


@router.post("/grid", response_model=List[ScoreRowSchema])
async def add_grid_score(
        score_row: InputScoreRowSchema,
        session: Session = Depends(create_session),
) -> List[ScoreRowSchema]:
    print("ho")
    return await ScoreBoardService(session).add_score(score_row, "grid")
