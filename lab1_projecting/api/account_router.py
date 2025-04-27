from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from config import get_db
from bll.account_service import AccountService
from dal.repositories.account_repository import AccountRepository
from models import Card

class AccountCreate(BaseModel):
    user_id: int
    currency: str = "UAH"

class AccountResponse(BaseModel):
    id: int
    number: str
    balance: float
    currency: str

class TransferRequest(BaseModel):
    from_account_id: int
    to_account_id: int
    amount: float

def create_account_router():
    router = APIRouter()

    @router.post("/", response_model=dict)
    async def create_account(account_data: AccountCreate, db: Session = Depends(get_db)):
        service = AccountService(AccountRepository(db))
        try:
            account = service.create_account(
                user_id=account_data.user_id,
                currency=account_data.currency
            )
            return {
                "message": "Account created successfully",
                "account_id": account.accountID,
                "account_number": account.accountNumber
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.get("/user/{user_id}", response_model=List[AccountResponse])
    async def get_user_accounts(user_id: int, db: Session = Depends(get_db)):
        service = AccountService(AccountRepository(db))
        accounts = service.get_user_accounts(user_id)
        return [
            {
                "id": acc.accountID,
                "number": acc.accountNumber,
                "balance": acc.balance,
                "currency": acc.currency
            }
            for acc in accounts
        ]

    @router.post("/transfer", response_model=dict)
    async def transfer_funds(transfer_data: TransferRequest, db: Session = Depends(get_db)):
        service = AccountService(AccountRepository(db))
        try:
            success = service.transfer_funds(
                transfer_data.from_account_id,
                transfer_data.to_account_id,
                transfer_data.amount
            )
            return {"message": "Transfer successful", "success": success}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/account/{account_id}")
    async def get_cards_by_account(
            account_id: int,
            db: Session = Depends(get_db)
    ):
        if account_id <= 0:
            raise HTTPException(status_code=422, detail="Invalid account ID")

        cards = db.query(Card).filter(Card.accountID == account_id).all()
        return cards

    return router
