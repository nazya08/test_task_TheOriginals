from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from src.adapters.schemas.pagination import Pagination, PaginationResponse
from src.adapters.schemas.user import UserResponse, UserCreate, UserId, UsersListResponse, UserExtendedData, UserUpdate
from src.adapters.sqlalchemy.models import User
from src.application.common.exceptions import UserNotFoundError, UserExistsError, WeakPasswordError
from src.presentation.dependencies.user import get_current_active_superuser, get_current_active_user, get_user_service
from src.application.user.user_service import UserService

router = APIRouter()


@router.get("/", response_model=UsersListResponse)
def read_users(
        skip: int = 0,
        limit: int = 10,
        user_service: UserService = Depends(get_user_service),
        current_superuser: User = Depends(get_current_active_superuser),
) -> UsersListResponse:
    """
    Retrieve paginated users response.
    """
    users = user_service.get_users_list(Pagination(skip=skip, limit=limit))
    total = user_service.user_repo.get_users_count()

    return UsersListResponse(
        pagination_detail=PaginationResponse(
            skip=skip, limit=limit, total=total
        ),
        users_list=[
            UserResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                is_active=user.is_active,
                type=user.type,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
            for user in users
        ]
    )


@router.get("/{user_id}", response_model=UserResponse)
def read_user_by_id(
        user_id: int,
        user_service: UserService = Depends(get_user_service),
        current_user: User = Depends(get_current_active_user),
) -> UserResponse:
    """
    Get user by id.
    """
    try:
        user = user_service.get_user(UserId(id=user_id))

        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            type=user.type,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/", response_model=UserResponse)
def create_user(
        user_in: UserCreate,
        user_service: UserService = Depends(get_user_service),
        current_superuser: User = Depends(get_current_active_superuser)
) -> UserResponse:
    """
    Create new user.
    """
    try:
        user = user_service.create_user(obj_in=user_in)

        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            type=user.type,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
    except UserExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except WeakPasswordError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_in: UserExtendedData,
    user_service: UserService = Depends(get_user_service),
    current_superuser: User = Depends(get_current_active_superuser)
) -> Any:
    """
    Update a user.
    """
    try:
        user_update_data = UserUpdate(user_id=user_id, user_data=user_in)
        updated_user = user_service.update_user(userdata=user_update_data)

        return UserResponse(
            id=updated_user.id,
            username=updated_user.username,
            email=updated_user.email,
            is_active=updated_user.is_active,
            type=updated_user.type,
            created_at=updated_user.created_at,
            updated_at=updated_user.updated_at
        )
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
