from typing import List

from fastapi import Depends, HTTPException, status
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from src.adapters.repositories.user import UserRepository
from src.adapters.schemas.token import TokenPayload
from src.adapters.sqlalchemy.models import User
from src.adapters.sqlalchemy.models.user import UserType
from src.main.security import decode_access_token
from src.presentation.api.auth_bearer import JWTBearer
from src.presentation.dependencies.base import get_db
from src.application.user.user_service import UserService

jwt_bearer = JWTBearer()


def get_user_repo(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(session=db)


def get_user_service(user_repo: UserRepository = Depends(get_user_repo)) -> UserService:
    return UserService(user_repo=user_repo)


def get_user(user_id: int, user_repo: UserRepository = Depends(get_user_repo)):
    user = user_repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


def get_current_user(
        token: str = Depends(jwt_bearer),
        user_db_gateway: UserRepository = Depends(get_user_repo)
) -> User:
    try:
        payload = decode_access_token(token)
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = user_db_gateway.get_user_by_id(id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
        current_user: User = Depends(get_current_user),
        user_service: UserService = Depends(get_user_service)
) -> User:
    if not user_service.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
        current_user: User = Depends(get_current_user),
        user_service: UserService = Depends(get_user_service)
) -> User:
    if not user_service.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user


class PermissionChecker:
    def __init__(self, allowed_roles: List[UserType]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)):
        if current_user.type not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access forbidden",
            )
        return current_user
