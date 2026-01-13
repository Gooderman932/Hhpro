"""Company data models."""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Company(Base):
    """Company model for general contractors, subcontractors, suppliers, and owners."""
    
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    company_type = Column(String)  # GC, subcontractor, supplier, owner
    industry = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)
    country = Column(String, default="USA")
    phone = Column(String)
    email = Column(String)
    website = Column(String)
    description = Column(Text)
    annual_revenue = Column(Float)
    employee_count = Column(Integer)
    founded_year = Column(Integer)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    owned_projects = relationship("Project", back_populates="owner_company")

    # Relationships
    project_participations = relationship("ProjectParticipation", back_populates="company")
