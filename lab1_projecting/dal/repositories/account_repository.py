from sqlalchemy.orm import Session
from dal.interfaces.iaccount_repository import IAccountRepository
from models.account import Account
from config import SessionLocal
from typing import Optional, List


class AccountRepository(IAccountRepository):
    def __init__(self, db: Session = None):
        self.db = db or SessionLocal()

    def get_by_id(self, account_id: int) -> Optional[Account]:
        return self.db.query(Account).filter(Account.accountID == account_id).first()

    def get_by_number(self, account_number: str) -> Optional[Account]:
        return self.db.query(Account).filter(Account.accountNumber == account_number).first()

    def get_by_user_id(self, user_id: int) -> List[Account]:
        return self.db.query(Account).filter(Account.userID == user_id).all()

    def create(self, account_data: dict) -> Account:
        account = Account(**account_data)
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account

    def update_balance(self, account_id: int, amount: float) -> None:
        account = self.get_by_id(account_id)
        if account:
            account.balance += amount
            self.db.commit()

    def __del__(self):
        self.db.close()