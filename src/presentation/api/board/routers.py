from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.status import HTTP_204_NO_CONTENT

from src.adapters.schemas.board import BoardCreate, BoardResponse, BoardExternalResponse, BoardUpdate
from src.adapters.schemas.user import UserResponse
from src.adapters.sqlalchemy.models import User, Board
from src.adapters.sqlalchemy.models.user import UserType
from src.application.board.board_service import BoardFilter, BoardService
from src.presentation.dependencies.base import get_db
from src.presentation.dependencies.board import get_board_service, get_board
from src.presentation.dependencies.user import get_current_active_superuser, get_current_active_user, get_user

router = APIRouter()


@router.get("/")
def read_all_boards(
        filters: BoardFilter = Depends(),
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        current_superuser: User = Depends(get_current_active_superuser)
):
    """
    Retrieve paginated boards response.
    """
    return filters.filter_boards(db, skip, limit)


@router.get("/public")
def read_public_boards(
        *,
        board_service: BoardService = Depends(get_board_service),
        skip: int = 0,
        limit: int = 100,
        current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve public boards response.
    """
    return board_service.get_public_boards(skip=skip, limit=limit)


@router.get("/user/{user_id}", response_model=List[BoardResponse])
def read_user_boards(
    user: User = Depends(get_user),
    current_user: User = Depends(get_current_active_user)
):
    """
    Read user boards by user_id.
    """
    return user.boards_owner


@router.get("/{board_id}", response_model=BoardExternalResponse)
def read_board_by_id(
    board: Board = Depends(get_board),
    board_service: BoardService = Depends(get_board_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Read a post by id.
    """
    count_of_lists = board_service.get_count_of_board_lists(board.id)
    count_of_members = board_service.get_count_of_board_members(board.id)

    if not board.is_public:
        if board.owner_id != current_user.id and current_user.type != UserType.admin:
            if not board_service.is_user_member_of_board(board, current_user):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You do not have permission to view this board"
                )

    board_detail = BoardResponse(
        id=board.id,
        name=board.name,
        is_public=board.is_public,
        owner_id=board.owner_id,
        created_at=board.created_at,
        updated_at=board.updated_at
    )
    return BoardExternalResponse(
        board_detail=board_detail,
        lists=count_of_lists,
        members=count_of_members
    )


@router.get("/{board_id}/members", response_model=List[UserResponse])
def read_board_members(
    board: Board = Depends(get_board),
    board_service: BoardService = Depends(get_board_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Read all members of board.
    """
    return board_service.get_board_members(board=board, current_user=current_user)


@router.post("/")
def create_board(
        *,
        board_service: BoardService = Depends(get_board_service),
        board_in: BoardCreate,
        current_user: User = Depends(get_current_active_user)
):
    """
    Create a board.
    """
    board = board_service.create_board(obj_in=board_in, current_user=current_user)

    return BoardResponse(
        id=board.id,
        name=board.name,
        is_public=board.is_public,
        owner_id=board.owner_id,
        created_at=board.created_at,
        updated_at=board.updated_at
    )


@router.patch("/{board_id}", response_model=BoardResponse)
def update_board(
    board_in: BoardUpdate,
    board_service: BoardService = Depends(get_board_service),
    board: Board = Depends(get_board),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update a board.
    """
    updated_board = board_service.update_board(board=board, board_data=board_in, current_user=current_user)

    return BoardResponse(
        id=updated_board.id,
        name=updated_board.name,
        is_public=updated_board.is_public,
        owner_id=current_user.id,
        created_at=updated_board.created_at,
        updated_at=updated_board.updated_at
    )


@router.delete("/{board_id}", status_code=HTTP_204_NO_CONTENT)
def remove_board(
    board: Board = Depends(get_board),
    board_service: BoardService = Depends(get_board_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a board.
    """
    return board_service.delete_board(board_id=board.id, current_user=current_user)


@router.post("/{board_id}/add_member/{user_id}", status_code=status.HTTP_201_CREATED)
def add_member_to_board(
    board: Board = Depends(get_board),
    user: User = Depends(get_user),
    board_service: BoardService = Depends(get_board_service),
    current_user: User = Depends(get_current_active_user),
):
    """
    Add a member to the board.
    """
    board_service.add_member_to_board(board=board, member_id=user.id, current_user=current_user)

    return {"detail": "Member added successfully"}


@router.delete("/{board_id}/remove-member/{user_id}", status_code=status.HTTP_200_OK)
def remove_member_from_board(
    board: Board = Depends(get_board),
    user: User = Depends(get_user),
    board_service: BoardService = Depends(get_board_service),
    current_user: User = Depends(get_current_active_user),
):
    """
    Remove a member from the board.
    """
    board_service.remove_member_from_board(board=board, member_id=user.id, current_user=current_user)

    return {"detail": "Member deleted successfully"}
