from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from src.adapters.repositories.list import ListRepository
from src.application.list.list_service import ListService
from src.presentation.dependencies.base import get_db


def get_list_repo(db: Session = Depends(get_db)) -> ListRepository:
    return ListRepository(session=db)


def get_list_service(list_repo: ListRepository = Depends(get_list_repo)) -> ListService:
    return ListService(list_repo=list_repo)


def get_list(board_id: int, list_id: int, list_repo: ListRepository = Depends(get_list_repo)):
    list_obj = list_repo.get_list_by_id(board_id=board_id, list_id=list_id)
    if not list_obj:
        raise HTTPException(
            status_code=404, detail="List not found"
        )

    return list_obj
