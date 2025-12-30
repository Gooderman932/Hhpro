"""
Prediction and forecast models
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Text, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

from app.database import Base


class WinProbabilityPrediction(Base):
    """
    Win probability predictions for tenders/bids
    """
    __tablename__ = "win_probability_predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Prediction
    win_probability = Column(Float, nullable=False)  # 0-1
    confidence_score = Column(Float, nullable=False)  # 0-1
    
    # Contributing factors
    factors = Column(JSON, default={})  # {'past_wins': 0.8, 'geography_fit': 0.9, ...}
    feature_importance = Column(JSON, default={})
    
    # Model info
    model_version = Column(String(50), nullable=False)
    model_type = Column(String(50), nullable=False)  # 'random_forest', 'neural_net', etc.
    
    # Outcome (if known)
    actual_outcome = Column(Boolean, nullable=True)  # True if won, False if lost
    outcome_date = Column(DateTime, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=func.now(), index=True)
    
    __table_args__ = (
        Index('ix_win_pred_lookup', 'project_id', 'company_id'),
    )
    
    def __repr__(self):
        return f"<WinProbabilityPrediction(project={self.project_id}, company={self.company_id}, prob={self.win_probability:.2f})>"


class DemandForecast(Base):
    """
    Demand forecasts by region, sector, and time period
    """
    __tablename__ = "demand_forecasts"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Geography
    country = Column(String(100), nullable=False, index=True)
    region = Column(String(100), nullable=True, index=True)
    
    # Sector
    project_type = Column(String(100), nullable=False, index=True)
    
    # Time period
    forecast_date = Column(DateTime, nullable=False, index=True)
    forecast_period = Column(String(20), nullable=False)  # 'Q1-2025', '2025-H1', etc.
    
    # Forecast values
    expected_projects = Column(Integer, nullable=False)
    expected_value = Column(Float, nullable=False)  # Total $ value
    
    # Confidence intervals
    projects_low = Column(Integer, nullable=True)
    projects_high = Column(Integer, nullable=True)
    value_low = Column(Float, nullable=True)
    value_high = Column(Float, nullable=True)
    
    # Growth metrics
    yoy_growth = Column(Float, nullable=True)  # Year-over-year growth %
    qoq_growth = Column(Float, nullable=True)  # Quarter-over-quarter growth %
    
    # Model info
    model_version = Column(String(50), nullable=False)
    confidence_score = Column(Float, nullable=True)
    
    # Contributing factors
    factors = Column(JSON, default={})
    
    # Actual outcome (for model validation)
    actual_projects = Column(Integer, nullable=True)
    actual_value = Column(Float, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index('ix_forecast_lookup', 'country', 'project_type', 'forecast_date'),
    )
    
    def __repr__(self):
        return f"<DemandForecast(region='{self.region}', type='{self.project_type}', period='{self.forecast_period}')>"


class PriceAnalysis(Base):
    """
    Price and cost analysis for materials, labor, and project types
    """
    __tablename__ = "price_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # What's being priced
    item_type = Column(String(100), nullable=False, index=True)  # 'material', 'labor', 'project'
    item_name = Column(String(255), nullable=False, index=True)  # 'steel', 'concrete', 'electrician_hourly'
    
    # Geography
    country = Column(String(100), nullable=False, index=True)
    region = Column(String(100), nullable=True)
    
    # Price data
    current_price = Column(Float, nullable=False)
    currency = Column(String(3), default="USD")
    unit = Column(String(50), nullable=True)  # 'per_sqft', 'per_ton', 'per_hour'
    
    # Trends
    price_1m_ago = Column(Float, nullable=True)
    price_3m_ago = Column(Float, nullable=True)
    price_12m_ago = Column(Float, nullable=True)
    
    # Statistics
    price_min_12m = Column(Float, nullable=True)
    price_max_12m = Column(Float, nullable=True)
    price_avg_12m = Column(Float, nullable=True)
    price_volatility = Column(Float, nullable=True)  # Standard deviation
    
    # Period
    analysis_date = Column(DateTime, nullable=False, index=True)
    
    # Sources
    data_sources = Column(JSON, default=[])
    sample_size = Column(Integer, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=func.now())
    
    __table_args__ = (
        Index('ix_price_lookup', 'item_type', 'item_name', 'country', 'analysis_date'),
    )
    
    def __repr__(self):
        return f"<PriceAnalysis(item='{self.item_name}', price={self.current_price}, region='{self.region}')>"


class ScenarioAnalysis(Base):
    """
    Scenario modeling results (e.g., impact of rate changes, policy shifts)
    """
    __tablename__ = "scenario_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Scenario definition
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    scenario_type = Column(String(100), nullable=False)  # 'interest_rate', 'commodity_price', 'policy', etc.
    
    # Parameters
    parameters = Column(JSON, nullable=False)  # The scenario inputs
    
    # Results
    baseline_forecast = Column(JSON, nullable=True)
    scenario_forecast = Column(JSON, nullable=True)
    impact_analysis = Column(JSON, nullable=True)
    
    # Summary metrics
    impact_magnitude = Column(Float, nullable=True)  # % change from baseline
    affected_projects = Column(Integer, nullable=True)
    affected_value = Column(Float, nullable=True)
    
    # Model
    model_version = Column(String(50), nullable=False)
    
    # Status
    is_saved = Column(Boolean, default=False)
    is_shared = Column(Boolean, default=False)
    
    # Metadata
    created_at = Column(DateTime, default=func.now(), index=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<ScenarioAnalysis(id={self.id}, name='{self.name}', type='{self.scenario_type}')>"
