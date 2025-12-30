"""
Company and relationship models for competitive intelligence
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON, Text, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database import Base


class CompanyType(str, enum.Enum):
    """Types of companies in construction industry"""
    GENERAL_CONTRACTOR = "general_contractor"
    SUBCONTRACTOR = "subcontractor"
    SUPPLIER = "supplier"
    OWNER = "owner"
    DEVELOPER = "developer"
    ARCHITECT = "architect"
    ENGINEER = "engineer"
    CONSULTANT = "consultant"
    OTHER = "other"


class CompanySize(str, enum.Enum):
    """Company size categories"""
    SMALL = "small"  # <50 employees
    MEDIUM = "medium"  # 50-250 employees
    LARGE = "large"  # 250-1000 employees
    ENTERPRISE = "enterprise"  # 1000+ employees


class Company(Base):
    """
    Companies in the construction ecosystem
    """
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Basic Information
    name = Column(String(255), nullable=False, index=True)
    legal_name = Column(String(255), nullable=True)
    company_type = Column(SQLEnum(CompanyType), nullable=False, index=True)
    size = Column(SQLEnum(CompanySize), nullable=True)
    
    # Contact
    website = Column(String(500), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    
    # Location
    headquarters_country = Column(String(100), nullable=True, index=True)
    headquarters_region = Column(String(100), nullable=True)
    headquarters_city = Column(String(100), nullable=True)
    headquarters_address = Column(String(500), nullable=True)
    
    # Business details
    specialties = Column(JSON, default=[])  # List of specialty trades/services
    certifications = Column(JSON, default=[])
    licenses = Column(JSON, default=[])
    
    # Financial (if available)
    annual_revenue = Column(Float, nullable=True)
    employee_count = Column(Integer, nullable=True)
    
    # Intelligence
    win_rate = Column(Float, nullable=True)  # 0-1, calculated from historical data
    average_project_size = Column(Float, nullable=True)
    total_projects = Column(Integer, default=0)
    
    # Relationships & Network
    relationship_score = Column(Float, nullable=True)  # How well-connected
    key_partners = Column(JSON, default=[])  # List of company IDs they frequently work with
    
    # Data enrichment
    description = Column(Text, nullable=True)
    logo_url = Column(String(500), nullable=True)
    linkedin_url = Column(String(500), nullable=True)
    
    # External IDs
    duns_number = Column(String(50), nullable=True, index=True)
    tax_id = Column(String(50), nullable=True)
    
    # AI processing
    embeddings = Column(JSON, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Metadata
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    last_enriched_at = Column(DateTime, nullable=True)
    
    # Relationships
    tenant = relationship("Tenant")
    owned_projects = relationship("Project", foreign_keys="Project.owner_company_id", back_populates="owner")
    gc_projects = relationship("Project", foreign_keys="Project.gc_company_id", back_populates="gc")
    architect_projects = relationship("Project", foreign_keys="Project.architect_company_id", back_populates="architect")
    project_participations = relationship("ProjectParticipant", back_populates="company")
    contacts = relationship("Contact", back_populates="company", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('ix_company_search', 'tenant_id', 'company_type', 'headquarters_country'),
        Index('ix_company_name', 'name', postgresql_ops={'name': 'gin_trgm_ops'}),  # For fuzzy search
    )
    
    def __repr__(self):
        return f"<Company(id={self.id}, name='{self.name}', type={self.company_type})>"


class Contact(Base):
    """
    Key decision makers and contacts at companies
    """
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Personal information
    full_name = Column(String(255), nullable=False, index=True)
    title = Column(String(255), nullable=True)
    department = Column(String(100), nullable=True)
    
    # Contact details
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    linkedin_url = Column(String(500), nullable=True)
    
    # Metadata
    notes = Column(Text, nullable=True)
    tags = Column(JSON, default=[])
    
    # Engagement
    last_contacted = Column(DateTime, nullable=True)
    engagement_score = Column(Float, nullable=True)  # 0-1
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Metadata
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    company = relationship("Company", back_populates="contacts")
    
    def __repr__(self):
        return f"<Contact(id={self.id}, name='{self.full_name}', title='{self.title}')>"


class CompanyRelationship(Base):
    """
    Tracks relationships between companies (who works with whom)
    """
    __tablename__ = "company_relationships"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    
    company_a_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    company_b_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Relationship metrics
    relationship_type = Column(String(100), nullable=True)  # 'frequent_partners', 'competitors', etc.
    collaboration_count = Column(Integer, default=0)
    total_project_value = Column(Float, default=0.0)
    success_rate = Column(Float, nullable=True)  # Win rate when working together
    
    # Most recent collaboration
    last_project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    last_collaboration = Column(DateTime, nullable=True)
    
    # Strength of relationship
    relationship_score = Column(Float, nullable=True)  # 0-1
    
    # Metadata
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index('ix_relationship_lookup', 'company_a_id', 'company_b_id'),
    )
    
    def __repr__(self):
        return f"<CompanyRelationship(company_a={self.company_a_id}, company_b={self.company_b_id}, score={self.relationship_score})>"
