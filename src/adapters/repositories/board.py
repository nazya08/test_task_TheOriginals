from typing import List

from typing_extensions import Optional

from src.adapters.repositories.base import SQLAlchemyRepo
from src.adapters.repositories.common.board import BoardSaver, BoardReader, BoardsReader
from src.adapters.sqlalchemy.models import Board, User
from src.adapters.sqlalchemy.models.board import board_members_association


class BoardRepository(SQLAlchemyRepo, BoardSaver, BoardReader, BoardsReader):
    def save_board(self, board: Board) -> None:
        self._session.add(board)
        self._session.commit()
        self._session.refresh(board)

    def update_board(self, board_id: int, board_data: dict) -> Optional[Board]:
        board = self.get_board_by_id(board_id)
        if board:
            for key, value in board_data.items():
                setattr(board, key, value)
            self._session.commit()
            self._session.refresh(board)
        return board

    def delete_board(self, board_id: int) -> None:
        board = self.get_board_by_id(board_id)
        if board:
            self._session.delete(board)
            self._session.commit()

    def add_member_to_board(self, board_id: int, member_id: int) -> None:
        board = self.get_board_by_id(board_id)
        if board:
            member = self._session.query(User).filter(User.id == member_id).first()
            board.members.append(member)
            self._session.commit()
            self._session.refresh(board)

    def remove_member_from_board(self, board_id: int, member_id: int) -> bool:
        result = self._session.execute(
            board_members_association.delete()
            .where(board_members_association.c.board_id == board_id)
            .where(board_members_association.c.user_id == member_id)
        )

        self._session.commit()

        if result.rowcount > 0:
            return True
        return False

    def get_board_members(self, board_id: int) -> List[User]:
        board = self._session.query(Board).filter(Board.id == board_id).first()
        return board.members

    def get_board_by_id(self, board_id: int) -> Optional[Board]:
        return self._session.query(Board).filter(Board.id == board_id).first()

    def get_list_of_public_boards(self, skip: int = 0, limit: int = 10) -> List[Board]:
        return self._session.query(Board).filter(Board.is_public == True).offset(skip).limit(limit).all()

    def get_lists_count(self, board_id: int) -> int:
        board = self.get_board_by_id(board_id)
        if board:
            return len(board.lists)

    def get_members_count(self, board_id: int) -> int:
        board = self.get_board_by_id(board_id)
        if board:
            members_count = len(board.members)
            if board.owner_id not in board.members:
                members_count += 1

            return members_count
