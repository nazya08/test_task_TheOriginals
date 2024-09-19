from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

from src.adapters.schemas.user import UserShortResponse


class CardCreate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    responsible_person_id: Optional[int] = None
    due_date: Optional[datetime] = None
    reminder_datetime: Optional[datetime] = None


class CardUpdate(CardCreate):
    pass


class CardResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    priority: str
    responsible_person_id: int
    list_id: int
    due_date: Optional[datetime] = None
    reminder_datetime: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CardExternalResponse(BaseModel):
    card_detail: CardResponse
    performers: List[UserShortResponse]
    comments_count: int
    attachments_count: int
    checklists_count: int
