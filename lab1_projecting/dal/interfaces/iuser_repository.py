from abc import ABC, abstractmethod
from typing import Optional
from models.user import User


class IUserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def create_user(self, user_data: dict) -> User:
        pass

    @abstractmethod
    def update_user(self, user: User) -> None:
        pass