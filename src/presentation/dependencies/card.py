from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from src.adapters.repositories.card.card import CardRepository
from src.application.board.board_service import BoardService
from src.application.card.card_service import CardService
from src.presentation.dependencies.base import get_db
from src.presentation.dependencies.board import get_board_service


def get_card_repo(db: Session = Depends(get_db)) -> CardRepository:
    return CardRepository(session=db)


def get_card_service(
        card_repo: CardRepository = Depends(get_card_repo),
        board_service: BoardService = Depends(get_board_service)
) -> CardService:
    return CardService(card_repo=card_repo, board_service=board_service)


def get_card(list_id: int, card_id: int, card_repo: CardRepository = Depends(get_card_repo)):
    card = card_repo.get_card(list_id=list_id, card_id=card_id)
    if not card:
        raise HTTPException(
            status_code=404, detail="Card not found"
        )

    return card
