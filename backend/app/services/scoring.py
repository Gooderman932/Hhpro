"""
Opportunity scoring service.

Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.
PROPRIETARY AND CONFIDENTIAL - Unauthorized use prohibited.

This module contains proprietary scoring algorithms and business logic.
"""
from typing import Dict, Any
from sqlalchemy.orm import Session
from ..models.project import Project
from ..models.prediction import OpportunityScore


class ScoringService:
    """Service for scoring project opportunities."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def score_opportunity(self, project: Project) -> OpportunityScore:
        """Score an opportunity based on multiple factors."""
        # Calculate individual scores
        value_score = self._calculate_value_score(project)
        fit_score = self._calculate_fit_score(project)
        competition_score = self._calculate_competition_score(project)
        timing_score = self._calculate_timing_score(project)
        risk_score = self._calculate_risk_score(project)
        
        # Calculate overall score (weighted average)
        overall_score = (
            value_score * 0.25 +
            fit_score * 0.25 +
            competition_score * 0.20 +
            timing_score * 0.15 +
            risk_score * 0.15
        )
        
        # Create or update opportunity score
        existing_score = self.db.query(OpportunityScore).filter(
            OpportunityScore.project_id == project.id
        ).first()
        
        if existing_score:
            score = existing_score
        else:
            score = OpportunityScore(project_id=project.id)
        
        score.overall_score = overall_score
        score.value_score = value_score
        score.fit_score = fit_score
        score.competition_score = competition_score
        score.timing_score = timing_score
        score.risk_score = risk_score
        score.reasoning = {
            "value": f"Project value: ${project.value or 0:,.0f}",
            "fit": "Based on sector alignment",
            "competition": "Based on historical participation",
            "timing": "Based on project timeline",
            "risk": "Based on project verification and completeness"
        }
        
        self.db.add(score)
        self.db.commit()
        self.db.refresh(score)
        
        return score
    
    def _calculate_value_score(self, project: Project) -> float:
        """Calculate value score (0-1) based on project value."""
        if not project.value:
            return 0.5
        
        # Normalize to 0-1 scale (assuming max value of $100M)
        max_value = 100_000_000
        normalized = min(project.value / max_value, 1.0)
        return normalized
    
    def _calculate_fit_score(self, project: Project) -> float:
        """Calculate fit score based on sector and location."""
        # In production, this would compare against company capabilities
        # For now, return a moderate score
        return 0.7
    
    def _calculate_competition_score(self, project: Project) -> float:
        """Calculate competition score (higher = less competition)."""
        # Count participants
        participant_count = len(project.participations)
        
        if participant_count == 0:
            return 1.0
        elif participant_count <= 3:
            return 0.8
        elif participant_count <= 6:
            return 0.6
        else:
            return 0.4
    
    def _calculate_timing_score(self, project: Project) -> float:
        """Calculate timing score based on project timeline."""
        # In production, consider start dates and deadlines
        # For now, return moderate score
        return 0.7
    
    def _calculate_risk_score(self, project: Project) -> float:
        """Calculate risk score (higher = lower risk)."""
        # Consider verification status and data completeness
        if project.is_verified:
            return 0.9
        elif project.value and project.city and project.state:
            return 0.7
        else:
            return 0.5
