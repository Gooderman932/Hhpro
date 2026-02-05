"""Subscription models."""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Subscription(Base):
    """User subscriptions."""
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    subscription_id = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_id = Column(String, unique=True)
    tier_id = Column(String, nullable=False)  # basic, professional, enterprise
    tier_name = Column(String)
    status = Column(String, default="active")  # active, cancelled, expired
    price = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))
    
    user = relationship("User", back_populates="subscriptions")


class PaymentTransaction(Base):
    """Payment transactions."""
    __tablename__ = "payment_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, index=True)
    session_id = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user_email = Column(String)
    tier_id = Column(String)
    tier_name = Column(String)
    amount = Column(Float)
    currency = Column(String, default="usd")
    payment_status = Column(String, default="pending")
    subscription_type = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
