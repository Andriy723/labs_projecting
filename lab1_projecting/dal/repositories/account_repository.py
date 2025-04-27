from sqlalchemy.orm import Session
from models.account import Account
from typing import List
import time

class AccountRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_account(self, user_id: int, currency: str) -> Account:
        account_number = f"UA{user_id:08d}{int(time.time()) % 10000:04d}"
        account = Account(
            accountNumber=account_number,
            balance=0.0,
            currency=currency,
            userID=user_id
        )
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account

    def get_user_accounts(self, user_id: int) -> List[Account]:
        return self.db.query(Account).filter(Account.userID == user_id).all()

    def get_account_by_id(self, account_id: int) -> Account:
        return self.db.query(Account).filter(Account.accountID == account_id).first()

    def update_balance(self, account_id: int, amount: float) -> None:
        account = self.get_account_by_id(account_id)
        if account:
            account.balance += amount
            self.db.commit()

    def __del__(self):
        self.db.close()