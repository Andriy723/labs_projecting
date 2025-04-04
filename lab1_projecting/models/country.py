from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config import Base

class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    currency = Column(String(10), nullable=False)

    cards = relationship("Card", back_populates="country")