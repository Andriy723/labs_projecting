from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from config import Base
import datetime

class User(Base):
    __tablename__ = "users"

    userID = Column(Integer, primary_key=True, index=True)
    userName = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    phoneNumber = Column(String(20), nullable=False)
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    lastLogin = Column(DateTime, nullable=True)
    isActive = Column(Boolean, default=True)
    accountVerified = Column(Boolean, default=False)

    accounts = relationship("Account", back_populates="user")
    payment_methods = relationship("PaymentMethod", back_populates="user")