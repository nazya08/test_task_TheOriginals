from typing import Optional

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from src.adapters.repositories.board import BoardRepository
from src.adapters.sqlalchemy.models import Board
from src.application.board.board_service import BoardService
from src.presentation.dependencies.base import get_db


def get_board_repo(db: Session = Depends(get_db)) -> BoardRepository:
    return BoardRepository(session=db)


def get_board_service(board_repo: BoardRepository = Depends(get_board_repo)) -> BoardService:
    return BoardService(board_repo=board_repo)


def get_board(
        board_id: Optional[int] = None,
        board_repo: BoardRepository = Depends(get_board_repo)
) -> Optional[Board]:
    if board_id is None:
        return None

    board = board_repo.get_board_by_id(board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")

    return board
