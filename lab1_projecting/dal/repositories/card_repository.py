from datetime import datetime

from sqlalchemy.orm import Session

from models import Account
from models.card import Card
from typing import List

class CardRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_card(self, card_data: dict) -> Card:
        if not self._validate_card(
                card_data['cardNumber'],
                card_data['expiryDate'],
                card_data['cvv']
        ):
            raise ValueError("Invalid card details")

        card = Card(**card_data)
        self.db.add(card)
        self.db.commit()
        self.db.refresh(card)
        return card

    def _validate_card(self, card_number: str, expiry_date: str, cvv: str) -> bool:
        if not (card_number.isdigit() and len(card_number) in (13, 15, 16)):
            return False

        try:
            month, year = map(int, expiry_date.split('/'))
            current_year = datetime.now().year % 100
            current_month = datetime.now().month

            if year < current_year or (year == current_year and month < current_month):
                return False

            if not (cvv.isdigit() and len(cvv) in (3, 4)):
                return False

            return True
        except:
            return False

    def get_account_cards(self, account_id: int) -> List[Card]:
        return self.db.query(Card).filter(Card.accountID == account_id).all()

    def get_user_cards(self, user_id: int) -> List[Card]:
        return (
            self.db.query(Card)
            .join(Account)
            .filter(Account.userID == user_id)
            .all()
        )

    def __del__(self):
        self.db.close()
