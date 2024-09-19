from typing import List as ListType

from fastapi import HTTPException

from src.adapters.repositories.list import ListRepository
from src.adapters.schemas.list import ListCreate, ListUpdate
from src.adapters.sqlalchemy.models import List as ListModel, User, Board


class ListService:
    def __init__(self, list_repo: ListRepository) -> None:
        self.list_repo = list_repo

    def get_lists_by_board(self, board_id: int) -> ListType[ListModel]:
        return self.list_repo.get_lists_by_board(board_id=board_id)

    def create_list(self, board: Board, obj_in: ListCreate, current_user: User) -> ListModel:
        if not current_user:
            raise HTTPException(status_code=400, detail="Invalid current user")

        if board.owner_id != current_user.id:
            raise HTTPException(
                status_code=403, detail="You do not have permission to perform this action"
            )
        max_position_row = self.list_repo.get_max_position(board.id)
        max_position = max_position_row[0] if max_position_row else 0
        new_position = max_position + 1

        list_data = obj_in.dict()
        list_data["board_id"] = board.id

        list_db_obj = ListModel(position=new_position, **list_data)

        self.list_repo.save_list(list_db_obj)

        return list_db_obj

    def update_list(self, board: Board, list: ListModel, obj_in: ListUpdate, current_user: User) -> ListModel:
        if board.owner_id != current_user.id:
            raise HTTPException(
                status_code=403, detail="You do not have permission to perform this action"
            )

        if obj_in.name is not None:
            list.name = obj_in.name

        if obj_in.position is not None:
            new_position = obj_in.position
            lists = self.list_repo.get_lists_by_board(board_id=board.id)

            # Зміна позицій всіх списків, якщо нова позиція відрізняється
            if new_position != list.position:
                # Пересунути всі списки вниз або вверх в залежності від нової позиції
                if new_position < list.position:
                    # Перемістити всі списки вниз, якщо нова позиція менша
                    for lst in lists:
                        if new_position <= lst.position < list.position:
                            lst.position += 1
                elif new_position > list.position:
                    # Перемістити всі списки вверх, якщо нова позиція більша
                    for lst in lists:
                        if list.position < lst.position <= new_position:
                            lst.position -= 1

                list.position = new_position

                self.list_repo.save_all_lists(lists)

        self.list_repo.save_list(list)

        return list

    def delete_list(self, board: Board, list: ListModel, current_user: User) -> None:
        if board.owner_id != current_user.id:
            raise HTTPException(
                status_code=403, detail="You do not have permission to perform this action"
            )

        self.list_repo.delete_list(board_id=board.id, list_id=list.id)

        # Оновити позиції інших списків
        lists_to_update = self.list_repo.get_lists_above_position(board_id=board.id, position=list.position)
        for lst in lists_to_update:
            lst.position -= 1

        self.list_repo.save_all_lists(lists_to_update)
