from typing import List, Optional
from dal.interfaces.iaccount_repository import IAccountRepository
from models.account import Account


class AccountService:
    def __init__(self, account_repository: IAccountRepository):
        self._account_repository = account_repository

    def create_account(self, account_data: dict) -> Account:
        if self._account_repository.get_by_number(account_data['accountNumber']):
            raise ValueError("Account with this number already exists")
        return self._account_repository.create(account_data)

    def get_user_accounts(self, user_id: int) -> List[Account]:
        return self._account_repository.get_by_user_id(user_id)

    def transfer_funds(self, from_account_id: int, to_account_id: int, amount: float) -> bool:
        if amount <= 0:
            raise ValueError("Amount must be positive")

        from_account = self._account_repository.get_by_id(from_account_id)
        to_account = self._account_repository.get_by_id(to_account_id)

        if not from_account or not to_account:
            raise ValueError("One or both accounts not found")

        if from_account.balance < amount:
            raise ValueError("Insufficient funds")

        try:
            self._account_repository.update_balance(from_account_id, -amount)
            self._account_repository.update_balance(to_account_id, amount)
            return True
        except Exception as e:
            raise ValueError(f"Transfer failed: {str(e)}")