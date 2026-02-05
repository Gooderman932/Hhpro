"""
Scoring Service - Manages opportunity scoring.
Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.
"""
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from ..ml.opportunity_scoring import OpportunityScorer
from ..models.prediction import OpportunityScore
from ..models.project import Project


class ScoringService:
    """Service for managing opportunity scores."""
    
    def __init__(self, db: Session):
        self.db = db
        self.scorer = OpportunityScorer()
    
    def score_project(
        self,
        project_id: int,
        company_profile: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Score an opportunity for a specific project."""
        
        # Get project from database
        project = self.db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise ValueError(f"Project {project_id} not found")
        
        # Build project data dict
        project_data = {
            'value': project.value or 0,
            'sector': project.sector,
            'state': project.state,
            'city': project.city,
            'project_type': project.project_type,
            'status': project.status,
            'is_verified': project.is_verified,
            'competitor_count': 5  # Default
        }
        
        # Generate score
        result = self.scorer.score_opportunity(project_data, company_profile)
        
        # Store in database
        opp_score = OpportunityScore(
            project_id=project_id,
            overall_score=result['overall_score'],
            value_score=result['scores']['value'],
            fit_score=result['scores']['fit'],
            competition_score=result['scores']['competition'],
            timing_score=result['scores']['timing'],
            risk_score=result['scores']['risk'],
            reasoning=result['reasoning']
        )
        self.db.add(opp_score)
        self.db.commit()
        
        result['project_id'] = project_id
        result['project_title'] = project.title
        result['score_id'] = opp_score.id
        return result
    
    def batch_score_projects(
        self,
        tenant_id: int,
        limit: int = 50,
        company_profile: Optional[Dict] = None
    ) -> List[Dict]:
        """Score and rank multiple projects for a tenant."""
        
        # Get active projects
        projects = self.db.query(Project).filter(
            Project.tenant_id == tenant_id,
            Project.status == 'active'
        ).limit(limit).all()
        
        # Build project data list
        project_data_list = [
            {
                'id': p.id,
                'title': p.title,
                'value': p.value or 0,
                'sector': p.sector,
                'state': p.state,
                'city': p.city,
                'project_type': p.project_type,
                'status': p.status,
                'is_verified': p.is_verified,
                'competitor_count': 5
            }
            for p in projects
        ]
        
        # Batch score
        results = self.scorer.batch_score(project_data_list, company_profile)
        
        # Add project details to results
        for result in results:
            project_info = result.pop('project')
            result['project_id'] = project_info['id']
            result['project_title'] = project_info['title']
            result['project_value'] = project_info['value']
            result['project_sector'] = project_info['sector']
            result['project_location'] = f"{project_info['city']}, {project_info['state']}"
        
        return results
    
    def get_project_scores(self, project_id: int) -> List[Dict]:
        """Get all scores for a project."""
        scores = self.db.query(OpportunityScore).filter(
            OpportunityScore.project_id == project_id
        ).order_by(OpportunityScore.created_at.desc()).all()
        
        return [
            {
                'id': s.id,
                'overall_score': s.overall_score,
                'scores': {
                    'value': s.value_score,
                    'fit': s.fit_score,
                    'competition': s.competition_score,
                    'timing': s.timing_score,
                    'risk': s.risk_score
                },
                'reasoning': s.reasoning,
                'created_at': s.created_at.isoformat() if s.created_at else None
            }
            for s in scores
        ]
