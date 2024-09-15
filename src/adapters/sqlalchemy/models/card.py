from datetime import datetime

from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

from src.adapters.sqlalchemy.db.base_class import Base
from src.adapters.sqlalchemy.models.base import TimestampedModel


task_performers_association = Table(
    'task_performers_association', Base.metadata,
    Column('card_id', ForeignKey('card.id'), primary_key=True),
    Column('user_id', ForeignKey('user.id'), primary_key=True)
)


class Priority(PyEnum):
    low = "Low"
    medium = "Medium"
    high = "High"


class Card(Base, TimestampedModel):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    priority = Column(Enum(Priority), default=Priority.medium)
    responsible_person_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    list_id = Column(Integer, ForeignKey('list.id'), nullable=False)

    due_date = Column(DateTime, nullable=True)
    reminder_datetime = Column(DateTime, nullable=True)

    list = relationship("List", back_populates="cards")
    responsible = relationship('User', back_populates='tasks_responsible')
    performers = relationship('User', secondary=task_performers_association, back_populates="perform_tasks")
    comments = relationship("CardComment", back_populates="card", cascade="all, delete-orphan")
    attachments = relationship("CardAttachment", back_populates="card", cascade="all, delete-orphan")
    activities = relationship("CardActivity", back_populates="card", cascade="all, delete-orphan")


class CardComment(Base, TimestampedModel):
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    card_id = Column(Integer, ForeignKey('card.id'), nullable=False)

    author = relationship("User", back_populates="comments")
    card = relationship("Card", back_populates="comments")


class CardAttachment(Base, TimestampedModel):
    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, nullable=False)
    card_id = Column(Integer, ForeignKey('card.id'), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    card = relationship("Card", back_populates="attachments")


class ActionType(PyEnum):
    created = "Created"
    updated = "Updated"
    status_changed = "Status Changed"
    comment_added = "Comment Added"
    assigned = "Assigned"


class CardActivity(Base, TimestampedModel):
    id = Column(Integer, primary_key=True, index=True)
    action_type = Column(Enum(ActionType), nullable=False)
    description = Column(String, nullable=False)
    performed_by_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    card_id = Column(Integer, ForeignKey('card.id'), nullable=False)
    performed_at = Column(DateTime, default=datetime.utcnow)

    performed_by = relationship("User", back_populates="card_activities")
    card = relationship("Card", back_populates="activities")
