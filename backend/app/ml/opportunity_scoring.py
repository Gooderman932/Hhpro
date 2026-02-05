"""
Opportunity Scoring Model - Multi-factor scoring for project opportunities.
Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.
"""
from typing import Dict, Any, List, Optional
from datetime import datetime


class OpportunityScorer:
    """Multi-factor opportunity scoring engine."""
    
    def __init__(self):
        self.model_version = "1.0.0"
        
        # Scoring weights
        self.weights = {
            'value': 0.20,
            'fit': 0.25,
            'competition': 0.20,
            'timing': 0.15,
            'risk': 0.20
        }
        
        # Target sectors (company's specialization)
        self.target_sectors = ['Commercial', 'Healthcare', 'Infrastructure']
        
        # Target regions
        self.target_regions = ['TX', 'FL', 'AZ', 'CA', 'WA']
    
    def score_opportunity(
        self,
        project: Dict[str, Any],
        company_profile: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Score a project opportunity."""
        
        if company_profile is None:
            company_profile = {}
        
        # Calculate individual scores
        value_score = self._score_value(project)
        fit_score = self._score_fit(project, company_profile)
        competition_score = self._score_competition(project)
        timing_score = self._score_timing(project)
        risk_score = self._score_risk(project)
        
        # Calculate weighted overall score
        overall_score = (
            value_score * self.weights['value'] +
            fit_score * self.weights['fit'] +
            competition_score * self.weights['competition'] +
            timing_score * self.weights['timing'] +
            risk_score * self.weights['risk']
        )
        
        # Generate reasoning
        reasoning = self._generate_reasoning(
            project, value_score, fit_score, competition_score, timing_score, risk_score
        )
        
        # Determine recommendation
        recommendation = self._get_recommendation(overall_score)
        
        return {
            'overall_score': round(overall_score, 2),
            'scores': {
                'value': round(value_score, 2),
                'fit': round(fit_score, 2),
                'competition': round(competition_score, 2),
                'timing': round(timing_score, 2),
                'risk': round(risk_score, 2)
            },
            'weights': self.weights,
            'recommendation': recommendation,
            'reasoning': reasoning,
            'model_version': self.model_version,
            'scored_at': datetime.now().isoformat()
        }
    
    def _score_value(self, project: Dict) -> float:
        """Score based on project value."""
        value = project.get('value', 0)
        
        if value >= 50_000_000:
            return 1.0
        elif value >= 20_000_000:
            return 0.9
        elif value >= 10_000_000:
            return 0.8
        elif value >= 5_000_000:
            return 0.7
        elif value >= 1_000_000:
            return 0.6
        else:
            return 0.4
    
    def _score_fit(self, project: Dict, company_profile: Dict) -> float:
        """Score based on sector and geographic fit."""
        score = 0.5  # Base score
        
        sector = project.get('sector', '')
        state = project.get('state', '')
        
        # Sector fit
        target_sectors = company_profile.get('target_sectors', self.target_sectors)
        if sector in target_sectors:
            score += 0.3
        
        # Geographic fit
        target_regions = company_profile.get('target_regions', self.target_regions)
        if state in target_regions:
            score += 0.2
        
        return min(1.0, score)
    
    def _score_competition(self, project: Dict) -> float:
        """Score based on expected competition level."""
        competitor_count = project.get('competitor_count', 5)
        
        if competitor_count <= 2:
            return 1.0
        elif competitor_count <= 4:
            return 0.8
        elif competitor_count <= 6:
            return 0.6
        elif competitor_count <= 10:
            return 0.4
        else:
            return 0.2
    
    def _score_timing(self, project: Dict) -> float:
        """Score based on project timing."""
        status = project.get('status', 'active')
        project_type = project.get('project_type', '')
        
        score = 0.5
        
        if status == 'active':
            score += 0.3
        
        if project_type == 'tender':
            score += 0.2  # Tenders are often more structured
        elif project_type == 'opportunity':
            score += 0.1
        
        return min(1.0, score)
    
    def _score_risk(self, project: Dict) -> float:
        """Score based on risk factors (higher = lower risk)."""
        score = 0.7  # Base score
        
        is_verified = project.get('is_verified', False)
        value = project.get('value', 0)
        
        if is_verified:
            score += 0.2
        
        # Very high value projects carry more risk
        if value > 100_000_000:
            score -= 0.2
        
        return max(0.2, min(1.0, score))
    
    def _generate_reasoning(
        self, project: Dict, value_score: float, fit_score: float,
        competition_score: float, timing_score: float, risk_score: float
    ) -> List[Dict[str, str]]:
        """Generate human-readable reasoning for the scores."""
        reasoning = []
        
        # Value reasoning
        value = project.get('value', 0)
        if value_score >= 0.8:
            reasoning.append({
                'factor': 'value',
                'assessment': 'positive',
                'explanation': f'High-value project (${value:,.0f}) represents significant revenue opportunity.'
            })
        elif value_score >= 0.6:
            reasoning.append({
                'factor': 'value',
                'assessment': 'neutral',
                'explanation': f'Moderate project value (${value:,.0f}) - standard opportunity.'
            })
        else:
            reasoning.append({
                'factor': 'value',
                'assessment': 'negative',
                'explanation': f'Lower project value (${value:,.0f}) may not justify pursuit costs.'
            })
        
        # Fit reasoning
        sector = project.get('sector', 'Unknown')
        state = project.get('state', 'Unknown')
        if fit_score >= 0.8:
            reasoning.append({
                'factor': 'fit',
                'assessment': 'positive',
                'explanation': f'{sector} sector in {state} aligns well with company expertise and presence.'
            })
        elif fit_score >= 0.5:
            reasoning.append({
                'factor': 'fit',
                'assessment': 'neutral',
                'explanation': f'Partial alignment with company focus areas.'
            })
        else:
            reasoning.append({
                'factor': 'fit',
                'assessment': 'negative',
                'explanation': f'{sector} sector or {state} location outside core competencies.'
            })
        
        # Competition reasoning
        if competition_score >= 0.7:
            reasoning.append({
                'factor': 'competition',
                'assessment': 'positive',
                'explanation': 'Limited competition expected - favorable bidding environment.'
            })
        elif competition_score >= 0.4:
            reasoning.append({
                'factor': 'competition',
                'assessment': 'neutral',
                'explanation': 'Moderate competition expected - standard market conditions.'
            })
        else:
            reasoning.append({
                'factor': 'competition',
                'assessment': 'negative',
                'explanation': 'High competition expected - will need competitive pricing strategy.'
            })
        
        return reasoning
    
    def _get_recommendation(self, overall_score: float) -> Dict[str, Any]:
        """Get recommendation based on overall score."""
        if overall_score >= 0.8:
            return {
                'action': 'PURSUE',
                'priority': 'high',
                'description': 'Strong opportunity - recommend aggressive pursuit.'
            }
        elif overall_score >= 0.6:
            return {
                'action': 'EVALUATE',
                'priority': 'medium',
                'description': 'Good opportunity - worth further evaluation.'
            }
        elif overall_score >= 0.4:
            return {
                'action': 'CONSIDER',
                'priority': 'low',
                'description': 'Mixed signals - pursue only if capacity allows.'
            }
        else:
            return {
                'action': 'PASS',
                'priority': 'none',
                'description': 'Poor fit - recommend passing on this opportunity.'
            }
    
    def batch_score(self, projects: List[Dict], company_profile: Optional[Dict] = None) -> List[Dict]:
        """Score multiple projects and rank them."""
        scored = []
        for project in projects:
            score_result = self.score_opportunity(project, company_profile)
            score_result['project'] = project
            scored.append(score_result)
        
        # Sort by overall score
        return sorted(scored, key=lambda x: x['overall_score'], reverse=True)
