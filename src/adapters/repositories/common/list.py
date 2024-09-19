from abc import abstractmethod
from typing import Protocol, List as ListType, Optional

from src.adapters.sqlalchemy.models import List as ListModel


class ListSaver(Protocol):
    @abstractmethod
    def save_list(self, list: ListModel) -> None:
        """Зберігає список в базі даних."""
        raise NotImplementedError

    @abstractmethod
    def save_all_lists(self, lists: ListType[ListModel]) -> None:
        """Зберігає списки в базі даних."""
        raise NotImplementedError

    @abstractmethod
    def update_list(self, board_id: int, list_id: int, list_data: dict) -> Optional[ListModel]:
        """Оновлює список за його ID та переданими даними."""
        raise NotImplementedError

    @abstractmethod
    def delete_list(self, board_id: int, list_id: int) -> None:
        """Видаляє список за його ID."""
        raise NotImplementedError


class ListReader(Protocol):
    @abstractmethod
    def get_lists_by_board(self, board_id: int) -> ListType[ListModel]:
        """Отримує всі списки для дошки за її ID з пагінацією."""
        raise NotImplementedError

    @abstractmethod
    def get_list_by_id(self, board_id: int, list_id: int) -> Optional[ListModel]:
        """Отримує конкретний список дошки за ID дошки та ID списку."""
        raise NotImplementedError
