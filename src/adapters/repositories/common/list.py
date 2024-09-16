from abc import abstractmethod
from typing import Protocol, List as ListType, Optional

from src.adapters.sqlalchemy.models import List


class ListSaver(Protocol):
    @abstractmethod
    def create_list(self, board_id: int, list_data: dict) -> List:
        """Створює новий список для певної дошки."""
        raise NotImplementedError

    @abstractmethod
    def update_board_list(self, list_id: int, list_data: dict) -> Optional[List]:
        """Оновлює список за його ID та переданими даними."""
        raise NotImplementedError

    @abstractmethod
    def delete_board_list(self, list_id: int) -> None:
        """Видаляє список за його ID."""
        raise NotImplementedError


class ListReader(Protocol):
    @abstractmethod
    def get_board_lists(self, board_id: int, skip: int = 0, limit: int = 10) -> ListType[List]:
        """Отримує всі списки для дошки за її ID з пагінацією."""
        raise NotImplementedError

    @abstractmethod
    def get_board_list(self, board_id: int, list_id: int) -> Optional[List]:
        """Отримує конкретний список дошки за ID дошки та ID списку."""
        raise NotImplementedError
