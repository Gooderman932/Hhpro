"""Notification preferences model."""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from ..database import Base


class NotificationPreference(Base):
    """User notification preferences for project alerts."""
    __tablename__ = "notification_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Email settings
    email_enabled = Column(Boolean, default=True)
    
    # Frequency: 'realtime', 'daily', 'weekly'
    frequency = Column(String(20), default='daily')
    
    # Value threshold (minimum project value in dollars)
    min_project_value = Column(Float, default=1000000)  # $1M default
    
    # Preferred sectors (JSON array)
    preferred_sectors = Column(JSON, default=list)
    
    # Preferred regions/states (JSON array)
    preferred_regions = Column(JSON, default=list)
    
    # Match type: 'any' (OR) or 'all' (AND)
    match_type = Column(String(10), default='any')
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Last notification sent
    last_notified_at = Column(DateTime, nullable=True)
    
    # Relationship
    user = relationship("User", back_populates="notification_preferences")


class NotificationLog(Base):
    """Log of sent notifications."""
    __tablename__ = "notification_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Notification type: 'realtime', 'daily_digest', 'weekly_digest'
    notification_type = Column(String(20), nullable=False)
    
    # Email details
    subject = Column(String(255), nullable=False)
    recipient_email = Column(String(255), nullable=False)
    
    # Projects included (JSON array of project IDs)
    project_ids = Column(JSON, default=list)
    
    # Status: 'sent', 'failed', 'pending'
    status = Column(String(20), default='pending')
    error_message = Column(String(500), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    sent_at = Column(DateTime, nullable=True)
