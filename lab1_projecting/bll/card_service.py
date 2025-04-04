from typing import List, Optional
from dal.interfaces.icard_repository import ICardRepository
from models.card import Card


class CardService:
    def __init__(self, card_repo: ICardRepository):
        self._card_repo = card_repo

    def add_card(self, card_data: dict) -> Card:
        if not self._card_repo.validate(
                card_data['cardNumber'],
                card_data['expiryDate'],
                card_data['cvv']
        ):
            raise ValueError("Invalid card details")
        return self._card_repo.create(card_data)

    def get_account_cards(self, account_id: int) -> List[Card]:
        return self._card_repo.get_by_account(account_id)

    def update_card(self, card_id: int, card_data: dict) -> Optional[Card]:
        return self._card_repo.update_details(card_id, card_data)

    def validate_card(self, card_number: str, expiry_date: str, cvv: str) -> bool:
        return self._card_repo.validate(card_number, expiry_date, cvv)