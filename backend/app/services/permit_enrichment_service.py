"""
Permit Enrichment Service - Proprietary AI Analysis Layer
Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.
CONFIDENTIAL - Patent Pending

Connects raw permit data to proprietary ML models for scoring and recommendations.
"""
import hashlib
import re
from typing import Dict, Any, List

from app.ml.proprietary.project_matcher import ProjectMatcherAI
from app.ml.proprietary.win_probability_model import WinProbabilityModel


# Trade keyword detection (derived from ProjectMatcherAI's domain knowledge)
_TRADE_PATTERNS = {
    "electrical": r"electri|wiring|power|panel|lighting|generator|circuit",
    "plumbing": r"plumb|pipe|water|drain|sewer|fixture|sprinkler",
    "hvac": r"hvac|heating|cooling|ventilat|air.?condition|duct|boiler",
    "drywall": r"drywall|sheetrock|gypsum|partition|taping",
    "roofing": r"roof|shingle|membrane|flashing|gutter|waterproof",
    "concrete": r"concrete|foundation|slab|masonry|cement|rebar",
    "structural": r"steel|structural|framing|beam|column|truss|welding",
    "flooring": r"floor|tile|carpet|hardwood|vinyl|epoxy",
    "painting": r"paint|coating|primer|stain|finish|texture",
    "general": r"construct|build|renovat|remodel|addition|tenant.?improve|demolit",
}

# Cost-to-timeline heuristic (TRADE SECRET)
_TIMELINE_BRACKETS = [
    (50_000, 2), (200_000, 4), (500_000, 6), (1_000_000, 9),
    (5_000_000, 14), (10_000_000, 18), (50_000_000, 24),
]

# Opportunity score weights (TRADE SECRET)
_OPP_WEIGHTS = {
    "match_score": 0.35,
    "win_probability": 0.25,
    "cost_score": 0.20,
    "recency_score": 0.20,
}


class PermitEnrichmentService:
    """Enriches raw permits with proprietary ML scores and recommendations."""

    def __init__(self):
        self.matcher = ProjectMatcherAI()
        self.win_model = WinProbabilityModel()

    def enrich_permit(self, permit: Dict[str, Any], user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Add proprietary analysis to a single permit."""
        desc = f"{permit.get('work_type', '')} {permit.get('description', '')}".lower()
        cost = permit.get("estimated_cost") or 0

        # 1. Detect required trades
        trades = [t for t, pat in _TRADE_PATTERNS.items() if re.search(pat, desc)]
        if not trades:
            trades = ["general"]

        # 2. Match score via ProjectMatcherAI
        project_for_match = {
            "name": permit.get("description") or permit.get("work_type") or "Permit Project",
            "description": desc,
            "value": cost,
            "sector": _infer_sector(desc),
            "state": permit.get("state", ""),
            "city": permit.get("city", ""),
        }
        matches = self.matcher.match_projects([project_for_match], user_profile, min_score=0)
        match_score = matches[0].fit_score / 100 if matches else 0.3

        # 3. Win probability via WinProbabilityModel
        pred = self.win_model.predict(project=project_for_match, user_profile=user_profile)
        win_prob = pred.probability

        # 4. Estimate timeline
        timeline = 3
        for threshold, months in _TIMELINE_BRACKETS:
            if cost <= threshold:
                timeline = months
                break
        else:
            timeline = 30

        # 5. Cost attractiveness score (normalized 0-1)
        min_val = user_profile.get("min_project_value", 50_000)
        max_val = user_profile.get("max_project_value", 10_000_000)
        if cost <= 0:
            cost_score = 0.3
        elif min_val <= cost <= max_val:
            cost_score = 0.8 + 0.2 * min(cost / max_val, 1)
        elif cost < min_val:
            cost_score = max(0.1, cost / min_val)
        else:
            cost_score = max(0.1, max_val / cost)

        # 6. Recency score
        recency_score = 0.7  # Default; real impl would parse filing_date vs now

        # 7. Opportunity score (proprietary weighted formula)
        opp_score = round(
            _OPP_WEIGHTS["match_score"] * match_score +
            _OPP_WEIGHTS["win_probability"] * win_prob +
            _OPP_WEIGHTS["cost_score"] * cost_score +
            _OPP_WEIGHTS["recency_score"] * recency_score,
            4
        ) * 100  # Scale to 0-100

        opp_score = min(round(opp_score, 1), 99.9)

        # 8. Recommendation
        rec = _recommendation(opp_score, match_score, win_prob)

        # 9. Watermark
        wm = "PDH-" + hashlib.md5(f"{permit.get('permit_id','')}{cost}".encode()).hexdigest()[:10]

        permit["proprietary_analysis"] = {
            "match_score": round(match_score * 100, 1),
            "win_probability": round(win_prob * 100, 1),
            "required_trades": trades,
            "estimated_timeline_months": timeline,
            "opportunity_score": opp_score,
            "cost_attractiveness": round(cost_score * 100, 1),
            "recommendation": rec,
            "watermark": wm,
            "legal_notice": "Patent Pending. Proprietary AI Analysis of Poor Dude Holdings LLC.",
        }
        # Remove raw provider data from response
        permit.pop("raw", None)
        return permit


def _infer_sector(desc: str) -> str:
    sectors = {
        "Healthcare": r"hospital|medical|clinic|health|dental|pharma",
        "Education": r"school|university|college|campus|classroom|education",
        "Retail": r"retail|store|shop|mall|restaurant|food",
        "Industrial": r"warehouse|factory|industrial|manufacturing|plant",
        "Residential": r"residential|apartment|condo|house|dwelling|family",
        "Data Center": r"data center|server|telecom",
    }
    for sector, pat in sectors.items():
        if re.search(pat, desc):
            return sector
    return "Commercial"


def _recommendation(opp: float, match: float, win: float) -> str:
    if opp >= 75 and match >= 0.7:
        return "Excellent opportunity - contact owner ASAP"
    if opp >= 60:
        return "Strong fit - prepare bid within 48 hours"
    if opp >= 45:
        return "Good prospect - worth evaluating"
    if opp >= 30:
        return "Moderate fit - review if capacity allows"
    return "Low priority - monitor for changes"
