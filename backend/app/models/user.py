"""User and tenant models for multi-tenancy."""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Tenant(Base):
    """Tenant model for multi-tenancy."""
    
    __tablename__ = "tenants"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    subdomain = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    subscription_tier = Column(String, default="basic")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    users = relationship("User", back_populates="tenant")


class User(Base):
    """User model."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    tenant = relationship("Tenant", back_populates="users")
