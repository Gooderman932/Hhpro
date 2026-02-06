"""
Proprietary Win Probability Prediction Model
Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.

CONFIDENTIAL AND PROPRIETARY INFORMATION
Patent Pending - U.S. Patent Application No. [Provisional]

This algorithm and methodology constitute trade secrets of Poor Dude Holdings LLC.
Unauthorized use, reproduction, or distribution is strictly prohibited.

INNOVATION CLAIMS:
- Novel multi-factor bid success prediction for construction industry
- Proprietary competitive pressure scoring methodology
- Custom contractor-project fit assessment algorithm
- Adaptive learning from historical bid outcomes

For licensing inquiries: legal@poorduceholdings.com
"""

import math
import hashlib
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class WinPrediction:
    """Structured win probability prediction result."""
    probability: float
    confidence: float
    factors: Dict[str, float]
    recommendation: str
    explanation: str
    model_version: str
    watermark: str


class WinProbabilityModel:
    """
    Proprietary Win Probability Prediction Model
    
    © 2025 Poor Dude Holdings LLC - Patent Pending
    
    A custom-built neural network-inspired model for predicting
    construction bid success probability based on multi-factor analysis.
    
    Key Features:
    - Project-contractor fit scoring
    - Competitive pressure analysis
    - Historical performance weighting
    - Regional market adjustment
    - Temporal factors consideration
    """
    
    VERSION = "1.0.0"
    COPYRIGHT = "© 2025 Poor Dude Holdings LLC"
    PATENT_STATUS = "Patent Pending"
    
    # Proprietary weight configurations (TRADE SECRET)
    _WEIGHTS = {
        "project_fit": 0.25,
        "competitive_pressure": 0.20,
        "historical_performance": 0.20,
        "market_conditions": 0.15,
        "timing_factors": 0.10,
        "relationship_strength": 0.10
    }
    
    # Proprietary threshold values (TRADE SECRET)
    _THRESHOLDS = {
        "high_probability": 0.70,
        "moderate_probability": 0.45,
        "low_probability": 0.25
    }
    
    def __init__(self, user_history: Optional[List[Dict]] = None):
        """
        Initialize the Win Probability Model.
        
        Args:
            user_history: Historical bid data for adaptive learning
        """
        self.user_history = user_history or []
        self._calibration_factor = self._calculate_calibration()
        self._model_id = self._generate_model_id()
    
    def _generate_model_id(self) -> str:
        """Generate unique model instance identifier for tracking."""
        timestamp = datetime.utcnow().isoformat()
        return hashlib.sha256(f"PDH-WPM-{timestamp}".encode()).hexdigest()[:16]
    
    def _calculate_calibration(self) -> float:
        """
        Proprietary calibration based on user's historical performance.
        
        TRADE SECRET: Calibration methodology
        """
        if not self.user_history:
            return 1.0
        
        wins = sum(1 for h in self.user_history if h.get("outcome") == "won")
        total = len(self.user_history)
        
        if total < 5:
            return 1.0
        
        historical_rate = wins / total
        # Proprietary calibration formula
        return 0.7 + (historical_rate * 0.6)
    
    def _score_project_fit(self, project: Dict, user_profile: Dict) -> float:
        """
        Proprietary Project-Contractor Fit Scoring Algorithm
        
        TRADE SECRET: Fit scoring methodology
        
        Factors:
        - Sector alignment
        - Value range match
        - Geographic proximity
        - Trade specialty alignment
        """
        score = 0.5  # Base score
        
        # Sector alignment (proprietary weighting)
        project_sector = project.get("sector", "").lower()
        preferred_sectors = [s.lower() for s in user_profile.get("preferred_sectors", [])]
        if project_sector in preferred_sectors:
            score += 0.25
        
        # Value range optimization (proprietary formula)
        project_value = project.get("value", 0)
        min_val = user_profile.get("min_project_value", 0)
        max_val = user_profile.get("max_project_value", float("inf"))
        
        if min_val <= project_value <= max_val:
            # Sweet spot calculation (TRADE SECRET)
            midpoint = (min_val + max_val) / 2
            deviation = abs(project_value - midpoint) / midpoint if midpoint else 0
            score += max(0, 0.15 * (1 - deviation))
        
        # Geographic proximity (proprietary scoring)
        project_state = project.get("state", "")
        service_states = user_profile.get("service_states", [])
        if project_state in service_states:
            score += 0.15
        
        # Trade alignment
        project_desc = f"{project.get('name', '')} {project.get('description', '')}".lower()
        trade = user_profile.get("trade_specialty", "").lower()
        if trade and trade in project_desc:
            score += 0.20
        
        return min(score, 1.0)
    
    def _score_competitive_pressure(self, project: Dict, market_data: Optional[Dict] = None) -> float:
        """
        Proprietary Competitive Pressure Analysis
        
        TRADE SECRET: Competitive pressure scoring algorithm
        
        Factors:
        - Number of expected bidders
        - Market saturation level
        - Project attractiveness score
        """
        base_pressure = 0.5
        
        # Expected bidders impact (proprietary formula)
        bidders = project.get("expected_bidders", 5)
        if bidders:
            # Inverse logarithmic scaling (TRADE SECRET)
            bidder_factor = 1 / (1 + math.log(max(bidders, 1)))
            base_pressure = base_pressure * (1 + bidder_factor)
        
        # Project value attractiveness (TRADE SECRET)
        value = project.get("value", 1000000)
        if value > 10000000:
            base_pressure *= 0.85  # High-value = more competition
        elif value < 500000:
            base_pressure *= 1.1  # Lower value = less competition
        
        # Market conditions adjustment
        if market_data:
            saturation = market_data.get("market_saturation", 0.5)
            base_pressure *= (1 - (saturation * 0.2))
        
        return min(max(1 - base_pressure, 0), 1.0)
    
    def _score_historical_performance(self, user_profile: Dict) -> float:
        """
        Proprietary Historical Performance Scoring
        
        TRADE SECRET: Performance weighting algorithm
        """
        if not self.user_history:
            return 0.5  # Neutral for new users
        
        recent_history = self.user_history[-20:]  # Last 20 bids
        wins = sum(1 for h in recent_history if h.get("outcome") == "won")
        
        if len(recent_history) < 3:
            return 0.5
        
        win_rate = wins / len(recent_history)
        
        # Proprietary performance curve (TRADE SECRET)
        # Non-linear transformation for realistic scoring
        return 0.3 + (win_rate * 0.6) + (win_rate ** 2 * 0.1)
    
    def _score_market_conditions(self, project: Dict, economic_data: Optional[Dict] = None) -> float:
        """
        Proprietary Market Conditions Analysis
        
        TRADE SECRET: Economic factor integration
        """
        base_score = 0.5
        
        project_sector = project.get("sector", "")
        project_state = project.get("state", "")
        
        # Sector-specific adjustments (TRADE SECRET)
        sector_factors = {
            "Healthcare": 0.15,  # Strong demand
            "Industrial": 0.10,
            "Commercial": 0.05,
            "Residential": 0.00,
            "Retail": -0.05,
            "Education": 0.10
        }
        base_score += sector_factors.get(project_sector, 0)
        
        # Regional adjustments (TRADE SECRET)
        hot_markets = ["TX", "FL", "AZ", "NC", "TN"]
        if project_state in hot_markets:
            base_score += 0.10
        
        # Economic indicator integration
        if economic_data:
            construction_trend = economic_data.get("construction_trend", 0)
            base_score += construction_trend * 0.1
        
        return min(max(base_score, 0), 1.0)
    
    def _score_timing_factors(self, project: Dict) -> float:
        """
        Proprietary Timing Analysis
        
        TRADE SECRET: Temporal factor scoring
        """
        score = 0.5
        
        # Seasonal adjustments (construction industry specific)
        current_month = datetime.now().month
        
        # Peak season bonus (TRADE SECRET thresholds)
        if current_month in [3, 4, 5, 9, 10]:  # Spring & Fall
            score += 0.15
        elif current_month in [6, 7, 8]:  # Summer
            score += 0.10
        elif current_month in [11, 12, 1, 2]:  # Winter
            score -= 0.05
        
        # Project timeline assessment
        bid_date = project.get("bid_date")
        if bid_date:
            try:
                bid_dt = datetime.fromisoformat(str(bid_date).replace("Z", ""))
                days_to_bid = (bid_dt - datetime.now()).days
                
                # Optimal preparation window (TRADE SECRET)
                if 14 <= days_to_bid <= 45:
                    score += 0.10
                elif days_to_bid < 7:
                    score -= 0.15
            except:
                pass
        
        return min(max(score, 0), 1.0)
    
    def _score_relationship_strength(self, project: Dict, user_data: Optional[Dict] = None) -> float:
        """
        Proprietary Relationship Scoring
        
        TRADE SECRET: Client relationship factor
        """
        if not user_data:
            return 0.5
        
        score = 0.5
        
        # Check if project owner is existing client
        project_owner = project.get("owner_name", "").lower()
        clients = user_data.get("clients", [])
        
        for client in clients:
            if client.get("company_name", "").lower() in project_owner:
                relationship_strength = client.get("relationship_strength", 5) / 10
                score += relationship_strength * 0.4
                break
        
        return min(score, 1.0)
    
    def _generate_watermark(self, prediction_data: Dict) -> str:
        """Generate proprietary watermark for output verification."""
        data_str = f"{self._model_id}-{datetime.utcnow().isoformat()}-{prediction_data.get('probability', 0)}"
        return f"PDH-{hashlib.sha256(data_str.encode()).hexdigest()[:12]}"
    
    def _generate_explanation(self, factors: Dict[str, float], probability: float) -> str:
        """Generate human-readable explanation of prediction."""
        explanations = []
        
        if factors["project_fit"] > 0.7:
            explanations.append("Strong project-profile alignment")
        elif factors["project_fit"] < 0.4:
            explanations.append("Limited project-profile fit")
        
        if factors["competitive_pressure"] > 0.6:
            explanations.append("favorable competitive landscape")
        elif factors["competitive_pressure"] < 0.4:
            explanations.append("high competitive pressure expected")
        
        if factors["historical_performance"] > 0.6:
            explanations.append("strong historical win rate")
        
        if factors["market_conditions"] > 0.6:
            explanations.append("positive market conditions")
        
        if not explanations:
            explanations.append("balanced factors across all dimensions")
        
        return "; ".join(explanations).capitalize()
    
    def predict(
        self,
        project: Dict[str, Any],
        user_profile: Dict[str, Any],
        market_data: Optional[Dict] = None,
        economic_data: Optional[Dict] = None,
        user_data: Optional[Dict] = None
    ) -> WinPrediction:
        """
        Generate win probability prediction.
        
        Proprietary algorithm combining multiple factors with
        custom weighting and calibration.
        
        Args:
            project: Project details
            user_profile: User's business profile
            market_data: Optional market intelligence data
            economic_data: Optional economic indicators
            user_data: Optional user's client/relationship data
            
        Returns:
            WinPrediction with probability, confidence, and explanation
        """
        # Calculate individual factor scores
        factors = {
            "project_fit": self._score_project_fit(project, user_profile),
            "competitive_pressure": self._score_competitive_pressure(project, market_data),
            "historical_performance": self._score_historical_performance(user_profile),
            "market_conditions": self._score_market_conditions(project, economic_data),
            "timing_factors": self._score_timing_factors(project),
            "relationship_strength": self._score_relationship_strength(project, user_data)
        }
        
        # Apply proprietary weighting (TRADE SECRET)
        weighted_sum = sum(
            factors[factor] * self._WEIGHTS[factor]
            for factor in factors
        )
        
        # Apply calibration
        calibrated_probability = weighted_sum * self._calibration_factor
        
        # Normalize to 0-1 range
        probability = min(max(calibrated_probability, 0.05), 0.95)
        
        # Calculate confidence based on factor agreement (TRADE SECRET)
        factor_variance = sum((f - probability) ** 2 for f in factors.values()) / len(factors)
        confidence = max(0.5, 1 - (factor_variance * 2))
        
        # Generate recommendation
        if probability >= self._THRESHOLDS["high_probability"]:
            recommendation = "STRONG PURSUE"
        elif probability >= self._THRESHOLDS["moderate_probability"]:
            recommendation = "PURSUE"
        elif probability >= self._THRESHOLDS["low_probability"]:
            recommendation = "EVALUATE"
        else:
            recommendation = "PASS"
        
        # Generate explanation
        explanation = self._generate_explanation(factors, probability)
        
        # Create prediction with watermark
        prediction_data = {"probability": probability, "factors": factors}
        watermark = self._generate_watermark(prediction_data)
        
        return WinPrediction(
            probability=round(probability, 4),
            confidence=round(confidence, 4),
            factors={k: round(v, 4) for k, v in factors.items()},
            recommendation=recommendation,
            explanation=explanation,
            model_version=f"{self.VERSION} {self.COPYRIGHT}",
            watermark=watermark
        )
    
    def batch_predict(
        self,
        projects: List[Dict],
        user_profile: Dict,
        **kwargs
    ) -> List[WinPrediction]:
        """Generate predictions for multiple projects."""
        return [
            self.predict(project, user_profile, **kwargs)
            for project in projects
        ]
    
    def get_model_info(self) -> Dict[str, str]:
        """Return model metadata."""
        return {
            "name": "Win Probability Prediction Model",
            "version": self.VERSION,
            "copyright": self.COPYRIGHT,
            "patent_status": self.PATENT_STATUS,
            "model_id": self._model_id,
            "license": "PROPRIETARY - All Rights Reserved"
        }
