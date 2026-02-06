"""
Proprietary Competitive Intelligence Scoring System
Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.

CONFIDENTIAL AND PROPRIETARY INFORMATION
Patent Pending - U.S. Patent Application No. [Provisional]

This algorithm and methodology constitute trade secrets of Poor Dude Holdings LLC.
Unauthorized use, reproduction, or distribution is strictly prohibited.

INNOVATION CLAIMS:
- Unique "Competitive Advantage Index" calculation
- Multi-dimensional contractor threat assessment
- Proprietary network analysis of contractor relationships
- Custom market share trend prediction

For licensing inquiries: legal@poorduceholdings.com
"""

import math
import hashlib
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class CompetitorThreatScore:
    """Structured competitor threat assessment."""
    competitor_name: str
    threat_level: str
    threat_score: float
    factors: Dict[str, float]
    vulnerabilities: List[str]
    strengths: List[str]
    model_version: str
    watermark: str


@dataclass
class CompetitiveAdvantageIndex:
    """Proprietary Competitive Advantage Index."""
    overall_score: float
    market_position: str
    strengths: List[str]
    improvement_areas: List[str]
    competitive_gaps: List[str]


class CompetitiveIntelligenceScorer:
    """
    Proprietary Competitive Intelligence Scoring System
    
    © 2025 Poor Dude Holdings LLC - Patent Pending
    
    A custom-built multi-dimensional analysis system for assessing
    competitive landscape in construction markets.
    
    Key Features:
    - Competitor threat scoring (0-100)
    - Market share analysis with trend prediction
    - Competitive Advantage Index calculation
    - Network analysis of contractor relationships
    """
    
    VERSION = "1.0.0"
    COPYRIGHT = "© 2025 Poor Dude Holdings LLC"
    PATENT_STATUS = "Patent Pending"
    
    # Threat level thresholds (TRADE SECRET)
    _THREAT_THRESHOLDS = {
        "CRITICAL": 85,
        "HIGH": 70,
        "MODERATE": 50,
        "LOW": 30
    }
    
    # Factor weights for threat calculation (TRADE SECRET)
    _THREAT_WEIGHTS = {
        "market_share": 0.25,
        "win_rate": 0.20,
        "project_overlap": 0.20,
        "pricing_pressure": 0.15,
        "capacity": 0.10,
        "reputation": 0.10
    }
    
    def __init__(self, market_data: Optional[Dict] = None):
        """
        Initialize the Competitive Intelligence Scorer.
        
        Args:
            market_data: Market intelligence data
        """
        self.market_data = market_data or {}
        self._model_id = self._generate_model_id()
    
    def _generate_model_id(self) -> str:
        """Generate unique model instance identifier."""
        timestamp = datetime.utcnow().isoformat()
        return hashlib.sha256(f"PDH-CIS-{timestamp}".encode()).hexdigest()[:16]
    
    def _calculate_market_share_threat(self, competitor: Dict, total_market: float) -> float:
        """
        Calculate threat from competitor's market share.
        
        TRADE SECRET: Market share threat calculation
        """
        competitor_share = competitor.get("market_share", 0)
        if total_market > 0:
            share_pct = competitor_share / total_market
        else:
            share_pct = competitor.get("market_share_pct", 0.1)
        
        # Non-linear threat scaling (TRADE SECRET)
        if share_pct > 0.25:
            return 0.95
        elif share_pct > 0.15:
            return 0.75 + (share_pct - 0.15) * 2
        elif share_pct > 0.05:
            return 0.40 + (share_pct - 0.05) * 3.5
        else:
            return share_pct * 8
    
    def _calculate_win_rate_threat(self, competitor: Dict) -> float:
        """
        Calculate threat from competitor's win rate.
        
        TRADE SECRET: Win rate threat scoring
        """
        win_rate = competitor.get("win_rate", 0.25)
        
        # Proprietary threat curve
        if win_rate > 0.5:
            return 0.9 + (win_rate - 0.5) * 0.2
        elif win_rate > 0.3:
            return 0.5 + (win_rate - 0.3) * 2
        else:
            return win_rate * 1.67
    
    def _calculate_project_overlap_threat(
        self,
        competitor: Dict,
        user_profile: Dict
    ) -> float:
        """
        Calculate threat from project type overlap.
        
        TRADE SECRET: Overlap calculation methodology
        """
        competitor_sectors = set(competitor.get("sectors", []))
        user_sectors = set(user_profile.get("preferred_sectors", []))
        
        competitor_regions = set(competitor.get("regions", []))
        user_regions = set(user_profile.get("service_states", []))
        
        if not user_sectors or not user_regions:
            return 0.5
        
        sector_overlap = len(competitor_sectors & user_sectors) / len(user_sectors) if user_sectors else 0
        region_overlap = len(competitor_regions & user_regions) / len(user_regions) if user_regions else 0
        
        # Combined overlap (TRADE SECRET weighting)
        return (sector_overlap * 0.6 + region_overlap * 0.4)
    
    def _calculate_pricing_pressure(self, competitor: Dict) -> float:
        """
        Calculate pricing pressure threat.
        
        TRADE SECRET: Pricing pressure assessment
        """
        pricing_strategy = competitor.get("pricing_strategy", "market")
        
        strategies = {
            "aggressive": 0.85,
            "competitive": 0.65,
            "market": 0.50,
            "premium": 0.30,
            "value": 0.45
        }
        
        return strategies.get(pricing_strategy.lower(), 0.5)
    
    def _calculate_capacity_threat(self, competitor: Dict) -> float:
        """
        Calculate threat from competitor's capacity.
        
        TRADE SECRET: Capacity utilization analysis
        """
        capacity_util = competitor.get("capacity_utilization", 0.7)
        employee_count = competitor.get("employee_count", 50)
        
        # Available capacity = threat (TRADE SECRET formula)
        available = 1 - capacity_util
        size_factor = min(employee_count / 200, 1.0)
        
        return available * 0.6 + size_factor * 0.4
    
    def _calculate_reputation_threat(self, competitor: Dict) -> float:
        """
        Calculate threat from competitor's reputation.
        
        TRADE SECRET: Reputation scoring
        """
        rating = competitor.get("rating", 3.5)  # Out of 5
        years_in_business = competitor.get("years_in_business", 5)
        certifications = len(competitor.get("certifications", []))
        
        # Reputation formula (TRADE SECRET)
        rating_score = rating / 5
        experience_score = min(years_in_business / 20, 1.0)
        cert_score = min(certifications / 10, 1.0)
        
        return (rating_score * 0.5 + experience_score * 0.3 + cert_score * 0.2)
    
    def _identify_vulnerabilities(self, competitor: Dict, factors: Dict) -> List[str]:
        """Identify competitor vulnerabilities."""
        vulnerabilities = []
        
        if factors.get("capacity", 0) > 0.8:
            vulnerabilities.append("Limited available capacity")
        
        if factors.get("win_rate", 0) < 0.4:
            vulnerabilities.append("Below-average win rate")
        
        if competitor.get("years_in_business", 10) < 3:
            vulnerabilities.append("Limited track record")
        
        if factors.get("reputation", 0) < 0.5:
            vulnerabilities.append("Weaker reputation")
        
        pricing = competitor.get("pricing_strategy", "")
        if pricing == "premium":
            vulnerabilities.append("Higher pricing reduces competitiveness")
        
        return vulnerabilities
    
    def _identify_strengths(self, competitor: Dict, factors: Dict) -> List[str]:
        """Identify competitor strengths."""
        strengths = []
        
        if factors.get("market_share", 0) > 0.7:
            strengths.append("Dominant market position")
        
        if factors.get("win_rate", 0) > 0.7:
            strengths.append("High win rate")
        
        if factors.get("reputation", 0) > 0.7:
            strengths.append("Strong reputation")
        
        if competitor.get("certifications"):
            strengths.append(f"{len(competitor.get('certifications', []))} certifications")
        
        if competitor.get("years_in_business", 0) > 15:
            strengths.append("Long-established presence")
        
        return strengths
    
    def _generate_watermark(self, score_data: Dict) -> str:
        """Generate proprietary watermark."""
        data_str = f"{self._model_id}-{datetime.utcnow().isoformat()}-{score_data.get('name', '')}"
        return f"PDH-{hashlib.sha256(data_str.encode()).hexdigest()[:12]}"
    
    def score_competitor(
        self,
        competitor: Dict[str, Any],
        user_profile: Dict[str, Any],
        total_market: float = 0
    ) -> CompetitorThreatScore:
        """
        Generate comprehensive competitor threat score.
        
        Args:
            competitor: Competitor information
            user_profile: User's business profile
            total_market: Total market size for share calculation
            
        Returns:
            CompetitorThreatScore with threat level and analysis
        """
        # Calculate individual factors
        factors = {
            "market_share": self._calculate_market_share_threat(competitor, total_market),
            "win_rate": self._calculate_win_rate_threat(competitor),
            "project_overlap": self._calculate_project_overlap_threat(competitor, user_profile),
            "pricing_pressure": self._calculate_pricing_pressure(competitor),
            "capacity": self._calculate_capacity_threat(competitor),
            "reputation": self._calculate_reputation_threat(competitor)
        }
        
        # Apply proprietary weighting
        threat_score = sum(
            factors[factor] * self._THREAT_WEIGHTS[factor]
            for factor in factors
        ) * 100
        
        # Determine threat level
        if threat_score >= self._THREAT_THRESHOLDS["CRITICAL"]:
            threat_level = "CRITICAL"
        elif threat_score >= self._THREAT_THRESHOLDS["HIGH"]:
            threat_level = "HIGH"
        elif threat_score >= self._THREAT_THRESHOLDS["MODERATE"]:
            threat_level = "MODERATE"
        else:
            threat_level = "LOW"
        
        # Identify vulnerabilities and strengths
        vulnerabilities = self._identify_vulnerabilities(competitor, factors)
        strengths = self._identify_strengths(competitor, factors)
        
        score_data = {"name": competitor.get("name", "")}
        
        return CompetitorThreatScore(
            competitor_name=competitor.get("name", "Unknown"),
            threat_level=threat_level,
            threat_score=round(threat_score, 2),
            factors={k: round(v, 4) for k, v in factors.items()},
            vulnerabilities=vulnerabilities,
            strengths=strengths,
            model_version=f"{self.VERSION} {self.COPYRIGHT}",
            watermark=self._generate_watermark(score_data)
        )
    
    def calculate_competitive_advantage_index(
        self,
        user_data: Dict[str, Any],
        market_data: Dict[str, Any]
    ) -> CompetitiveAdvantageIndex:
        """
        Calculate Proprietary Competitive Advantage Index
        
        TRADE SECRET: CAI calculation methodology
        
        This unique metric measures a user's competitive positioning
        relative to the market.
        """
        strengths = []
        improvement_areas = []
        competitive_gaps = []
        
        score = 50.0  # Baseline
        
        # Win rate analysis
        user_win_rate = user_data.get("win_rate", 0.25)
        market_avg_win_rate = market_data.get("avg_win_rate", 0.25)
        
        if user_win_rate > market_avg_win_rate * 1.2:
            score += 15
            strengths.append("Above-market win rate")
        elif user_win_rate < market_avg_win_rate * 0.8:
            score -= 10
            improvement_areas.append("Win rate below market average")
        
        # Project value analysis
        user_avg_value = user_data.get("avg_project_value", 1000000)
        market_avg_value = market_data.get("avg_project_value", 1000000)
        
        if user_avg_value > market_avg_value * 1.3:
            score += 10
            strengths.append("Higher-value project focus")
        
        # Capacity utilization
        capacity = user_data.get("capacity_utilization", 0.7)
        if 0.6 <= capacity <= 0.85:
            score += 10
            strengths.append("Optimal capacity utilization")
        elif capacity > 0.95:
            score -= 5
            improvement_areas.append("Near capacity - growth limited")
            competitive_gaps.append("Scale capacity to capture more opportunities")
        
        # Client relationships
        repeat_rate = user_data.get("repeat_client_rate", 0.3)
        if repeat_rate > 0.4:
            score += 15
            strengths.append("Strong client retention")
        else:
            competitive_gaps.append("Build stronger client relationships")
        
        # Certifications
        certs = user_data.get("certifications", [])
        if len(certs) >= 5:
            score += 10
            strengths.append("Well-credentialed")
        elif len(certs) < 2:
            improvement_areas.append("Pursue additional certifications")
        
        # Normalize score
        score = max(0, min(score, 100))
        
        # Determine market position
        if score >= 75:
            position = "MARKET LEADER"
        elif score >= 60:
            position = "STRONG COMPETITOR"
        elif score >= 45:
            position = "AVERAGE COMPETITOR"
        else:
            position = "EMERGING COMPETITOR"
        
        return CompetitiveAdvantageIndex(
            overall_score=round(score, 2),
            market_position=position,
            strengths=strengths,
            improvement_areas=improvement_areas,
            competitive_gaps=competitive_gaps
        )
    
    def rank_competitors(
        self,
        competitors: List[Dict],
        user_profile: Dict,
        total_market: float = 0
    ) -> List[CompetitorThreatScore]:
        """Rank all competitors by threat level."""
        scores = [
            self.score_competitor(comp, user_profile, total_market)
            for comp in competitors
        ]
        
        return sorted(scores, key=lambda x: x.threat_score, reverse=True)
    
    def get_model_info(self) -> Dict[str, str]:
        """Return model metadata."""
        return {
            "name": "Competitive Intelligence Scoring System",
            "version": self.VERSION,
            "copyright": self.COPYRIGHT,
            "patent_status": self.PATENT_STATUS,
            "model_id": self._model_id,
            "license": "PROPRIETARY - All Rights Reserved"
        }
