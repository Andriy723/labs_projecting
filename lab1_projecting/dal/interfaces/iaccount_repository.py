from abc import ABC, abstractmethod
from typing import List, Optional
from models.account import Account


class IAccountRepository(ABC):
    @abstractmethod
    def get_by_id(self, account_id: int) -> Optional[Account]:
        pass

    @abstractmethod
    def get_by_number(self, account_number: str) -> Optional[Account]:
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> List[Account]:
        pass

    @abstractmethod
    def create(self, account_data: dict) -> Account:
        pass

    @abstractmethod
    def update_balance(self, account_id: int, amount: float) -> None:
        pass