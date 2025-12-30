"""
Opportunity Scoring Engine
Scores and prioritizes construction projects based on fit, likelihood, and value
"""
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from loguru import logger
from sqlalchemy.orm import Session

from app.models.project import Project, ProjectType, ProjectStage, OpportunityScore
from app.models.company import Company
from app.ml.win_probability import win_probability_model


class OpportunityScorer:
    """
    Multi-factor scoring system for opportunity prioritization
    
    Scores based on:
    1. Fit - How well the project matches company capabilities
    2. Likelihood - Probability of project going ahead
    3. Size - Project value and strategic importance
    4. Timing - Urgency and timeline
    5. Competition - Expected competitive intensity
    """
    
    def __init__(self):
        self.weights = {
            'fit': 0.30,
            'likelihood': 0.25,
            'size': 0.20,
            'timing': 0.15,
            'competition': 0.10
        }
    
    def score_opportunity(self, 
                         project: Project,
                         company: Company,
                         db: Session,
                         include_win_prob: bool = True) -> Dict:
        """
        Generate comprehensive opportunity score
        
        Returns:
            {
                'overall_score': 0.85,
                'category': 'high|medium|low',
                'scores': {
                    'fit_score': 0.9,
                    'likelihood_score': 0.8,
                    'size_score': 0.7,
                    'timing_score': 0.9,
                    'competition_score': 0.6
                },
                'win_probability': 0.75,
                'recommendation': 'pursue|monitor|pass',
                'reasoning': {...}
            }
        """
        # Calculate individual scores
        fit_score = self._score_fit(project, company, db)
        likelihood_score = self._score_likelihood(project, db)
        size_score = self._score_size(project, company)
        timing_score = self._score_timing(project)
        competition_score = self._score_competition(project, db)
        
        # Weighted overall score
        overall = (
            self.weights['fit'] * fit_score +
            self.weights['likelihood'] * likelihood_score +
            self.weights['size'] * size_score +
            self.weights['timing'] * timing_score +
            self.weights['competition'] * competition_score
        )
        
        # Categorize
        if overall >= 0.7:
            category = OpportunityScore.HIGH
            recommendation = 'pursue'
        elif overall >= 0.5:
            category = OpportunityScore.MEDIUM
            recommendation = 'monitor'
        else:
            category = OpportunityScore.LOW
            recommendation = 'pass'
        
        # Get win probability if model is trained
        win_prob = None
        if include_win_prob and win_probability_model.is_trained:
            try:
                win_result = win_probability_model.predict(
                    win_probability_model.prepare_features(project, company, db)
                )
                win_prob = win_result[0]  # Extract probability from tuple
                
                # Adjust recommendation based on win probability
                if win_prob < 0.3:
                    recommendation = 'pass'
                elif win_prob > 0.7 and overall >= 0.6:
                    recommendation = 'pursue'
            except Exception as e:
                logger.warning(f"Could not calculate win probability: {e}")
        
        result = {
            'overall_score': float(overall),
            'category': category,
            'scores': {
                'fit_score': float(fit_score),
                'likelihood_score': float(likelihood_score),
                'size_score': float(size_score),
                'timing_score': float(timing_score),
                'competition_score': float(competition_score)
            },
            'win_probability': float(win_prob) if win_prob else None,
            'recommendation': recommendation,
            'reasoning': self._generate_reasoning(
                project, company, 
                fit_score, likelihood_score, size_score, 
                timing_score, competition_score, win_prob
            )
        }
        
        return result
    
    def _score_fit(self, project: Project, company: Company, db: Session) -> float:
        """
        Score how well project fits company capabilities
        Based on: type match, geographic match, size match, experience
        """
        score = 0.0
        weights = {'type': 0.35, 'geography': 0.25, 'size': 0.20, 'experience': 0.20}
        
        # 1. Project type match
        company_specialties = company.specialties or []
        project_type_str = project.project_type.value if project.project_type else ""
        
        if project_type_str in company_specialties:
            type_score = 1.0
        elif any(spec in project_type_str for spec in company_specialties):
            type_score = 0.7
        else:
            # Check if company has done similar projects
            from app.models.project import ProjectParticipant
            similar_projects = db.query(ProjectParticipant).join(Project).filter(
                ProjectParticipant.company_id == company.id,
                Project.project_type == project.project_type
            ).count()
            type_score = min(similar_projects / 10, 1.0)
        
        score += weights['type'] * type_score
        
        # 2. Geographic fit
        geo_score = 0.0
        if company.headquarters_country == project.country:
            geo_score += 0.5
        if company.headquarters_region == project.region:
            geo_score += 0.5
        
        # Check for regional experience even if not HQ
        from app.models.project import ProjectParticipant
        region_projects = db.query(ProjectParticipant).join(Project).filter(
            ProjectParticipant.company_id == company.id,
            Project.region == project.region
        ).count()
        
        if region_projects > 0:
            geo_score = max(geo_score, min(region_projects / 5, 1.0))
        
        score += weights['geography'] * geo_score
        
        # 3. Size match
        if project.estimated_value and company.average_project_size:
            size_ratio = project.estimated_value / company.average_project_size
            # Prefer projects 0.5x to 2x typical size
            if 0.5 <= size_ratio <= 2.0:
                size_score = 1.0
            elif 0.25 <= size_ratio <= 4.0:
                size_score = 0.7
            else:
                size_score = 0.4
        else:
            size_score = 0.5
        
        score += weights['size'] * size_score
        
        # 4. Overall experience level
        experience_score = min(company.total_projects / 50, 1.0) if company.total_projects else 0.3
        score += weights['experience'] * experience_score
        
        return score
    
    def _score_likelihood(self, project: Project, db: Session) -> float:
        """
        Score likelihood of project going ahead
        Based on: stage, completeness of data, source quality
        """
        score = 0.5  # Base score
        
        # Stage progression (later stages more likely)
        stage_scores = {
            ProjectStage.PLANNING: 0.3,
            ProjectStage.PERMIT: 0.5,
            ProjectStage.TENDER: 0.8,
            ProjectStage.BIDDING: 0.9,
            ProjectStage.AWARDED: 1.0,
            ProjectStage.CONSTRUCTION: 1.0,
            ProjectStage.COMPLETED: 0.0,  # Already done
            ProjectStage.CANCELLED: 0.0
        }
        
        stage_score = stage_scores.get(project.stage, 0.5)
        
        # Data completeness (more complete = more real)
        completeness = 0
        fields = [
            project.owner_company_id,
            project.estimated_value,
            project.start_date,
            project.address,
            project.description
        ]
        completeness = sum(1 for f in fields if f) / len(fields)
        
        # Source quality
        from app.models.project import ProjectSource
        source_scores = {
            ProjectSource.PERMIT: 0.9,
            ProjectSource.TENDER: 1.0,
            ProjectSource.NEWS: 0.7,
            ProjectSource.WEB_SCRAPE: 0.6,
            ProjectSource.MANUAL: 0.8,
            ProjectSource.CLIENT_UPLOAD: 1.0,
            ProjectSource.API_INTEGRATION: 0.9
        }
        
        source_score = source_scores.get(project.source, 0.5)
        
        # Verified projects are more likely
        verified_boost = 0.2 if project.is_verified else 0
        
        # Combine
        score = (
            0.4 * stage_score +
            0.3 * completeness +
            0.2 * source_score +
            0.1 +
            verified_boost
        )
        
        return min(score, 1.0)
    
    def _score_size(self, project: Project, company: Company) -> float:
        """
        Score based on project value and strategic importance
        """
        if not project.estimated_value:
            return 0.5
        
        value = project.estimated_value
        
        # Absolute value scoring (larger = better, but with diminishing returns)
        # Score based on value tiers
        if value < 1_000_000:
            value_score = 0.3
        elif value < 5_000_000:
            value_score = 0.5
        elif value < 25_000_000:
            value_score = 0.7
        elif value < 100_000_000:
            value_score = 0.85
        else:
            value_score = 1.0
        
        # Relative value (compared to company's typical projects)
        if company.average_project_size:
            relative_value = value / company.average_project_size
            # Sweet spot is 1-3x typical size
            if 1.0 <= relative_value <= 3.0:
                relative_score = 1.0
            elif 0.5 <= relative_value <= 5.0:
                relative_score = 0.8
            else:
                relative_score = 0.6
        else:
            relative_score = 0.7
        
        # Combine
        score = 0.6 * value_score + 0.4 * relative_score
        
        return score
    
    def _score_timing(self, project: Project) -> float:
        """
        Score based on timeline urgency and opportunity window
        """
        now = datetime.now()
        
        # Bid deadline scoring
        if project.bid_deadline:
            days_until = (project.bid_deadline - now).days
            
            if days_until < 0:
                return 0.0  # Already passed
            elif days_until < 7:
                return 0.3  # Too urgent
            elif days_until < 30:
                return 1.0  # Perfect window
            elif days_until < 90:
                return 0.8  # Good window
            elif days_until < 180:
                return 0.6  # Reasonable
            else:
                return 0.4  # Too far out
        
        # Start date scoring (if no bid deadline)
        elif project.start_date:
            months_until = (project.start_date - now).days / 30
            
            if months_until < 1:
                return 0.5
            elif months_until < 6:
                return 0.8
            elif months_until < 12:
                return 0.7
            else:
                return 0.5
        
        # No timeline info
        return 0.5
    
    def _score_competition(self, project: Project, db: Session) -> float:
        """
        Score based on expected competitive intensity
        Lower competition = higher score
        """
        from app.models.project import ProjectParticipant
        
        # Check if we know competitors for this project
        known_participants = db.query(ProjectParticipant).filter(
            ProjectParticipant.project_id == project.id
        ).count()
        
        if known_participants > 0:
            # Direct info: more participants = more competition
            if known_participants <= 3:
                return 1.0
            elif known_participants <= 5:
                return 0.8
            elif known_participants <= 8:
                return 0.6
            else:
                return 0.4
        
        # Estimate based on similar projects
        similar = db.query(Project).filter(
            Project.project_type == project.project_type,
            Project.region == project.region,
            Project.stage == project.stage
        ).limit(50).all()
        
        if similar:
            avg_participants = np.mean([
                db.query(ProjectParticipant).filter(
                    ProjectParticipant.project_id == p.id
                ).count()
                for p in similar
            ])
            
            # Normalize to 0-1 (assume 1-10 participants typical)
            competition_score = 1.0 - min(avg_participants / 10, 1.0)
        else:
            # Default moderate competition
            competition_score = 0.6
        
        # High-value projects attract more competition
        if project.estimated_value:
            if project.estimated_value > 100_000_000:
                competition_score *= 0.7  # More competition
            elif project.estimated_value < 5_000_000:
                competition_score *= 1.2  # Less competition
            
            competition_score = min(competition_score, 1.0)
        
        return competition_score
    
    def _generate_reasoning(self, 
                           project: Project,
                           company: Company,
                           fit: float, likelihood: float, size: float,
                           timing: float, competition: float,
                           win_prob: Optional[float]) -> Dict:
        """Generate human-readable reasoning for the score"""
        reasoning = {
            'strengths': [],
            'concerns': [],
            'key_factors': {}
        }
        
        # Identify strengths
        if fit >= 0.7:
            reasoning['strengths'].append(f"Strong fit with {company.name}'s capabilities")
        if likelihood >= 0.7:
            reasoning['strengths'].append("High likelihood of proceeding")
        if size >= 0.7:
            reasoning['strengths'].append("Good project size match")
        if timing >= 0.7:
            reasoning['strengths'].append("Favorable timeline")
        if competition >= 0.7:
            reasoning['strengths'].append("Lower competitive intensity")
        if win_prob and win_prob >= 0.7:
            reasoning['strengths'].append(f"High win probability ({win_prob:.0%})")
        
        # Identify concerns
        if fit < 0.5:
            reasoning['concerns'].append("Limited experience in this project type or region")
        if likelihood < 0.5:
            reasoning['concerns'].append("Uncertain if project will proceed")
        if size < 0.5:
            reasoning['concerns'].append("Project size outside typical range")
        if timing < 0.5:
            reasoning['concerns'].append("Timeline may be too tight or too far out")
        if competition < 0.5:
            reasoning['concerns'].append("Expected high competition")
        if win_prob and win_prob < 0.4:
            reasoning['concerns'].append(f"Low win probability ({win_prob:.0%})")
        
        # Key factors
        reasoning['key_factors'] = {
            'fit': 'high' if fit >= 0.7 else 'medium' if fit >= 0.5 else 'low',
            'likelihood': 'high' if likelihood >= 0.7 else 'medium' if likelihood >= 0.5 else 'low',
            'size': 'good' if size >= 0.7 else 'acceptable' if size >= 0.5 else 'poor',
            'timing': 'urgent' if timing >= 0.8 else 'good' if timing >= 0.6 else 'distant',
            'competition': 'low' if competition >= 0.7 else 'moderate' if competition >= 0.5 else 'high'
        }
        
        return reasoning
    
    def score_batch(self, 
                   projects: List[Project],
                   company: Company,
                   db: Session) -> pd.DataFrame:
        """Score multiple opportunities and return ranked list"""
        import pandas as pd
        
        results = []
        for project in projects:
            score = self.score_opportunity(project, company, db, include_win_prob=False)
            results.append({
                'project_id': project.id,
                'project_title': project.title,
                'project_type': project.project_type.value if project.project_type else None,
                'estimated_value': project.estimated_value,
                'overall_score': score['overall_score'],
                'category': score['category'].value,
                'recommendation': score['recommendation'],
                **score['scores']
            })
        
        df = pd.DataFrame(results)
        df = df.sort_values('overall_score', ascending=False)
        
        return df


# Global scorer instance
opportunity_scorer = OpportunityScorer()


def score_opportunity(project: Project, company: Company, db: Session) -> Dict:
    """
    Convenience function for opportunity scoring
    
    Example:
        score = score_opportunity(project, my_company, db)
        print(score['recommendation'])  # 'pursue'
        print(score['overall_score'])   # 0.85
    """
    return opportunity_scorer.score_opportunity(project, company, db)
