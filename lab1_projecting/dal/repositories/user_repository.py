from sqlalchemy.orm import Session
from dal.interfaces.iuser_repository import IUserRepository
from models.user import User
from config import SessionLocal
from typing import Optional, List


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

    def update_user(self, user: User) -> User:
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user_id: int) -> bool:
        user = self.get_by_id(user_id)
        if not user:
            return False

        self.db.delete(user)
        self.db.commit()
        return True

    def get_all(self) -> List[User]:
        return self.db.query(User).all()

    def __del__(self):
        self.db.close()