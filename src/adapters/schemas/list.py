from datetime import datetime

from pydantic import BaseModel
from typing import Optional


class ListCreate(BaseModel):
    name: str


class ListUpdate(BaseModel):
    name: Optional[str] = None
    position: Optional[int] = None


class ListNameUpdate(BaseModel):
    name: Optional[str] = None


class ListPositionUpdate(BaseModel):
    position: Optional[int] = None


class ListResponse(BaseModel):
    id: int
    name: str
    position: int
    board_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ListExternalResponse(BaseModel):
    list_detail: ListResponse
    cards: int
