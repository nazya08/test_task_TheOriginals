from typing import List

from sqlalchemy.exc import IntegrityError

from src.adapters.repositories.base import SQLAlchemyRepo
from src.adapters.repositories.common.user import UserReader, UsersReader, UserSaver
from src.adapters.sqlalchemy.models.user import User


class UserRepository(SQLAlchemyRepo, UserReader, UsersReader, UserSaver):
    def save_user(self, user: User) -> None:
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)

    def update_user(self, user_id: int, update_data: dict) -> User:
        user = self.get_user_by_id(user_id)
        for key, value in update_data.items():
            setattr(user, key, value)
        try:
            self._session.commit()
            self._session.refresh(user)
        except IntegrityError as err:
            self._session.rollback()

        return user

    def get_user_by_id(self, id: int) -> User:
        return self._session.query(User).filter(User.id == id).first()

    def get_user_by_username(self, username: str) -> User:
        return self._session.query(User).filter(User.username == username).first()

    def get_user_by_email(self, email: str) -> User:
        return self._session.query(User).filter(User.email == email).first()

    def get_users_list(self, skip: int, limit: int) -> List[User]:
        return self._session.query(User).offset(skip).limit(limit).all()

    def get_users_count(self) -> int:
        return self._session.query(User).count()
