from typing import List as ListType

from fastapi import APIRouter, Depends
from starlette.status import HTTP_204_NO_CONTENT

from src.adapters.schemas.card import CardUpdate, CardResponse, CardCreate, CardExternalResponse
from src.adapters.schemas.user import UserResponse
from src.adapters.sqlalchemy.models import Board, User, List, Card
from src.application.card.card_service import CardService
from src.presentation.dependencies.board import get_board
from src.presentation.dependencies.card import get_card, get_card_service
from src.presentation.dependencies.list import get_list
from src.presentation.dependencies.user import get_current_active_user, get_user

router = APIRouter()


@router.get("/{board_id}/lists/{list_id}/cards")
def read_all_cards(
    board: Board = Depends(get_board),
    list: List = Depends(get_list),
    card_service: CardService = Depends(get_card_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve cards by list_id.
    """
    lists = card_service.get_cards_by_list(list_id=list.id)
    return lists


@router.get("/{board_id}/lists/{list_id}/cards/{card_id}", response_model=CardExternalResponse)
def read_card_by_id(
    board: Board = Depends(get_board),
    list: List = Depends(get_list),
    card: Card = Depends(get_card),
    current_user: User = Depends(get_current_active_user)
) -> CardExternalResponse:
    """
    Read a card by id.
    """
    return CardExternalResponse(
        card_detail=CardResponse(
            id=card.id,
            title=card.title,
            description=card.description,
            priority=card.priority,
            responsible_person_id=card.responsible_person_id,
            list_id=card.list_id,
            due_date=card.due_date,
            reminder_datetime=card.reminder_datetime,
            created_at=card.created_at,
            updated_at=card.updated_at
        ),
        performers=[UserResponse.from_orm(performer) for performer in card.performers],
        comments_count=len(card.comments),
        attachments_count=len(card.attachments),
        checklists_count=len(card.check_lists),
    )


@router.post("/{board_id}/lists/{list_id}/cards", response_model=CardResponse)
def create_card(
    card_in: CardCreate,
    board: Board = Depends(get_board),
    list: List = Depends(get_list),
    card_service: CardService = Depends(get_card_service),
    current_user: User = Depends(get_current_active_user)
) -> CardResponse:
    """
    Create a new card.
    """
    card = card_service.create_card(board=board, list_id=list.id, obj_in=card_in, current_user=current_user)

    return CardResponse(
        id=card.id,
        title=card.title,
        description=card.description,
        priority=card.priority,
        responsible_person_id=card.responsible_person_id,
        list_id=card.list_id,
        due_date=card.due_date,
        reminder_datetime=card.reminder_datetime,
        created_at=card.created_at,
        updated_at=card.updated_at
    )


@router.patch("/{board_id}/lists/{list_id}/cards/{card_id}", response_model=CardResponse)
def update_card(
        card_in: CardUpdate,
        board: Board = Depends(get_board),
        list: List = Depends(get_list),
        card: Card = Depends(get_card),
        card_service: CardService = Depends(get_card_service),
        current_user: User = Depends(get_current_active_user)
) -> CardResponse:
    """
    Update a card.
    """
    updated_card = card_service.update_card(
        board=board, list_id=list.id, card_id=card.id, obj_in=card_in, current_user=current_user
    )

    return CardResponse(
        id=updated_card.id,
        title=updated_card.title,
        description=updated_card.description,
        priority=updated_card.priority,
        responsible_person_id=updated_card.responsible_person_id,
        list_id=updated_card.list_id,
        due_date=updated_card.due_date,
        reminder_datetime=updated_card.reminder_datetime,
        created_at=updated_card.created_at,
        updated_at=updated_card.updated_at
    )


@router.delete("/{board_id}/lists/{list_id}/cards/{card_id}", status_code=HTTP_204_NO_CONTENT)
def remove_card(
    board: Board = Depends(get_board),
    list: List = Depends(get_list),
    card: Card = Depends(get_card),
    card_service: CardService = Depends(get_card_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a card.
    """
    return card_service.delete_card(board=board, list_id=list.id, card_id=card.id, current_user=current_user)


@router.get("/{board_id}/lists/{list_id}/cards/{card_id}/performers", response_model=ListType[UserResponse])
def get_performers(
    board: Board = Depends(get_board),
    list: List = Depends(get_list),
    card: Card = Depends(get_card),
    card_service: CardService = Depends(get_card_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all performers for a card.
    """
    performers = card_service.get_performers(board=board, list_id=list.id, card_id=card.id, current_user=current_user)
    return performers


@router.post("/{board_id}/lists/{list_id}/cards/{card_id}/performers/{user_id}")
def add_performer(
    user: User = Depends(get_user),
    board: Board = Depends(get_board),
    list: List = Depends(get_list),
    card: Card = Depends(get_card),
    card_service: CardService = Depends(get_card_service),
    current_user: User = Depends(get_current_active_user)
) -> dict:
    """
    Add a performer to a card.
    """
    card_service.add_performer(
        board=board, list_id=list.id, card_id=card.id, user=user, current_user=current_user
    )
    return {"detail": "Performer added successfully to the card '{}' #{}".format(card.title, card.id)}


@router.delete("/{board_id}/lists/{list_id}/cards/{card_id}/performers/{user_id}")
def remove_performer(
    user: User = Depends(get_user),
    board: Board = Depends(get_board),
    list: List = Depends(get_list),
    card: Card = Depends(get_card),
    card_service: CardService = Depends(get_card_service),
    current_user: User = Depends(get_current_active_user)
) -> dict:
    """
    Remove a performer from a card.
    """
    card_service.remove_performer(
        board=board, list_id=list.id, card_id=card.id, user=user, current_user=current_user
    )
    return {"detail": "Performer deleted successfully"}

