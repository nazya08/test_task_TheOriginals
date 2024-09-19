from typing import List, Optional

from src.adapters.repositories.base import SQLAlchemyRepo
from src.adapters.repositories.common.card import CardSaver, CardReader
from src.adapters.sqlalchemy.models.card import Card


class CardRepository(SQLAlchemyRepo, CardSaver, CardReader):
    def save_card(self, card: Card) -> None:
        self._session.commit()
        self._session.refresh(card)

    def create_card(self, card: Card) -> None:
        self._session.add(card)
        self.save_card(card)

    def update_card(self, list_id: int, card_id: int, card_data: dict) -> Card:
        card = self.get_card(list_id=list_id, card_id=card_id)
        if card:
            for key, value in card_data.items():
                setattr(card, key, value)
            self._session.commit()
            self._session.refresh(card)
        return card

    def delete_card(self, list_id: int, card_id: int) -> None:
        card = self.get_card(list_id=list_id, card_id=card_id)
        if card:
            self._session.delete(card)
            self._session.commit()

    def get_card(self, list_id: int, card_id: int) -> Optional[Card]:
        return (
            self._session.query(Card)
            .filter(Card.list_id == list_id, Card.id == card_id)
            .first()
        )

    def get_cards(self, list_id: Optional[int] = None) -> List[Card]:
        query = self._session.query(Card)
        if list_id is not None:
            query = query.filter(Card.list_id == list_id)
        return query.all()
