from sqlalchemy.orm import Session
from dal.interfaces.iuser_repository import IUserRepository
from models.user import User
from config import SessionLocal
from typing import Optional


class UserRepository(IUserRepository):
    def __init__(self, db: Session = None):
        self.db = db or SessionLocal()

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.userID == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def create_user(self, user_data: dict) -> User:
        user = User(**user_data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, user: User) -> None:
        self.db.commit()
        self.db.refresh(user)

    def __del__(self):
        self.db.close()