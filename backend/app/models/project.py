"""Project data models."""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Project(Base):
    """Project model for opportunities, permits, and tenders."""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text)
    project_type = Column(String)  # opportunity, permit, tender
    sector = Column(String)  # commercial, residential, infrastructure, healthcare
    status = Column(String, default="active")  # active, awarded, completed, cancelled
    value = Column(Float)
    estimated_start_date = Column(DateTime)
    estimated_completion_date = Column(DateTime)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)
    country = Column(String, default="USA")
    latitude = Column(Float)
    longitude = Column(Float)
    source = Column(String)
    source_url = Column(String)
    is_verified = Column(Boolean, default=False)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    owner_company_id = Column(Integer, ForeignKey("companies.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    tenant = relationship("Tenant", back_populates="projects")
    owner_company = relationship("Company", back_populates="owned_projects")
    participations = relationship("ProjectParticipation", back_populates="project")
    predictions = relationship("Prediction", back_populates="project")
    opportunity_scores = relationship("OpportunityScore", back_populates="project")


class ProjectParticipation(Base):
    """Many-to-many relationship between projects and companies."""
    __tablename__ = "project_participations"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    role = Column(String)  # owner, gc, subcontractor, supplier
    status = Column(String)  # bidding, won, lost, participating
    bid_amount = Column(Float)
    won = Column(Boolean)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    project = relationship("Project", back_populates="participations")
    company = relationship("Company", back_populates="project_participations")
