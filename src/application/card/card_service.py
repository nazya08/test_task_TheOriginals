from typing import List

from fastapi import HTTPException, Depends
from starlette import status

from src.adapters.repositories.card.card import CardRepository
from src.adapters.schemas.card import CardCreate
from src.adapters.sqlalchemy.models import Card, User, Board
from src.adapters.sqlalchemy.models.user import UserType
from src.application.board.board_service import BoardService


class CardService:
    def __init__(self, card_repo: CardRepository, board_service: BoardService) -> None:
        self.card_repo = card_repo
        self.board_service = board_service

    def get_cards_by_list(self, list_id: int) -> List[Card]:
        return self.card_repo.get_cards(list_id=list_id)

    def get_card(self, list_id: int, card_id: int) -> Card:
        return self.card_repo.get_card(list_id=list_id, card_id=card_id)

    def create_card(self, board: Board, list_id: int, obj_in: CardCreate, current_user: User) -> Card:
        if board.owner_id != current_user.id and current_user.type != UserType.admin:
            if not self.board_service.is_user_member_of_board(board, current_user):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You do not have permission to create a card in this board"
                )

        card_data = obj_in.dict()

        responsible_person_id = card_data.get("responsible_person_id")

        if responsible_person_id is None:
            # Якщо користувач є власником дошки, призначити його як відповідального
            if current_user.id == board.owner_id:
                responsible_person_id = board.owner_id
            else:
                responsible_person_id = current_user.id

        if current_user.id == board.owner_id:
            if not self.board_service.is_user_member_of_board_by_id(board=board, user_id=responsible_person_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Can't make this person being responsible for this card."
                )
        else:
            if responsible_person_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You can only assign yourself as responsible."
                )

        card_data["responsible_person_id"] = responsible_person_id
        card_data["list_id"] = list_id

        card_db_obj = Card(**card_data)

        self.card_repo.create_card(card_db_obj)

        return card_db_obj

    def update_card(self, board: Board, list_id: int, card_id: int, obj_in: CardCreate, current_user: User) -> Card:
        if board.owner_id != current_user.id and current_user.type != UserType.admin:
            if not self.board_service.is_user_member_of_board(board, current_user):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You do not have permission to update a card in this board"
                )

        card_data = obj_in.dict(exclude_unset=True)

        updated_card = self.card_repo.update_card(list_id=list_id, card_id=card_id, card_data=card_data)

        return updated_card

    def delete_card(self, board: Board, list_id: int, card_id: int, current_user: User) -> None:
        if board.owner_id != current_user.id and current_user.type != UserType.admin:
            raise HTTPException(
                status_code=403, detail="You do not have permission to delete this card"
            )

        self.card_repo.delete_card(list_id=list_id, card_id=card_id)

    def add_performer(self, board: Board, list_id: int, card_id: int, user: User, current_user: User) -> None:
        if board.owner_id != current_user.id and current_user.type != UserType.admin:
            raise HTTPException(
                status_code=403, detail="You do not have permission to perform this action"
            )

        card = self.card_repo.get_card(list_id=list_id, card_id=card_id)
        if not self.board_service.is_user_member_of_board_by_id(board=board, user_id=user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not a member of this board."
            )
        card.performers.append(user)
        self.card_repo.save_card(card)

    def remove_performer(self, board: Board, list_id: int, card_id: int, user: User, current_user: User):
        if board.owner_id != current_user.id and current_user.type != UserType.admin:
            raise HTTPException(
                status_code=403, detail="You do not have permission to perform this action"
            )

        card = self.card_repo.get_card(list_id=list_id, card_id=card_id)
        if user in card.performers:
            card.performers.remove(user)
            self.card_repo.save_card(card)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Performer not found."
            )

    def get_performers(self, board: Board, list_id: int, card_id: int, current_user: User) -> List[User]:
        if board.owner_id != current_user.id and current_user.type != UserType.admin:
            raise HTTPException(
                status_code=403, detail="You do not have permission to perform this action"
            )

        card = self.card_repo.get_card(list_id=list_id, card_id=card_id)
        if not self.board_service.is_user_member_of_board_by_id(board=board, user_id=current_user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not a member of this board."
            )

        return card.performers

