from sqlalchemy.orm import Session
from dal.interfaces.itransaction_repository import ITransactionRepository
from models import Account
from models.transaction import Transaction
from config import SessionLocal
from typing import Optional, List


class TransactionRepository(ITransactionRepository):
    def __init__(self, db: Session = None):
        self.db = db or SessionLocal()

    def create(self, transaction_data: dict) -> Transaction:
        transaction = Transaction(**transaction_data)
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction

    def get_by_id(self, transaction_id: int) -> Optional[Transaction]:
        return self.db.query(Transaction).filter(Transaction.id == transaction_id).first()

    def get_by_account(self, account_id: int) -> List[Transaction]:
        return self.db.query(Transaction).filter(Transaction.accountID == account_id).all()

    def get_by_user(self, user_id: int) -> List[Transaction]:
        return self.db.query(Transaction).join(Account).filter(Account.userID == user_id).all()

    def __del__(self):
        self.db.close()