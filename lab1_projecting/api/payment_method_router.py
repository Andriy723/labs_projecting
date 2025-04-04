from fastapi import APIRouter, Depends, HTTPException
from bll.payment_method_service import PaymentMethodService
from dal.repositories.payment_method_repository import PaymentMethodRepository
from config import get_db


def create_payment_method_router():
    router = APIRouter()

    @router.post("/")
    async def add_payment_method(payment_method_data: dict, db=Depends(get_db)):
        service = PaymentMethodService(PaymentMethodRepository(db))
        try:
            method = service.add_payment_method(payment_method_data)
            return {"message": "Payment method added", "id": method.id}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.get("/user/{user_id}")
    async def get_user_methods(user_id: int, db=Depends(get_db)):
        service = PaymentMethodService(PaymentMethodRepository(db))
        methods = service.get_user_payment_methods(user_id)
        return {"payment_methods": methods}

    @router.post("/{method_id}/set-default")
    async def set_default_method(method_id: int, db=Depends(get_db)):
        service = PaymentMethodService(PaymentMethodRepository(db))
        try:
            service.set_default_payment_method(method_id)
            return {"message": "Payment method set as default"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    return router