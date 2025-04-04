from fastapi import APIRouter, Depends, HTTPException
from bll.account_service import AccountService
from dal.repositories.account_repository import AccountRepository
from config import get_db


def create_account_router():
    router = APIRouter()

    @router.post("/")
    async def create_account(account_data: dict, db=Depends(get_db)):
        try:
            service = AccountService(AccountRepository(db))
            account = service.create_account(account_data)
            return {"message": "Account created", "account_id": account.accountID}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.get("/user/{user_id}")
    async def get_user_accounts(user_id: int, db=Depends(get_db)):
        service = AccountService(AccountRepository(db))
        accounts = service.get_user_accounts(user_id)
        return {"accounts": [{
            "id": acc.accountID,
            "number": acc.accountNumber,
            "balance": acc.balance,
            "currency": acc.currency
        } for acc in accounts]}

    @router.post("/transfer")
    async def transfer_funds(transfer_data: dict, db=Depends(get_db)):
        try:
            service = AccountService(AccountRepository(db))
            success = service.transfer_funds(
                transfer_data['from_account_id'],
                transfer_data['to_account_id'],
                transfer_data['amount']
            )
            return {"message": "Transfer successful", "success": success}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    return router