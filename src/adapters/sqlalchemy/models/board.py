from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship

from src.adapters.sqlalchemy.db.base_class import Base
from src.adapters.sqlalchemy.models.base import TimestampedModel

board_members_association = Table(
    'board_members_association', Base.metadata,
    Column('board_id', Integer, ForeignKey('board.id')),
    Column('user_id', Integer, ForeignKey('user.id'))
)


class Board(Base, TimestampedModel):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    is_public = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    owner = relationship("User", back_populates="boards")
    lists = relationship("List", back_populates="board", cascade="all, delete-orphan")
    members = relationship("User", secondary=board_members_association, back_populates="boards")
