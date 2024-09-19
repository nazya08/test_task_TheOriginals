from typing import Optional, Union, List, Dict

from fastapi import HTTPException, Depends
from fastapi_filter.contrib.sqlalchemy import Filter
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.adapters.repositories.board import BoardRepository
from src.adapters.schemas.board import BoardCreate, BoardUpdate
from src.adapters.sqlalchemy.models import Board, User
from src.adapters.sqlalchemy.models.user import UserType


class BoardService:
    def __init__(self, board_repo: BoardRepository) -> None:
        self.board_repo = board_repo

    def create_board(self, obj_in: BoardCreate, current_user: User) -> Board:
        if not current_user:
            raise HTTPException(status_code=400, detail="Invalid current user")

        board_data = obj_in.dict()
        board_data["owner_id"] = current_user.id

        board_db_obj = Board(**board_data)
        self.board_repo.save_board(board_db_obj)

        return board_db_obj

    def update_board(self, board: Board, board_data: BoardUpdate, current_user: User) -> Board:
        if board.owner_id != current_user.id:
            raise HTTPException(
                status_code=403, detail="You do not have permission to perform this action"
            )

        updated_board = self.board_repo.update_board(board.id, board_data.dict())

        return updated_board

    def delete_board(self, board_id: int, current_user: User) -> None:
        board = self.board_repo.get_board_by_id(board_id)
        if board.owner_id != current_user.id and current_user.type != UserType.admin:
            raise HTTPException(
                status_code=403, detail="You do not have permission to delete this board"
            )

        self.board_repo.delete_board(board_id)

    def get_public_boards(self, skip: int = 0, limit: int = 10) -> List[Board]:
        return self.board_repo.get_list_of_public_boards(skip=skip, limit=limit)

    def get_board_members(self, board: Board, current_user: User) -> List[User]:
        if not board.is_public and board.owner_id != current_user.id and current_user.type != UserType.admin:
            raise HTTPException(status_code=403, detail="You do not have permission to see members of this board")
        return self.board_repo.get_board_members(board_id=board.id)

    def is_user_member_of_board(self, board: Board, current_user: User) -> bool:
        board_members = self.board_repo.get_board_members(board_id=board.id)

        if current_user.type == UserType.admin or current_user.id == board.owner_id:
            return True
        return current_user.id in [member.id for member in board_members]

    def add_member_to_board(self, board: Board, member_id: int, current_user: User) -> None:
        if board.owner_id != current_user.id and current_user.type != UserType.admin:
            raise HTTPException(status_code=403, detail="You do not have permission to add members to this board")

        if member_id == current_user.id:
            raise HTTPException(status_code=400, detail="Board owner cannot add themselves as a member")

        if any(member.id == member_id for member in board.members):
            raise HTTPException(status_code=400, detail="User is already a member of this board")

        self.board_repo.add_member_to_board(board_id=board.id, member_id=member_id)

    def remove_member_from_board(self, board: Board, member_id: int, current_user: User) -> None:
        if board.owner_id != current_user.id and current_user.type != UserType.admin:
            raise HTTPException(status_code=403, detail="You do not have permission to remove members from this board")

        if member_id == current_user.id:
            raise HTTPException(status_code=403, detail="Administrators cannot remove themselves")

        removed_user = self.board_repo.remove_member_from_board(board_id=board.id, member_id=member_id)
        if not removed_user:
            raise HTTPException(status_code=404, detail="User is not a member of the board")

    def get_count_of_board_lists(self, board_id: int) -> int:
        return self.board_repo.get_lists_count(board_id)

    def get_count_of_board_members(self, board_id: int) -> int:
        return self.board_repo.get_members_count(board_id)


class BoardFilter(Filter):
    name: Optional[str] = None
    is_public: Optional[bool] = None

    class Constants(Filter.Constants):
        model = Board
        ordering_field_name = "order_by"
        search_field_name = "search"

    def filter_boards(
            self, db: Session, skip: int, limit: int
    ) -> Union[List[Board], Dict[str, str]]:
        """
        Filters and retrieves boards based on the provided filter parameters.

        Args:
            db: SQLAlchemy Session object for database access.
            skip: The number of boards to skip before returning results (pagination).
            limit: The maximum number of boards to return.

        Returns:
            A list of `Board` objects if the filtering is successful, or a dictionary
            containing an error message if any errors occur.

        Raises:
            SQLAlchemyError: If any database-related error occurs during the filtering process.

        """

        try:
            query = db.query(Board)

            if self.name:
                query = query.filter(Board.name.ilike(f"%{self.name}%"))

            if self.is_public is not None:
                query = query.filter(Board.is_public == self.is_public)

            boards = query.offset(skip).limit(limit).all()
            return boards

        except SQLAlchemyError as e:
            return {"error": str(e)}
