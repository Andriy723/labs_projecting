from abc import ABC, abstractmethod
from typing import List, Optional
from models.transaction import Transaction


class ITransactionRepository(ABC):
    @abstractmethod
    def create(self, transaction_data: dict) -> Transaction:
        pass

    @abstractmethod
    def get_by_id(self, transaction_id: int) -> Optional[Transaction]:
        pass

    @abstractmethod
    def get_by_account(self, account_id: int) -> List[Transaction]:
        pass

    @abstractmethod
    def get_by_user(self, user_id: int) -> List[Transaction]:
        pass

    @abstractmethod
    def get_all_by_account(self, account_id: int) -> List[Transaction]:
        pass
