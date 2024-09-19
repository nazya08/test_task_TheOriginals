from datetime import datetime

from pydantic import BaseModel
from typing import Optional

from src.adapters.schemas.user import UserExtendedData


class BoardCreate(BaseModel):
    name: str
    is_public: bool


class BoardUpdate(BaseModel):
    name: Optional[str]
    is_public: Optional[bool]


class BoardResponse(BaseModel):
    id: int
    name: str
    is_public: bool
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BoardExternalResponse(BaseModel):
    board_detail: BoardResponse
    lists: int
    members: int


class BoardMember(BaseModel):
    board_id: int
    member_id: int
    member_data: UserExtendedData
