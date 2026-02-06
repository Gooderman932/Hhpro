"""User profile and personalization models."""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from ..database import Base


class UserProfile(Base):
    """Extended user profile with business information."""
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Business Information
    business_type = Column(String(50))  # gc, subcontractor, supplier, owner, other
    trade_specialty = Column(String(100))  # electrical, plumbing, drywall, etc.
    company_size = Column(String(50))  # 1-10, 11-50, 51-200, 200+
    
    # Service Area
    service_states = Column(JSON, default=list)  # ["TX", "AZ", "FL"]
    service_cities = Column(JSON, default=list)  # ["Austin", "Houston"]
    service_radius_miles = Column(Integer, default=50)
    
    # Preferences
    min_project_value = Column(Float, default=100000)
    max_project_value = Column(Float, default=50000000)
    preferred_sectors = Column(JSON, default=list)
    
    # Saved Searches
    saved_searches = Column(JSON, default=list)
    
    # Onboarding
    onboarding_completed = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class UserProject(Base):
    """User's own projects they want to track."""
    __tablename__ = "user_projects"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Project Details
    name = Column(String(255), nullable=False)
    description = Column(Text)
    value = Column(Float)
    sector = Column(String(100))
    status = Column(String(50))  # bidding, won, lost, in_progress, completed
    
    # Location
    address = Column(String(255))
    city = Column(String(100))
    state = Column(String(50))
    zip_code = Column(String(20))
    
    # Bidding Info
    bid_date = Column(DateTime)
    bidding_competitors = Column(JSON, default=list)  # ["Company A", "Company B"]
    
    # AI Enrichment
    ai_category = Column(String(100))
    ai_insights = Column(Text)
    ai_enriched = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TrackedCompetitor(Base):
    """Competitors user wants to track."""
    __tablename__ = "tracked_competitors"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Competitor Info
    company_name = Column(String(255), nullable=False)
    company_type = Column(String(100))  # gc, subcontractor, supplier
    specialties = Column(JSON, default=list)
    
    # Tracking Data
    notes = Column(Text)
    threat_level = Column(String(20))  # low, medium, high
    estimated_revenue = Column(Float)
    
    # Activity Tracking
    recent_wins = Column(Integer, default=0)
    recent_bids = Column(Integer, default=0)
    last_activity_date = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class UserClient(Base):
    """User's clients/customers to track relationships."""
    __tablename__ = "user_clients"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Client Info
    company_name = Column(String(255), nullable=False)
    contact_name = Column(String(255))
    contact_email = Column(String(255))
    contact_phone = Column(String(50))
    
    # Relationship
    relationship_strength = Column(Integer, default=5)  # 1-10 scale
    total_projects = Column(Integer, default=0)
    total_revenue = Column(Float, default=0)
    
    # Notes
    notes = Column(Text)
    last_contact_date = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PermitData(Base):
    """Cached construction permit data from external APIs."""
    __tablename__ = "permit_data"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Permit Info
    permit_number = Column(String(100), unique=True, index=True)
    permit_type = Column(String(100))  # commercial, residential, renovation
    
    # Project Details
    project_name = Column(String(255))
    description = Column(Text)
    estimated_value = Column(Float)
    
    # Location
    address = Column(String(255))
    city = Column(String(100), index=True)
    state = Column(String(50), index=True)
    zip_code = Column(String(20))
    
    # Parties
    owner_name = Column(String(255))
    contractor_name = Column(String(255))
    
    # Dates
    issue_date = Column(DateTime, index=True)
    expiration_date = Column(DateTime)
    
    # Classification
    sector = Column(String(100))
    building_type = Column(String(100))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    fetched_at = Column(DateTime, default=datetime.utcnow)


class SmartAlert(Base):
    """User alert preferences and history."""
    __tablename__ = "smart_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Alert Type
    alert_type = Column(String(50))  # new_permit, competitor_activity, market_trend, opportunity
    
    # Content
    title = Column(String(255))
    message = Column(Text)
    data = Column(JSON)
    
    # Status
    is_read = Column(Boolean, default=False)
    is_sent = Column(Boolean, default=False)
    
    # Priority
    priority = Column(String(20), default="normal")  # low, normal, high, urgent
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    read_at = Column(DateTime)


class EconomicIndicator(Base):
    """Cached economic data from FRED and other sources."""
    __tablename__ = "economic_indicators"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Indicator Info
    indicator_code = Column(String(50), index=True)  # FRED series ID
    indicator_name = Column(String(255))
    category = Column(String(100))  # construction, housing, employment, materials
    
    # Data
    value = Column(Float)
    previous_value = Column(Float)
    percent_change = Column(Float)
    
    # Geographic
    region = Column(String(100))  # national, state code, MSA
    
    # Time Period
    period_date = Column(DateTime, index=True)
    period_type = Column(String(20))  # monthly, quarterly, annual
    
    # Timestamps
    fetched_at = Column(DateTime, default=datetime.utcnow)
