"""Prediction service for ML models."""
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from ..models.project import Project, ProjectParticipation
from ..models.prediction import Prediction
from ..models.company import Company


class PredictionService:
    """Service for making ML predictions."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def predict_win_probability(
        self,
        project: Project,
        company: Company
    ) -> Dict[str, Any]:
        """Predict win probability for a company on a project."""
        # In production, this would use a trained ML model
        # For now, use simple heuristics
        
        # Get historical win rate for the company
        past_participations = self.db.query(ProjectParticipation).filter(
            ProjectParticipation.company_id == company.id
        ).all()
        
        if not past_participations:
            win_rate = 0.5  # Default for new companies
        else:
            wins = sum(1 for p in past_participations if p.won)
            win_rate = wins / len(past_participations)
        
        # Adjust based on sector match (simplified)
        confidence = 0.7
        
        # Create prediction record
        prediction = Prediction(
            project_id=project.id,
            prediction_type="win_probability",
            predicted_value=win_rate,
            confidence=confidence,
            model_version="v1.0",
            features={
                "historical_win_rate": win_rate,
                "past_projects": len(past_participations),
            }
        )
        
        self.db.add(prediction)
        self.db.commit()
        
        return {
            "win_probability": win_rate,
            "confidence": confidence,
            "prediction_id": prediction.id,
        }
    
    def predict_demand(
        self,
        sector: str,
        region: str,
        months_ahead: int = 6
    ) -> Dict[str, Any]:
        """Predict demand for a sector in a region."""
        # In production, this would use time series forecasting
        # For now, return placeholder data
        
        # Get historical project counts
        projects = self.db.query(Project).filter(
            Project.sector == sector,
            Project.state == region
        ).all()
        
        baseline = len(projects)
        
        # Simple trend projection
        forecast = {
            "sector": sector,
            "region": region,
            "baseline_projects": baseline,
            "forecast": [
                {"month": i, "predicted_projects": baseline + i}
                for i in range(1, months_ahead + 1)
            ],
            "confidence": 0.6,
        }
        
        return forecast
