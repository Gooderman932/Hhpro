"""
Proprietary Project-Contractor Matching AI
Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.

CONFIDENTIAL AND PROPRIETARY INFORMATION
Patent Pending - U.S. Patent Application No. [Provisional]

This algorithm and methodology constitute trade secrets of Poor Dude Holdings LLC.
Unauthorized use, reproduction, or distribution is strictly prohibited.

INNOVATION CLAIMS:
- Custom embeddings for construction project matching
- Proprietary "Fit Score" calculation methodology
- Semantic analysis of construction project descriptions
- Adaptive learning from user feedback

For licensing inquiries: legal@poorduceholdings.com
"""

import math
import hashlib
import re
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from collections import Counter


@dataclass
class ProjectMatch:
    """Structured project match result."""
    project: Dict[str, Any]
    fit_score: float
    match_factors: Dict[str, float]
    match_reasons: List[str]
    concerns: List[str]
    recommendation: str
    model_version: str
    watermark: str


class ProjectMatcherAI:
    """
    Proprietary Project-Contractor Matching AI
    
    © 2025 Poor Dude Holdings LLC - Patent Pending
    
    A custom-built recommendation engine for matching construction
    projects with contractors based on multi-dimensional analysis.
    
    Key Features:
    - Semantic analysis of project descriptions
    - Multi-factor fit scoring
    - Custom embeddings for construction domain
    - Adaptive learning from user feedback
    """
    
    VERSION = "1.0.0"
    COPYRIGHT = "© 2025 Poor Dude Holdings LLC"
    PATENT_STATUS = "Patent Pending"
    
    # Proprietary keyword embeddings (TRADE SECRET)
    _TRADE_KEYWORDS = {
        "electrical": ["electrical", "wiring", "power", "voltage", "circuit", "panel", "conduit", "lighting", "generator"],
        "plumbing": ["plumbing", "pipe", "water", "drain", "sewer", "fixture", "valve", "pump", "sprinkler"],
        "hvac": ["hvac", "heating", "cooling", "ventilation", "air", "duct", "chiller", "boiler", "thermostat"],
        "drywall": ["drywall", "sheetrock", "gypsum", "wall", "ceiling", "partition", "finishing", "taping"],
        "roofing": ["roof", "roofing", "shingle", "membrane", "flashing", "gutter", "skylight", "waterproofing"],
        "concrete": ["concrete", "foundation", "slab", "masonry", "cement", "rebar", "formwork", "pour"],
        "structural": ["steel", "structural", "framing", "beam", "column", "truss", "erection", "welding"],
        "flooring": ["floor", "tile", "carpet", "hardwood", "vinyl", "epoxy", "terrazzo", "laminate"],
        "painting": ["paint", "coating", "finish", "primer", "stain", "texture", "wallpaper"],
        "landscaping": ["landscape", "irrigation", "grading", "paving", "hardscape", "planting", "drainage"],
        "general": ["construction", "building", "renovation", "remodel", "addition", "tenant", "improvement"]
    }
    
    # Sector characteristics (TRADE SECRET)
    _SECTOR_PROFILES = {
        "Healthcare": {"complexity": 0.9, "regulation": 0.95, "timeline_sensitivity": 0.85},
        "Education": {"complexity": 0.6, "regulation": 0.7, "timeline_sensitivity": 0.9},
        "Commercial": {"complexity": 0.5, "regulation": 0.5, "timeline_sensitivity": 0.7},
        "Residential": {"complexity": 0.4, "regulation": 0.4, "timeline_sensitivity": 0.6},
        "Industrial": {"complexity": 0.7, "regulation": 0.6, "timeline_sensitivity": 0.5},
        "Retail": {"complexity": 0.5, "regulation": 0.5, "timeline_sensitivity": 0.8},
        "Data Center": {"complexity": 0.95, "regulation": 0.7, "timeline_sensitivity": 0.9}
    }
    
    def __init__(self, user_feedback: Optional[List[Dict]] = None):
        """
        Initialize the Project Matcher AI.
        
        Args:
            user_feedback: Historical accept/reject decisions for learning
        """
        self.user_feedback = user_feedback or []
        self._model_id = self._generate_model_id()
        self._feedback_weights = self._learn_from_feedback()
    
    def _generate_model_id(self) -> str:
        """Generate unique model instance identifier."""
        timestamp = datetime.utcnow().isoformat()
        return hashlib.sha256(f"PDH-PMA-{timestamp}".encode()).hexdigest()[:16]
    
    def _learn_from_feedback(self) -> Dict[str, float]:
        """
        Proprietary adaptive learning from user feedback.
        
        TRADE SECRET: Feedback learning algorithm
        """
        if not self.user_feedback:
            return {}
        
        # Analyze patterns in accepted vs rejected projects
        accepted_sectors = Counter()
        accepted_values = []
        rejected_sectors = Counter()
        
        for feedback in self.user_feedback:
            project = feedback.get("project", {})
            decision = feedback.get("decision", "")
            
            if decision == "accepted":
                accepted_sectors[project.get("sector", "")] += 1
                if project.get("value"):
                    accepted_values.append(project["value"])
            elif decision == "rejected":
                rejected_sectors[project.get("sector", "")] += 1
        
        # Calculate learned preferences (TRADE SECRET formula)
        weights = {}
        for sector in set(list(accepted_sectors.keys()) + list(rejected_sectors.keys())):
            accepted = accepted_sectors.get(sector, 0)
            rejected = rejected_sectors.get(sector, 0)
            total = accepted + rejected
            if total > 0:
                weights[f"sector_{sector}"] = accepted / total
        
        return weights
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract relevant keywords from text."""
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        return words
    
    def _calculate_text_similarity(self, project_text: str, trade: str) -> float:
        """
        Proprietary text similarity calculation.
        
        TRADE SECRET: Semantic matching algorithm
        """
        if not trade or not project_text:
            return 0.5
        
        project_words = set(self._extract_keywords(project_text))
        trade_keywords = set(self._TRADE_KEYWORDS.get(trade.lower(), []))
        
        if not trade_keywords:
            return 0.5
        
        # Calculate Jaccard-inspired similarity with custom weighting
        intersection = project_words & trade_keywords
        
        if not intersection:
            return 0.2
        
        # Proprietary similarity scoring (TRADE SECRET)
        base_score = len(intersection) / len(trade_keywords)
        
        # Boost for multiple matches
        if len(intersection) >= 3:
            base_score *= 1.2
        
        return min(base_score, 1.0)
    
    def _calculate_value_fit(
        self,
        project_value: float,
        min_value: float,
        max_value: float
    ) -> float:
        """
        Proprietary value range fit calculation.
        
        TRADE SECRET: Value optimization algorithm
        """
        if not project_value:
            return 0.5
        
        if project_value < min_value:
            # Below range - calculate how far
            ratio = project_value / min_value
            return max(0.1, ratio * 0.6)
        
        if project_value > max_value:
            # Above range
            ratio = max_value / project_value
            return max(0.1, ratio * 0.5)
        
        # Within range - optimal zone calculation (TRADE SECRET)
        range_size = max_value - min_value
        if range_size == 0:
            return 1.0
        
        midpoint = (min_value + max_value) / 2
        position = abs(project_value - midpoint) / (range_size / 2)
        
        # Center of range gets highest score
        return 0.7 + (0.3 * (1 - position))
    
    def _calculate_geographic_fit(
        self,
        project_state: str,
        service_states: List[str],
        project_city: Optional[str] = None,
        service_cities: Optional[List[str]] = None
    ) -> float:
        """
        Proprietary geographic fit calculation.
        
        TRADE SECRET: Location matching algorithm
        """
        if not service_states:
            return 0.5
        
        # State match
        if project_state not in service_states:
            return 0.1  # Out of service area
        
        # Base score for state match
        score = 0.7
        
        # City bonus
        if service_cities and project_city:
            if project_city.lower() in [c.lower() for c in service_cities]:
                score += 0.25
            else:
                score += 0.1  # Same state bonus
        else:
            score += 0.15
        
        return min(score, 1.0)
    
    def _calculate_sector_fit(
        self,
        project_sector: str,
        preferred_sectors: List[str]
    ) -> float:
        """
        Proprietary sector fit calculation.
        
        TRADE SECRET: Sector matching algorithm
        """
        if not preferred_sectors:
            return 0.5
        
        if project_sector in preferred_sectors:
            # Position in preference list matters
            try:
                position = preferred_sectors.index(project_sector)
                return 1.0 - (position * 0.05)  # Slight decrease for lower priority
            except ValueError:
                return 0.8
        
        # Check for related sectors (TRADE SECRET mapping)
        related = {
            "Healthcare": ["Education", "Commercial"],
            "Commercial": ["Retail", "Office"],
            "Industrial": ["Data Center", "Warehouse"],
            "Residential": ["Multi-Family", "Single-Family"]
        }
        
        for preferred in preferred_sectors:
            if project_sector in related.get(preferred, []):
                return 0.6
        
        return 0.3
    
    def _calculate_complexity_fit(
        self,
        project: Dict,
        user_profile: Dict
    ) -> float:
        """
        Proprietary complexity matching.
        
        TRADE SECRET: Complexity assessment algorithm
        """
        company_size = user_profile.get("company_size", "11-50")
        sector = project.get("sector", "Commercial")
        value = project.get("value", 1000000)
        
        # Company capability estimation
        size_capability = {
            "1-10": 0.3,
            "11-50": 0.5,
            "51-200": 0.75,
            "200+": 1.0
        }.get(company_size, 0.5)
        
        # Project complexity estimation
        sector_profile = self._SECTOR_PROFILES.get(sector, {"complexity": 0.5})
        base_complexity = sector_profile["complexity"]
        
        # Value adds complexity
        if value > 20000000:
            base_complexity = min(base_complexity + 0.2, 1.0)
        elif value > 10000000:
            base_complexity = min(base_complexity + 0.1, 1.0)
        
        # Calculate fit (TRADE SECRET formula)
        if size_capability >= base_complexity:
            return 0.9
        else:
            gap = base_complexity - size_capability
            return max(0.3, 0.9 - (gap * 1.5))
    
    def _generate_match_reasons(
        self,
        factors: Dict[str, float],
        project: Dict
    ) -> List[str]:
        """Generate human-readable match reasons."""
        reasons = []
        
        if factors.get("geographic_fit", 0) > 0.8:
            reasons.append(f"Located in your service area ({project.get('state', '')})")
        
        if factors.get("sector_fit", 0) > 0.8:
            reasons.append(f"Matches preferred sector: {project.get('sector', '')}")
        
        if factors.get("value_fit", 0) > 0.8:
            reasons.append("Within your target value range")
        
        if factors.get("trade_similarity", 0) > 0.6:
            reasons.append("Aligns with your trade specialty")
        
        if factors.get("complexity_fit", 0) > 0.8:
            reasons.append("Appropriate complexity for your team")
        
        return reasons if reasons else ["General market opportunity"]
    
    def _generate_concerns(
        self,
        factors: Dict[str, float],
        project: Dict
    ) -> List[str]:
        """Generate potential concerns."""
        concerns = []
        
        if factors.get("geographic_fit", 1) < 0.5:
            concerns.append("Outside primary service area")
        
        if factors.get("value_fit", 1) < 0.5:
            concerns.append("Value outside typical range")
        
        if factors.get("complexity_fit", 1) < 0.5:
            concerns.append("May require additional resources")
        
        sector_profile = self._SECTOR_PROFILES.get(project.get("sector", ""), {})
        if sector_profile.get("regulation", 0) > 0.8:
            concerns.append("High regulatory requirements")
        
        return concerns
    
    def _generate_watermark(self, match_data: Dict) -> str:
        """Generate proprietary watermark."""
        data_str = f"{self._model_id}-{datetime.utcnow().isoformat()}-{match_data.get('score', 0)}"
        return f"PDH-{hashlib.sha256(data_str.encode()).hexdigest()[:12]}"
    
    def match_project(
        self,
        project: Dict[str, Any],
        user_profile: Dict[str, Any]
    ) -> ProjectMatch:
        """
        Generate project match score and analysis.
        
        Args:
            project: Project details
            user_profile: User's business profile
            
        Returns:
            ProjectMatch with fit score and recommendations
        """
        # Calculate individual factors
        project_text = f"{project.get('name', '')} {project.get('description', '')}"
        
        factors = {
            "trade_similarity": self._calculate_text_similarity(
                project_text,
                user_profile.get("trade_specialty", "")
            ),
            "value_fit": self._calculate_value_fit(
                project.get("value", 0),
                user_profile.get("min_project_value", 0),
                user_profile.get("max_project_value", float("inf"))
            ),
            "geographic_fit": self._calculate_geographic_fit(
                project.get("state", ""),
                user_profile.get("service_states", []),
                project.get("city"),
                user_profile.get("service_cities")
            ),
            "sector_fit": self._calculate_sector_fit(
                project.get("sector", ""),
                user_profile.get("preferred_sectors", [])
            ),
            "complexity_fit": self._calculate_complexity_fit(project, user_profile)
        }
        
        # Apply proprietary weighting (TRADE SECRET)
        weights = {
            "trade_similarity": 0.20,
            "value_fit": 0.20,
            "geographic_fit": 0.25,
            "sector_fit": 0.20,
            "complexity_fit": 0.15
        }
        
        # Calculate weighted fit score
        fit_score = sum(factors[f] * weights[f] for f in factors)
        
        # Apply feedback learning adjustment
        sector_key = f"sector_{project.get('sector', '')}"
        if sector_key in self._feedback_weights:
            fit_score *= (0.8 + 0.4 * self._feedback_weights[sector_key])
        
        # Normalize to 0-100
        fit_score = min(fit_score * 100, 100)
        
        # Generate recommendation
        if fit_score >= 80:
            recommendation = "HIGHLY RECOMMENDED"
        elif fit_score >= 60:
            recommendation = "RECOMMENDED"
        elif fit_score >= 40:
            recommendation = "CONSIDER"
        else:
            recommendation = "LOW FIT"
        
        match_data = {"score": fit_score}
        
        return ProjectMatch(
            project=project,
            fit_score=round(fit_score, 2),
            match_factors={k: round(v, 4) for k, v in factors.items()},
            match_reasons=self._generate_match_reasons(factors, project),
            concerns=self._generate_concerns(factors, project),
            recommendation=recommendation,
            model_version=f"{self.VERSION} {self.COPYRIGHT}",
            watermark=self._generate_watermark(match_data)
        )
    
    def match_projects(
        self,
        projects: List[Dict],
        user_profile: Dict,
        min_score: float = 0
    ) -> List[ProjectMatch]:
        """Match and rank multiple projects."""
        matches = [
            self.match_project(project, user_profile)
            for project in projects
        ]
        
        # Filter by minimum score and sort by fit
        filtered = [m for m in matches if m.fit_score >= min_score]
        return sorted(filtered, key=lambda x: x.fit_score, reverse=True)
    
    def record_feedback(self, project: Dict, decision: str):
        """Record user feedback for adaptive learning."""
        self.user_feedback.append({
            "project": project,
            "decision": decision,
            "timestamp": datetime.utcnow().isoformat()
        })
        self._feedback_weights = self._learn_from_feedback()
    
    def get_model_info(self) -> Dict[str, str]:
        """Return model metadata."""
        return {
            "name": "Project-Contractor Matching AI",
            "version": self.VERSION,
            "copyright": self.COPYRIGHT,
            "patent_status": self.PATENT_STATUS,
            "model_id": self._model_id,
            "license": "PROPRIETARY - All Rights Reserved",
            "feedback_samples": len(self.user_feedback)
        }
