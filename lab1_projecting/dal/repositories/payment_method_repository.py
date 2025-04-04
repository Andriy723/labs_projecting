from sqlalchemy.orm import Session
from dal.interfaces.ipayment_method_repository import IPaymentMethodRepository
from models.payment_method import PaymentMethod
from config import SessionLocal
from typing import Optional, List


class PaymentMethodRepository(IPaymentMethodRepository):
    def __init__(self, db: Session = None):
        self.db = db or SessionLocal()

    def create(self, payment_method_data: dict) -> PaymentMethod:
        payment_method = PaymentMethod(**payment_method_data)
        self.db.add(payment_method)
        self.db.commit()
        self.db.refresh(payment_method)
        return payment_method

    def get_by_id(self, payment_method_id: int) -> Optional[PaymentMethod]:
        return self.db.query(PaymentMethod).filter(PaymentMethod.id == payment_method_id).first()

    def get_by_user(self, user_id: int) -> List[PaymentMethod]:
        return self.db.query(PaymentMethod).filter(PaymentMethod.userID == user_id).all()

    def set_as_default(self, payment_method_id: int) -> None:
        payment_method = self.get_by_id(payment_method_id)
        if payment_method:
            self.db.query(PaymentMethod).filter(
                PaymentMethod.userID == payment_method.userID
            ).update({"isDefault": False})

            payment_method.isDefault = True
            self.db.commit()

    def __del__(self):
        self.db.close()