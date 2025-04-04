from typing import Optional
from dal.interfaces.iuser_repository import IUserRepository
from models.user import User


class UserService:
    def __init__(self, user_repository: IUserRepository):
        self._user_repository = user_repository

    def register_user(self, user_data: dict) -> User:
        if self._user_repository.get_by_email(user_data["email"]):
            raise ValueError("User with this email already exists")
        return self._user_repository.create_user(user_data)

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = self._user_repository.get_by_email(email)
        if user and user.password == password:
            return user
        return None