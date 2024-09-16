from abc import abstractmethod
from typing import Protocol, List, Optional

from src.adapters.sqlalchemy.models import Board


class BoardSaver(Protocol):
    @abstractmethod
    def save_board(self, board: Board) -> None:
        """Зберігає дошку в базі даних."""
        raise NotImplementedError

    @abstractmethod
    def update_board(self, board_id: int, board_data: dict) -> Optional[Board]:
        """Оновлює дані дошки за її ID."""
        raise NotImplementedError

    @abstractmethod
    def delete_board(self, board_id: int) -> None:
        """Видаляє дошку за її ID."""
        raise NotImplementedError

    @abstractmethod
    def add_member_to_board(self, board_id: int, member_id: int) -> Optional[Board]:
        """Додає користувача до дошки за ID дошки та ID користувача."""
        raise NotImplementedError

    @abstractmethod
    def remove_member_from_board(self, board_id: int, member_id: int) -> Optional[Board]:
        """Видаляє користувача з дошки за ID дошки та ID користувача."""
        raise NotImplementedError


class BoardReader(Protocol):
    @abstractmethod
    def get_board_by_id(self, board_id: int) -> Optional[Board]:
        """Отримує дошку за її ID."""
        raise NotImplementedError

    @abstractmethod
    def get_user_board(self, user_id: int, board_id: int) -> Optional[Board]:  # /boards/me/{board_id}
        """Отримує конкретну дошку користувача за ID користувача та ID дошки."""
        raise NotImplementedError

    @abstractmethod
    def get_board_member_by_id(self, board_id: int, member_id: int) -> Optional[Board]:
        """Отримує конкретного учасника дошки за ID дошки та ID учасника."""
        raise NotImplementedError

    @abstractmethod
    def get_board_members(self, board_id: int) -> List[int]:
        """Отримує всіх учасників дошки за її ID."""
        raise NotImplementedError


class BoardsReader(Protocol):
    @abstractmethod
    def get_user_boards(self, user_id: int, skip: int = 0, limit: int = 10) -> List[Board]:  # /boards/me
        """Отримує всі дошки користувача за його ID."""
        raise NotImplementedError

    @abstractmethod
    def get_boards_list(self, skip: int = 0, limit: int = 10) -> List[Board]:  # /boards/public
        """Отримує список всіх публічних дошок."""
        raise NotImplementedError
