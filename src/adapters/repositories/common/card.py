from abc import abstractmethod
from typing import Protocol, List, Optional

from src.adapters.sqlalchemy.models import Card, Comment, CardAttachment, CheckList, CardActivity


class CardSaver(Protocol):
    @abstractmethod
    def save_card(self, card: Card) -> None:
        raise NotImplementedError

    @abstractmethod
    def create_card(self, card: Card) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_card(self, list_id: int, card_id: int, card_data: dict) -> Optional[Card]:
        raise NotImplementedError

    @abstractmethod
    def delete_card(self, list_id: int, card_id: int) -> None:
        raise NotImplementedError


class CardReader(Protocol):
    @abstractmethod
    def get_cards(self, list_id: int) -> List[Card]:
        raise NotImplementedError

    @abstractmethod
    def get_card(self, list_id: int, card_id: int) -> Optional[Card]:
        raise NotImplementedError


class CommentSaver(Protocol):
    @abstractmethod
    def save_comment(self, comment: Comment) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_comment(self, comment_id: int, comment_data: dict) -> Optional[Comment]:
        raise NotImplementedError

    @abstractmethod
    def delete_comment(self, comment_id: int) -> None:
        raise NotImplementedError


class CommentReader(Protocol):
    @abstractmethod
    def get_comments(self, card_id: int) -> List[Comment]:
        raise NotImplementedError

    @abstractmethod
    def get_comment(self, comment_id: int) -> Optional[Comment]:
        raise NotImplementedError


class CardAttachmentSaver(Protocol):
    @abstractmethod
    def save_card_attachment(self, attachment: CardAttachment) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_card_attachment(self, attachment_id: int) -> None:
        raise NotImplementedError


class CardAttachmentReader(Protocol):
    @abstractmethod
    def get_card_attachments(self, card_id: int) -> List[CardAttachment]:
        raise NotImplementedError

    @abstractmethod
    def get_card_attachment(self, attachment_id: int) -> Optional[CardAttachment]:
        raise NotImplementedError


class CheckListSaver(Protocol):
    @abstractmethod
    def save_checklist(self, checklist: CheckList) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_checklist(self, checklist_id: int, checklist_data: dict) -> Optional[CheckList]:
        raise NotImplementedError

    @abstractmethod
    def delete_checklist(self, checklist_id: int) -> None:
        raise NotImplementedError


class CheckListReader(Protocol):
    @abstractmethod
    def get_checklists(self, card_id: int) -> List[CheckList]:
        raise NotImplementedError

    @abstractmethod
    def get_checklist(self, checklist_id: int) -> Optional[CheckList]:
        raise NotImplementedError


class CardActivitySaver(Protocol):
    @abstractmethod
    def save_card_activity(self, activity: CardActivity) -> None:
        raise NotImplementedError


class CardActivityReader(Protocol):
    @abstractmethod
    def get_card_activities(self, card_id: int) -> List[CardActivity]:
        raise NotImplementedError

    @abstractmethod
    def get_card_activity(self, activity_id: int) -> Optional[CardActivity]:
        raise NotImplementedError
