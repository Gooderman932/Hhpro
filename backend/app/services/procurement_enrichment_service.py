"""
Procurement Enrichment Service - Proprietary AI for Federal Opportunities
Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.
CONFIDENTIAL - Patent Pending
"""
import hashlib
import re
from typing import Dict, Any, List

from app.ml.proprietary.project_matcher import ProjectMatcherAI
from app.ml.proprietary.win_probability_model import WinProbabilityModel

# NAICS → trade mapping (TRADE SECRET)
_NAICS_TRADES = {
    "2362": ["general", "concrete", "structural"],
    "2371": ["plumbing", "concrete"],
    "2373": ["concrete", "structural"],
    "2381": ["concrete", "structural"],
    "2382": ["electrical", "plumbing", "hvac"],
    "2383": ["drywall", "painting", "flooring"],
    "2389": ["general"],
}

# Federal opportunity timeline heuristics
_FED_TIMELINE = [
    (100_000, 3), (500_000, 6), (2_000_000, 10), (10_000_000, 18),
    (50_000_000, 24), (200_000_000, 36),
]

_OPP_WEIGHTS = {
    "match_score": 0.30,
    "win_probability": 0.25,
    "value_score": 0.25,
    "urgency_score": 0.20,
}


class ProcurementEnrichmentService:
    """Proprietary enrichment for federal procurement opportunities."""

    def __init__(self):
        self.matcher = ProjectMatcherAI()
        self.win_model = WinProbabilityModel()

    def enrich_opportunity(self, opp: Dict[str, Any], user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Add proprietary AI analysis to a federal opportunity."""
        desc = f"{opp.get('title', '')} {opp.get('description', '')}".lower()
        naics = opp.get("naics", "")
        value = opp.get("estimated_value") or 0

        # 1. Detect trades from NAICS + description
        trades = set()
        for prefix, trade_list in _NAICS_TRADES.items():
            if naics.startswith(prefix):
                trades.update(trade_list)
        # Also scan description
        trade_keywords = {
            "electrical": r"electri|wiring|power|panel",
            "plumbing": r"plumb|pipe|water|drain|sewer",
            "hvac": r"hvac|heating|cooling|ventilat",
            "drywall": r"drywall|sheetrock|gypsum",
            "roofing": r"roof|shingle|membrane",
            "concrete": r"concrete|foundation|slab|masonry",
            "structural": r"steel|structural|framing",
            "painting": r"paint|coating|primer",
            "general": r"construct|build|renovat|repair|maintain",
        }
        for trade, pat in trade_keywords.items():
            if re.search(pat, desc):
                trades.add(trade)
        if not trades:
            trades = {"general"}

        # 2. Match score
        project_for_match = {
            "name": opp.get("title", "Federal Opportunity"),
            "description": desc,
            "value": value,
            "sector": "Government",
            "state": opp.get("place_of_performance_state", ""),
            "city": opp.get("place_of_performance_city", ""),
        }
        matches = self.matcher.match_projects([project_for_match], user_profile, min_score=0)
        match_score = matches[0].fit_score / 100 if matches else 0.25

        # 3. Win probability
        pred = self.win_model.predict(project=project_for_match, user_profile=user_profile)
        win_prob = pred.probability

        # 4. Timeline
        timeline = 6
        for threshold, months in _FED_TIMELINE:
            if value <= threshold:
                timeline = months
                break
        else:
            timeline = 36

        # 5. Value attractiveness
        min_val = user_profile.get("min_project_value", 50_000)
        max_val = user_profile.get("max_project_value", 10_000_000)
        if value <= 0:
            value_score = 0.3
        elif min_val <= value <= max_val:
            value_score = 0.85
        elif value < min_val:
            value_score = max(0.1, value / min_val)
        else:
            value_score = max(0.1, max_val / value)

        # 6. Urgency (deadline proximity)
        urgency_score = 0.6  # Default

        # 7. Opportunity score
        opp_score = round(
            _OPP_WEIGHTS["match_score"] * match_score +
            _OPP_WEIGHTS["win_probability"] * win_prob +
            _OPP_WEIGHTS["value_score"] * value_score +
            _OPP_WEIGHTS["urgency_score"] * urgency_score,
            4
        ) * 100
        opp_score = min(round(opp_score, 1), 99.9)

        # 8. Recommendation
        if opp_score >= 70 and match_score >= 0.65:
            rec = "High-value federal opportunity - prepare response immediately"
        elif opp_score >= 55:
            rec = "Strong federal prospect - review requirements and team"
        elif opp_score >= 40:
            rec = "Worth evaluating - check set-aside and capability requirements"
        elif opp_score >= 25:
            rec = "Moderate fit - consider teaming arrangement"
        else:
            rec = "Low priority - monitor for future related opportunities"

        wm = "PDH-FED-" + hashlib.md5(f"{opp.get('opportunity_id', '')}{value}".encode()).hexdigest()[:8]

        opp["proprietary_analysis"] = {
            "match_score": round(match_score * 100, 1),
            "win_probability": round(win_prob * 100, 1),
            "required_trades": sorted(trades),
            "estimated_timeline_months": timeline,
            "opportunity_score": opp_score,
            "value_attractiveness": round(value_score * 100, 1),
            "recommendation": rec,
            "watermark": wm,
            "legal_notice": "Patent Pending. Proprietary AI Analysis of Poor Dude Holdings LLC.",
        }
        opp.pop("raw", None)
        return opp
