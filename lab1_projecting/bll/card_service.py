from typing import List, Optional
from dal.interfaces.icard_repository import ICardRepository
from models.card import Card


class CardService:
    def __init__(self, card_repo: ICardRepository):
        self._card_repo = card_repo

    def add_card(self, card_data: dict) -> Card:
        return self._card_repo.create_card(card_data)

    def validate_card_details(self, card_number: str, expiry_date: str, cvv: str) -> bool:
        return self._card_repo._validate_card(card_number, expiry_date, cvv)

    def get_account_cards(self, account_id: int) -> List[Card]:
        return self._card_repo.get_by_account(account_id)

    def update_card(self, card_id: int, card_data: dict) -> Optional[Card]:
        return self._card_repo.update_details(card_id, card_data)

    def validate_card(self, card_number: str, expiry_date: str, cvv: str) -> bool:
        return self._card_repo.validate(card_number, expiry_date, cvv)

    def get_cards_by_user(self, user_id: int) -> List[Card]:
        return self._card_repo.get_by_user(user_id)

    def get_user_cards(self, user_id: int) -> List[Card]:
        return self._card_repo.get_user_cards(user_id)