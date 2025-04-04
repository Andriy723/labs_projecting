from sqlalchemy.orm import Session
from dal.interfaces.icard_repository import ICardRepository
from models.card import Card
from datetime import datetime
from config import SessionLocal
from typing import Optional, List


class CardRepository(ICardRepository):
    def __init__(self, db: Session = None):
        self.db = db or SessionLocal()

    def create(self, card_data: dict) -> Card:
        card = Card(**card_data)
        self.db.add(card)
        self.db.commit()
        self.db.refresh(card)
        return card

    def get_by_id(self, card_id: int) -> Optional[Card]:
        return self.db.query(Card).filter(Card.id == card_id).first()

    def get_by_account(self, account_id: int) -> List[Card]:
        return self.db.query(Card).filter(Card.accountID == account_id).all()

    def update_details(self, card_id: int, card_data: dict) -> Optional[Card]:
        card = self.get_by_id(card_id)
        if card:
            for key, value in card_data.items():
                setattr(card, key, value)
            self.db.commit()
            self.db.refresh(card)
        return card

    def validate(self, card_number: str, expiry_date: str, cvv: str) -> bool:
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

    def __del__(self):
        self.db.close()