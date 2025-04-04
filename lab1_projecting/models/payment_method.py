from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from config import Base

class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    isDefault = Column(Boolean, default=False)
    userID = Column(Integer, ForeignKey("users.userID"), nullable=False)

    user = relationship("User", back_populates="payment_methods")