from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from config import Base

class CardType(PyEnum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"
    PREPARED = "PREPARED"

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    cardNumber = Column(String(16), unique=True, nullable=False)
    holderName = Column(String(100), nullable=False)
    expiryDate = Column(String(5), nullable=False)
    cvv = Column(String(3), nullable=False)
    cardType = Column(Enum(CardType), nullable=False)
    cardIssuer = Column(String(100), nullable=False)
    issuingCountry = Column(Integer, ForeignKey("countries.id"))
    accountID = Column(Integer, ForeignKey("accounts.accountID"))

    account = relationship("Account", back_populates="cards")
    country = relationship("Country", back_populates="cards")