"""
Prediction Service - Orchestrates ML predictions.
Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.
"""
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from ..ml.win_probability import WinProbabilityModel
from ..ml.demand_forecast import DemandForecastModel
from ..models.prediction import Prediction
from ..models.project import Project


class PredictionService:
    """Service for managing ML predictions."""
    
    def __init__(self, db: Session):
        self.db = db
        self.win_model = WinProbabilityModel()
        self.demand_model = DemandForecastModel()
    
    def predict_win_probability(
        self,
        project_id: int,
        company_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate win probability prediction for a project."""
        
        # Get project from database
        project = self.db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise ValueError(f"Project {project_id} not found")
        
        # Build project data dict
        project_data = {
            'value': project.value or 0,
            'sector': project.sector,
            'city': project.city,
            'state': project.state,
            'project_type': project.project_type,
            'competitor_count': 5,  # Default
            'timing_score': 0.7 if project.status == 'active' else 0.4
        }
        
        # Default company data if not provided
        if company_data is None:
            company_data = {
                'years_experience': 10,
                'past_win_rate': 0.35,
                'relationship_strength': 0.5,
                'sector_fit': 0.7 if project.sector in ['Commercial', 'Healthcare'] else 0.5,
                'geographic_proximity': 0.6
            }
        
        # Generate prediction
        result = self.win_model.predict(project_data, company_data)
        
        # Store prediction in database
        prediction = Prediction(
            project_id=project_id,
            prediction_type='win_probability',
            predicted_value=result['win_probability'],
            confidence=result['confidence'],
            model_version=result['model_version'],
            features={'project': project_data, 'company': company_data}
        )
        self.db.add(prediction)
        self.db.commit()
        
        result['project_id'] = project_id
        result['project_title'] = project.title
        return result
    
    def forecast_demand(
        self,
        sector: str,
        region: str,
        months_ahead: int = 6
    ) -> Dict[str, Any]:
        """Generate demand forecast for sector/region."""
        return self.demand_model.forecast(sector, region, months_ahead)
    
    def get_regional_outlook(self, regions: Optional[List[str]] = None) -> List[Dict]:
        """Get demand outlook for multiple regions."""
        return self.demand_model.get_regional_outlook(regions)
    
    def get_project_predictions(self, project_id: int) -> List[Dict]:
        """Get all predictions for a project."""
        predictions = self.db.query(Prediction).filter(
            Prediction.project_id == project_id
        ).order_by(Prediction.created_at.desc()).all()
        
        return [
            {
                'id': p.id,
                'prediction_type': p.prediction_type,
                'predicted_value': p.predicted_value,
                'confidence': p.confidence,
                'model_version': p.model_version,
                'created_at': p.created_at.isoformat() if p.created_at else None
            }
            for p in predictions
        ]
