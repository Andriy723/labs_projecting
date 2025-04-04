from fastapi import APIRouter, Depends, HTTPException
from bll.transaction_service import TransactionService
from dal.repositories.transaction_repository import TransactionRepository
from config import get_db


def create_transaction_router():
    router = APIRouter()

    @router.post("/")
    async def create_transaction(transaction_data: dict, db=Depends(get_db)):
        service = TransactionService(TransactionRepository(db))
        try:
            transaction = service.create_transaction(transaction_data)
            return {"message": "Transaction created", "id": transaction.id}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.get("/account/{account_id}")
    async def get_account_transactions(account_id: int, db=Depends(get_db)):
        service = TransactionService(TransactionRepository(db))
        transactions = service.get_account_transactions(account_id)
        return {"transactions": transactions}

    @router.get("/user/{user_id}")
    async def get_user_transactions(user_id: int, db=Depends(get_db)):
        service = TransactionService(TransactionRepository(db))
        transactions = service.get_user_transactions(user_id)
        return {"transactions": transactions}

    @router.get("/{transaction_id}")
    async def get_transaction(transaction_id: int, db=Depends(get_db)):
        service = TransactionService(TransactionRepository(db))
        transaction = service.get_transaction_details(transaction_id)
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return transaction

    return router