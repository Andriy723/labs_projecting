from sqlalchemy import Column, Integer, String, Double, ForeignKey
from sqlalchemy.orm import relationship
from config import Base

class Account(Base):
    __tablename__ = "accounts"

    accountID = Column(Integer, primary_key=True, index=True)
    accountNumber = Column(String(34), unique=True, nullable=False)
    balance = Column(Double, default=0.0)
    currency = Column(String(10), nullable=False)
    userID = Column(Integer, ForeignKey("users.userID"))

    user = relationship("User", back_populates="accounts")
    cards = relationship("Card", back_populates="account")
    transactions = relationship("Transaction", back_populates="account")