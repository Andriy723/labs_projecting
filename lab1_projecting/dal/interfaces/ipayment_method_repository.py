from abc import ABC, abstractmethod
from typing import List, Optional
from models.payment_method import PaymentMethod


class IPaymentMethodRepository(ABC):
    @abstractmethod
    def create(self, payment_method_data: dict) -> PaymentMethod:
        pass

    @abstractmethod
    def get_by_id(self, payment_method_id: int) -> Optional[PaymentMethod]:
        pass

    @abstractmethod
    def get_by_user(self, user_id: int) -> List[PaymentMethod]:
        pass

    @abstractmethod
    def set_as_default(self, payment_method_id: int) -> None:
        pass