import re

from typing import Union, Optional, List

from src.adapters.repositories.user import UserRepository
from src.adapters.schemas.pagination import Pagination
from src.adapters.schemas.user import UserCreate, UserSignUp, UserId, UserUpdate
from src.adapters.sqlalchemy.models import User
from src.adapters.sqlalchemy.models.user import UserType
from src.application.common.exceptions import UserExistsError, UserNotFoundError, WeakPasswordError
from src.main.security import get_password_hash, verify_password


class UserService:

    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    def create_user(self, obj_in: Union[UserCreate, UserSignUp]) -> User:
        user_data = obj_in.dict()

        if self.user_repo.get_user_by_username(user_data['username']):
            raise UserExistsError("User with this username already exists.")

        if self.user_repo.get_user_by_email(user_data['email']):
            raise UserExistsError("User with this email already exists.")

        password = user_data.pop("password")
        response, msg = self.validate_password(password)
        if not response:
            raise WeakPasswordError(msg)

        user_data["hashed_password"] = get_password_hash(password)
        user = User(**user_data)

        self.user_repo.save_user(user)

        return user

    def update_user(self, userdata: UserUpdate) -> User:
        if not self.user_repo.get_user_by_id(userdata.user_id):
            raise UserNotFoundError("User not found.")

        if self.user_repo.get_user_by_username(userdata.user_data.username):
            raise UserExistsError("User with this username already exists.")

        if self.user_repo.get_user_by_email(userdata.user_data.email):
            raise UserExistsError("User with this email already exists.")

        update_data = userdata.user_data.dict(exclude_unset=True)
        updated_user = self.user_repo.update_user(user_id=userdata.user_id, update_data=update_data)

        return updated_user

    def get_users_list(self, data: Pagination) -> List[User]:
        return self.user_repo.get_users_list(skip=data.skip, limit=data.limit)

    def get_users_total(self) -> int:
        return self.user_repo.get_users_count()

    def get_user(self, data: UserId) -> User:
        user = self.user_repo.get_user_by_id(data.id)
        if not user:
            raise UserNotFoundError("User not found.")

        return user

    def sign_up(self, obj_in: UserSignUp) -> Optional[User]:
        user = self.create_user(obj_in)

        return user

    def authenticate(self, email: str, password: str) -> Optional[User]:
        user = self.user_repo.get_user_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.type == UserType.admin

    def validate_password(self, password: str) -> tuple[bool, str]:  # TODO: relocate to another file
        if not re.search(r"\d", password):
            return False, "Password must contain at least one digit."
        if not re.search(r"[a-z]", password):
            return (
                False,
                "Password must contain at least one lowercase letter.",
            )
        if not re.search(r"[A-Z]", password):
            return (
                False,
                "Password must contain at least one uppercase letter.",
            )

        return True, "Password is valid"
