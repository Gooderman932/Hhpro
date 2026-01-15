"""ML prediction models."""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Prediction(Base):
    """ML predictions for various outcomes."""
    
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    prediction_type = Column(String, nullable=False)  # win_probability, demand_forecast, etc.
    predicted_value = Column(Float)
    confidence = Column(Float)
    model_version = Column(String)
    features = Column(JSON)  # Store features used for prediction
    meta_data = Column("metadata", JSON)  # Additional metadata (renamed from 'metadata' to avoid SQLAlchemy reserved name)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="predictions")


class OpportunityScore(Base):
    """Opportunity scoring for projects."""
    
    __tablename__ = "opportunity_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    overall_score = Column(Float, nullable=False)
    value_score = Column(Float)
    fit_score = Column(Float)
    competition_score = Column(Float)
    timing_score = Column(Float)
    risk_score = Column(Float)
    reasoning = Column(JSON)  # Explanation of the scoring
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="opportunity_scores")
