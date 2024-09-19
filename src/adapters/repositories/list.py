from typing import Dict, Optional, List as ListType

from src.adapters.repositories.base import SQLAlchemyRepo
from src.adapters.repositories.common.list import ListSaver, ListReader
from src.adapters.sqlalchemy.models import List as ListModel


class ListRepository(SQLAlchemyRepo, ListSaver, ListReader):
    def save_list(self, list: ListModel) -> None:
        self._session.add(list)
        self._session.commit()
        self._session.refresh(list)

    def save_all_lists(self, lists: ListType[ListModel]) -> None:
        self._session.commit()

    def update_list(self, board_id: int, list_id: int, list_data: Dict) -> Optional[ListModel]:
        list = self.get_list_by_id(board_id=board_id, list_id=list_id)
        if list:
            for key, value in list_data.items():
                setattr(list, key, value)
            self._session.commit()
            self._session.refresh(list)
        return list

    def delete_list(self, board_id: int, list_id: int) -> None:
        list_to_delete = self.get_list_by_id(board_id=board_id, list_id=list_id)
        if list_to_delete:
            self._session.delete(list_to_delete)
            self._session.commit()

    def get_lists_by_board(self, board_id: int) -> ListType[ListModel]:
        return self._session.query(ListModel).filter(ListModel.board_id == board_id).order_by(ListModel.position).all()

    def get_list_by_id(self, board_id: int, list_id: int) -> Optional[ListModel]:
        return self._session.query(ListModel).filter(ListModel.board_id == board_id, ListModel.id == list_id).first()

    def get_max_position(self, board_id: int) -> Optional[int]:
        return (
            self._session.query(ListModel.position)
            .filter(ListModel.board_id == board_id)
            .order_by(ListModel.position.desc())
            .first()
        )

    def get_lists_above_position(self, board_id: int, position: int) -> ListType[ListModel]:
        return (
            self._session.query(ListModel)
            .filter(ListModel.board_id == board_id, ListModel.position > position)
            .order_by(ListModel.position)
            .all()
        )
