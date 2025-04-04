from typing import List, Optional
from dal.interfaces.ipayment_method_repository import IPaymentMethodRepository
from models.payment_method import PaymentMethod


class PaymentMethodService:
    def __init__(self, payment_method_repo: IPaymentMethodRepository):
        self._payment_method_repo = payment_method_repo

    def add_payment_method(self, payment_method_data: dict) -> PaymentMethod:
        return self._payment_method_repo.create(payment_method_data)

    def get_user_payment_methods(self, user_id: int) -> List[PaymentMethod]:
        return self._payment_method_repo.get_by_user(user_id)

    def get_payment_method(self, payment_method_id: int) -> Optional[PaymentMethod]:
        return self._payment_method_repo.get_by_id(payment_method_id)

    def set_default_payment_method(self, payment_method_id: int) -> None:
        self._payment_method_repo.set_as_default(payment_method_id)