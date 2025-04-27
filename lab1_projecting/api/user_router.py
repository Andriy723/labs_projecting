from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from bll.user_service import UserService, pwd_context
from dal.repositories.user_repository import UserRepository
from config import get_db
from sqlalchemy.orm import Session

from models import Account, Card, Transaction, PaymentMethod


class UserCreate(BaseModel):
    userName: str
    email: str
    password: str
    phoneNumber: str
    isActive: bool = True
    accountVerified: bool = False


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    message: str
    user_id: int

class UserUpdate(BaseModel):
    userName: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    phoneNumber: Optional[str] = None
    isActive: Optional[bool] = None
    accountVerified: Optional[bool] = None


def create_user_router():
    router = APIRouter()

    @router.get("/")
    async def get_all_users(db: Session = Depends(get_db)):
        try:
            user_repo = UserRepository(db)
            service = UserService(user_repo)
            users = service.get_all_users()
            return users
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/")
    async def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
        try:
            user_repo = UserRepository(db)
            service = UserService(user_repo)
            user = service.register_user(user_data.dict())
            return user
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.put("/{user_id}")
    async def update_user(
            user_id: int,
            user_data: UserUpdate,
            db: Session = Depends(get_db)
    ):
        try:
            user_repo = UserRepository(db)
            service = UserService(user_repo)

            update_data = user_data.dict(exclude_unset=True)

            if 'password' in update_data:
                update_data['password'] = pwd_context.hash(update_data['password'])

            user = service.update_user(user_id, update_data)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.patch("/{user_id}")
    async def partial_update_user(user_id: int, user_data: dict, db: Session = Depends(get_db)):
        try:
            user_repo = UserRepository(db)
            service = UserService(user_repo)
            user = service.partial_update_user(user_id, user_data)  # Implement this method
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.delete("/{user_id}")
    async def delete_user(
            user_id: int,
            cascade: bool = Query(False, description="Delete all related objects"),
            db: Session = Depends(get_db)
    ):
        try:
            user_repo = UserRepository(db)
            service = UserService(user_repo)

            if cascade:
                accounts = db.query(Account).filter(Account.userID == user_id).all()
                for account in accounts:
                    db.query(Card).filter(Card.accountID == account.accountID).delete()
                    db.query(Transaction).filter(Transaction.accountID == account.accountID).delete()
                    db.query(PaymentMethod).filter(PaymentMethod.userID == user_id).delete()
                    db.delete(account)

            success = service.delete_user(user_id)
            if not success:
                raise HTTPException(status_code=404, detail="User not found")
            return {"message": "User deleted successfully"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    return router