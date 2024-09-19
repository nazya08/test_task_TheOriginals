from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from starlette.status import HTTP_204_NO_CONTENT

from src.adapters.schemas.list import ListCreate, ListResponse, ListUpdate, ListExternalResponse
from src.adapters.sqlalchemy.models import Board, User, List
from src.adapters.sqlalchemy.models.user import UserType
from src.application.board.board_service import BoardService
from src.application.list.list_service import ListService
from src.presentation.dependencies.board import get_board, get_board_service
from src.presentation.dependencies.list import get_list_service, get_list
from src.presentation.dependencies.user import get_current_active_user

router = APIRouter()


# TODO: delete list | read list by id | read all lists
@router.get("/{board_id}/lists")
def read_all_lists(
    board: Board = Depends(get_board),
    list_service: ListService = Depends(get_list_service),
    board_service: BoardService = Depends(get_board_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve lists by board_id.
    """
    if not board.is_public:
        if board.owner_id != current_user.id and current_user.type != UserType.admin:
            if not board_service.is_user_member_of_board(board, current_user):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You do not have permission to view this board"
                )

    lists = list_service.get_lists_by_board(board_id=board.id)
    return lists


@router.get("/{board_id}/lists/{list_id}", response_model=ListExternalResponse)
def read_list_by_id(
    board: Board = Depends(get_board),
    list: List = Depends(get_list),
    board_service: BoardService = Depends(get_board_service),
    current_user: User = Depends(get_current_active_user)
) -> ListExternalResponse:
    """
    Read a list by id.
    """
    if not board.is_public:
        if board.owner_id != current_user.id and current_user.type != UserType.admin:
            if not board_service.is_user_member_of_board(board, current_user):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You do not have permission to view this board"
                )
    return ListExternalResponse(
        list_detail=ListResponse(
            id=list.id,
            name=list.name,
            position=list.position,
            board_id=list.board_id,
            created_at=list.created_at,
            updated_at=list.updated_at
        ),
        cards=len(list.cards)
    )


@router.post("/{board_id}/lists", response_model=ListResponse)
def create_list(
    list_in: ListCreate,
    board: Board = Depends(get_board),
    list_service: ListService = Depends(get_list_service),
    current_user: User = Depends(get_current_active_user)
) -> ListResponse:
    """
    Create a new list.
    """
    list_obj = list_service.create_list(board=board, obj_in=list_in, current_user=current_user)

    return ListResponse(
        id=list_obj.id,
        name=list_obj.name,
        position=list_obj.position,
        board_id=list_obj.board_id,
        created_at=list_obj.created_at,
        updated_at=list_obj.updated_at
    )


@router.patch("/{board_id}/lists/{list_id}", response_model=ListResponse)
def update_list(
        list_in: ListUpdate,
        board: Board = Depends(get_board),
        list: List = Depends(get_list),
        list_service: ListService = Depends(get_list_service),
        current_user: User = Depends(get_current_active_user)
) -> ListResponse:
    """
    Update a list.
    """
    updated_list = list_service.update_list(
        board=board, list=list, obj_in=list_in, current_user=current_user
    )

    return ListResponse(
        id=updated_list.id,
        name=updated_list.name,
        position=updated_list.position,
        board_id=updated_list.board_id,
        created_at=updated_list.created_at,
        updated_at=updated_list.updated_at
    )


@router.delete("/{board_id}/lists/{list_id}", status_code=HTTP_204_NO_CONTENT)
def remove_list(
    board: Board = Depends(get_board),
    list: List = Depends(get_list),
    list_service: ListService = Depends(get_list_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a list.
    """
    return list_service.delete_list(board=board, list=list, current_user=current_user)

