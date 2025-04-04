from fastapi import APIRouter, Depends, HTTPException
from bll.user_service import UserService
from dal.repositories.user_repository import UserRepository
from config import get_db


def create_user_router():
    router = APIRouter()

    @router.post("/")
    async def create_user(user_data: dict, db=Depends(get_db)):
        try:
            user_repo = UserRepository(db)
            service = UserService(user_repo)

            user = service.register_user(user_data)
            return {"message": "User created", "user_id": user.userID}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.post("/login")
    async def login_user(credentials: dict, db=Depends(get_db)):
        try:
            user_repo = UserRepository(db)
            service = UserService(user_repo)

            user = service.authenticate_user(
                credentials["email"],
                credentials["password"]
            )
            if not user:
                raise HTTPException(status_code=401, detail="Invalid credentials")
            return {"message": "Login successful", "user_id": user.userID}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    return router