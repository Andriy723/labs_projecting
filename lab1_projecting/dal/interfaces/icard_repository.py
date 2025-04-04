from abc import ABC, abstractmethod
from typing import List, Optional
from models.card import Card


class ICardRepository(ABC):
    @abstractmethod
    def create(self, card_data: dict) -> Card:
        pass

    @abstractmethod
    def get_by_id(self, card_id: int) -> Optional[Card]:
        pass

    @abstractmethod
    def get_by_account(self, account_id: int) -> List[Card]:
        pass

    @abstractmethod
    def update_details(self, card_id: int, card_data: dict) -> Optional[Card]:
        pass

    @abstractmethod
    def validate(self, card_number: str, expiry_date: str, cvv: str) -> bool:
        pass