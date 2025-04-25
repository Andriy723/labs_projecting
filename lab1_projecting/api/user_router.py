from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from bll.user_service import UserService
from dal.repositories.user_repository import UserRepository
from config import get_db


class UserCreate(BaseModel):
    userName: str
    email: str
    password: str
    phoneNumber: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    message: str
    user_id: int


def create_user_router():
    router = APIRouter()

    @router.post("/", response_model=UserResponse)
    async def create_user(user_data: UserCreate, db=Depends(get_db)):
        try:
            user_repo = UserRepository(db)
            service = UserService(user_repo)

            user = service.register_user(user_data.dict())
            return {"message": "User created", "user_id": user.userID}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.post("/login", response_model=UserResponse)
    async def login_user(credentials: UserLogin, db=Depends(get_db)):
        try:
            user_repo = UserRepository(db)
            service = UserService(user_repo)

            user = service.authenticate_user(
                credentials.email,
                credentials.password
            )
            if not user:
                raise HTTPException(status_code=401, detail="Invalid credentials")
            return {"message": "Login successful", "user_id": user.userID}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    # api/user_router.py
    @router.get("/{user_id}")
    async def get_user(user_id: int, db=Depends(get_db)):
        service = UserService(UserRepository(db))
        user = service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return {
            "userID": user.userID,
            "userName": user.userName,
            "email": user.email,
            "phoneNumber": user.phoneNumber
        }

    return router