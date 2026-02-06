"""
Construction Intelligence ML Models - Package Initialization
Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.

CONFIDENTIAL AND PROPRIETARY INFORMATION
Patent Pending - U.S. Patent Application

This module and all contained algorithms constitute trade secrets
of Poor Dude Holdings LLC. Unauthorized use, reproduction, or 
distribution is strictly prohibited.

For licensing inquiries: legal@poorduceholdings.com
"""

__version__ = "1.0.0"
__author__ = "Poor Dude Holdings LLC"
__copyright__ = "Copyright (c) 2025 Poor Dude Holdings LLC"
__license__ = "PROPRIETARY - All Rights Reserved"

from .win_probability_model import WinProbabilityModel
from .demand_forecast_model import DemandForecastModel
from .competitive_intelligence import CompetitiveIntelligenceScorer
from .project_matcher import ProjectMatcherAI

__all__ = [
    "WinProbabilityModel",
    "DemandForecastModel", 
    "CompetitiveIntelligenceScorer",
    "ProjectMatcherAI"
]
