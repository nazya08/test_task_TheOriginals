from enum import Enum as PyEnum

from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship

from src.adapters.sqlalchemy.db.base_class import Base
from src.adapters.sqlalchemy.models.base import TimestampedModel
from src.adapters.sqlalchemy.models.board import board_members_association
from src.adapters.sqlalchemy.models.card import task_performers_association


class UserType(PyEnum):
    default_user = "default_user"
    admin = "admin"


class User(Base, TimestampedModel):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    type = Column(Enum(UserType), default=UserType.default_user)
    is_active = Column(Boolean, default=True)

    boards_owner = relationship("Board", back_populates="owner")
    boards = relationship("Board", secondary=board_members_association, back_populates="members")
    cards_responsible = relationship("Card", back_populates="responsible")
    perform_cards = relationship("Card", secondary=task_performers_association, back_populates="performers")
    comments = relationship("Comment", back_populates="author")
    card_activities = relationship("CardActivity", back_populates="performed_by")
