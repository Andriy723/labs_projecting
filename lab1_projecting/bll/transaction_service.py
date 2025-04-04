from typing import List, Optional
from dal.interfaces.itransaction_repository import ITransactionRepository
from models.transaction import Transaction


class TransactionService:
    def __init__(self, transaction_repo: ITransactionRepository):
        self._transaction_repo = transaction_repo

    def create_transaction(self, transaction_data: dict) -> Transaction:
        return self._transaction_repo.create(transaction_data)

    def get_account_transactions(self, account_id: int) -> List[Transaction]:
        return self._transaction_repo.get_by_account(account_id)

    def get_user_transactions(self, user_id: int) -> List[Transaction]:
        return self._transaction_repo.get_by_user(user_id)

    def get_transaction_details(self, transaction_id: int) -> Optional[Transaction]:
        return self._transaction_repo.get_by_id(transaction_id)