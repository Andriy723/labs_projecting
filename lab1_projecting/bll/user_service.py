from typing import Optional
from dal.interfaces.iuser_repository import IUserRepository
from models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, user_repository: IUserRepository):
        self._user_repository = user_repository

    def register_user(self, user_data: dict) -> User:
        if self._user_repository.get_by_email(user_data["email"]):
            raise ValueError("User with this email already exists")

        # Хешування пароля
        user_data["password"] = pwd_context.hash(user_data["password"])
        return self._user_repository.create_user(user_data)

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = self._user_repository.get_by_email(email)
        if not user:
            return None
        if not pwd_context.verify(password, user.password):
            return None
        return user