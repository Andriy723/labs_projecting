from typing import Optional, List
from dal.interfaces.iuser_repository import IUserRepository
from models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, user_repository: IUserRepository):
        self._user_repository = user_repository


    def get_all_users(self) -> List[User]:
        return self._user_repository.get_all()

    def update_user(self, user_id: int, user_data: dict) -> Optional[User]:
        user = self._user_repository.get_by_id(user_id)
        if not user:
            return None

        for key, value in user_data.items():
            if hasattr(user, key):
                setattr(user, key, value)

        return self._user_repository.update_user(user)

    def partial_update_user(self, user_id: int, user_data: dict) -> Optional[User]:
        user = self._user_repository.get_by_id(user_id)
        if not user:
            return None

        for key, value in user_data.items():
            if hasattr(user, key):
                setattr(user, key, value)

        return self._user_repository.update_user(user)

    def register_user(self, user_data: dict) -> User:
        if not user_data.get("password"):
            raise ValueError("Password is required")

        if self._user_repository.get_by_email(user_data["email"]):
            raise ValueError("User with this email already exists")

        user_data["password"] = pwd_context.hash(user_data["password"])
        return self._user_repository.create_user(user_data)

    def delete_user(self, user_id: int) -> bool:
        return self._user_repository.delete_user(user_id)

    def delete_user_with_dependencies(self, user_id: int) -> bool:
        return self._user_repository.delete_user(user_id)