from typing import List, Optional
from dal.interfaces.iaccount_repository import IAccountRepository
from models.account import Account


class AccountService:
    def __init__(self, account_repository: IAccountRepository):
        self._account_repository = account_repository

    def create_account(self, user_id: int, currency: str = "UAH") -> Account:
        if not user_id:
            raise ValueError("User ID is required")
        if currency not in ["UAH", "USD", "EUR"]:
            raise ValueError("Invalid currency")

        return self._account_repository.create_account(user_id, currency)

    def get_user_accounts(self, user_id: int) -> List[Account]:
        if not user_id:
            raise ValueError("User ID is required")
        return self._account_repository.get_user_accounts(user_id)

    def transfer_funds(self, from_account_id: int, to_account_id: int, amount: float) -> bool:
        if amount <= 0:
            raise ValueError("Amount must be positive")

        from_account = self._account_repository.get_account_by_id(from_account_id)
        to_account = self._account_repository.get_account_by_id(to_account_id)

        if not from_account or not to_account:
            raise ValueError("One or both accounts not found")

        if from_account.currency != to_account.currency:
            raise ValueError("Cannot transfer between different currencies")

        if from_account.balance < amount:
            raise ValueError("Insufficient funds")

        try:
            self._account_repository.update_balance(from_account_id, -amount)
            self._account_repository.update_balance(to_account_id, amount)
            return True
        except Exception as e:
            raise ValueError(f"Transfer failed: {str(e)}")