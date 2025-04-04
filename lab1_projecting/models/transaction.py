import datetime

from sqlalchemy import Column, Integer, Double, DateTime, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from config import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Double, nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    description = Column(String(255), nullable=True)
    accountID = Column(Integer, ForeignKey("accounts.accountID"))

    account = relationship("Account", back_populates="transactions")