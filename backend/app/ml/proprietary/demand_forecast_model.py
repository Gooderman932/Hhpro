"""
Proprietary Construction Demand Forecasting Engine
Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.

CONFIDENTIAL AND PROPRIETARY INFORMATION
Patent Pending - U.S. Patent Application No. [Provisional]

This algorithm and methodology constitute trade secrets of Poor Dude Holdings LLC.
Unauthorized use, reproduction, or distribution is strictly prohibited.

INNOVATION CLAIMS:
- Proprietary "Market Momentum Score" calculation
- Novel seasonality adjustment for regional construction patterns
- Custom economic indicator integration methodology
- Multi-factor time-series prediction for construction demand

For licensing inquiries: legal@poorduceholdings.com
"""

import math
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class DemandForecast:
    """Structured demand forecast result."""
    period: str
    predicted_demand: float
    confidence_interval: Tuple[float, float]
    momentum_score: float
    trend: str
    factors: Dict[str, float]
    model_version: str
    watermark: str


@dataclass
class MarketMomentum:
    """Proprietary Market Momentum Score."""
    score: float
    direction: str
    strength: str
    contributing_factors: List[str]


class DemandForecastModel:
    """
    Proprietary Construction Demand Forecasting Engine
    
    © 2025 Poor Dude Holdings LLC - Patent Pending
    
    A custom-built time-series prediction system specifically designed
    for construction industry demand forecasting.
    
    Key Features:
    - Proprietary Market Momentum Score calculation
    - Construction-specific seasonality adjustments
    - Economic indicator integration
    - Regional market factor analysis
    - Multi-horizon forecasting (1-12 months)
    """
    
    VERSION = "1.0.0"
    COPYRIGHT = "© 2025 Poor Dude Holdings LLC"
    PATENT_STATUS = "Patent Pending"
    
    # Proprietary seasonality factors by month (TRADE SECRET)
    _SEASONALITY = {
        1: 0.75,   # January - Winter slowdown
        2: 0.78,   # February
        3: 0.92,   # March - Spring pickup
        4: 1.05,   # April - Peak season starts
        5: 1.15,   # May - Strong activity
        6: 1.12,   # June
        7: 1.08,   # July - Summer
        8: 1.05,   # August
        9: 1.10,   # September - Fall peak
        10: 1.08,  # October
        11: 0.92,  # November - Slowdown begins
        12: 0.80   # December - Holiday slowdown
    }
    
    # Regional growth factors (TRADE SECRET)
    _REGIONAL_FACTORS = {
        # Southeast - High Growth
        "TX": 1.25, "FL": 1.22, "NC": 1.18, "TN": 1.15, "GA": 1.12, "SC": 1.10,
        "AL": 1.05, "MS": 1.02, "LA": 1.00, "AR": 0.98, "KY": 0.97, "VA": 1.08,
        "WV": 0.90,
        # Southwest/Mountain
        "AZ": 1.20, "NV": 1.08, "CO": 1.10, "UT": 1.15, "NM": 1.02, "ID": 1.18,
        "MT": 1.05, "WY": 0.95, "OK": 1.00,
        # Pacific
        "CA": 1.02, "WA": 1.05, "OR": 1.03, "HI": 0.98, "AK": 0.92,
        # Midwest
        "OH": 0.98, "IL": 0.90, "MI": 0.95, "IN": 1.00, "WI": 0.97, "MN": 1.02,
        "IA": 0.96, "MO": 0.98, "KS": 0.95, "NE": 0.97, "SD": 1.00, "ND": 1.05,
        # Northeast
        "PA": 0.95, "NY": 0.92, "NJ": 0.95, "CT": 0.93, "MA": 0.98, "MD": 1.00,
        "DE": 0.97, "RI": 0.92, "VT": 0.90, "NH": 0.95, "ME": 0.93, "DC": 1.05,
        # Territories
        "PR": 0.88, "GU": 0.85, "VI": 0.82, "AS": 0.80, "MP": 0.80
    }
    
    # Sector growth multipliers (TRADE SECRET)
    _SECTOR_MULTIPLIERS = {
        "Healthcare": 1.35,
        "Industrial": 1.28,
        "Data Center": 1.40,
        "Education": 1.15,
        "Commercial": 1.10,
        "Residential": 1.05,
        "Retail": 0.95,
        "Hospitality": 0.90
    }
    
    def __init__(self, historical_data: Optional[List[Dict]] = None):
        """
        Initialize the Demand Forecast Model.
        
        Args:
            historical_data: Historical permit/project data for calibration
        """
        self.historical_data = historical_data or []
        self._model_id = self._generate_model_id()
        self._base_demand = self._calculate_base_demand()
    
    def _generate_model_id(self) -> str:
        """Generate unique model instance identifier."""
        timestamp = datetime.utcnow().isoformat()
        return hashlib.sha256(f"PDH-DFM-{timestamp}".encode()).hexdigest()[:16]
    
    def _calculate_base_demand(self) -> float:
        """Calculate base demand from historical data."""
        if not self.historical_data:
            return 100.0  # Normalized base
        
        values = [d.get("value", 0) for d in self.historical_data]
        return sum(values) / len(values) if values else 100.0
    
    def _apply_seasonality(self, base_value: float, target_month: int) -> float:
        """
        Apply proprietary seasonality adjustment.
        
        TRADE SECRET: Seasonality calculation methodology
        """
        seasonal_factor = self._SEASONALITY.get(target_month, 1.0)
        return base_value * seasonal_factor
    
    def _apply_regional_factor(self, value: float, region: str) -> float:
        """
        Apply proprietary regional growth factor.
        
        TRADE SECRET: Regional adjustment methodology
        """
        regional_factor = self._REGIONAL_FACTORS.get(region, 1.0)
        return value * regional_factor
    
    def _apply_sector_factor(self, value: float, sector: str) -> float:
        """
        Apply proprietary sector growth multiplier.
        
        TRADE SECRET: Sector adjustment methodology
        """
        sector_factor = self._SECTOR_MULTIPLIERS.get(sector, 1.0)
        return value * sector_factor
    
    def _calculate_economic_impact(self, economic_data: Optional[Dict]) -> float:
        """
        Proprietary economic indicator integration.
        
        TRADE SECRET: Economic factor weighting
        """
        if not economic_data:
            return 1.0
        
        impact = 1.0
        
        # Construction spending trend
        construction_trend = economic_data.get("construction_spending_change", 0)
        impact *= (1 + construction_trend * 0.3)
        
        # Housing starts impact
        housing_trend = economic_data.get("housing_starts_change", 0)
        impact *= (1 + housing_trend * 0.2)
        
        # Employment factor
        employment_trend = economic_data.get("construction_employment_change", 0)
        impact *= (1 + employment_trend * 0.15)
        
        # Interest rate inverse impact
        rate_change = economic_data.get("interest_rate_change", 0)
        impact *= (1 - rate_change * 0.1)
        
        return max(0.5, min(impact, 1.5))
    
    def calculate_market_momentum(
        self,
        region: str,
        sector: str,
        economic_data: Optional[Dict] = None
    ) -> MarketMomentum:
        """
        Proprietary Market Momentum Score Calculation
        
        TRADE SECRET: Momentum scoring algorithm
        
        This is our unique methodology for measuring market momentum
        in construction demand.
        """
        factors = []
        score = 50.0  # Neutral baseline
        
        # Regional momentum (TRADE SECRET formula)
        regional_factor = self._REGIONAL_FACTORS.get(region, 1.0)
        regional_score = (regional_factor - 1) * 100
        score += regional_score
        if regional_factor > 1.1:
            factors.append(f"Strong regional growth ({region})")
        
        # Sector momentum (TRADE SECRET formula)
        sector_factor = self._SECTOR_MULTIPLIERS.get(sector, 1.0)
        sector_score = (sector_factor - 1) * 80
        score += sector_score
        if sector_factor > 1.1:
            factors.append(f"High-growth sector ({sector})")
        
        # Seasonal momentum
        current_month = datetime.now().month
        seasonal_factor = self._SEASONALITY.get(current_month, 1.0)
        seasonal_score = (seasonal_factor - 1) * 50
        score += seasonal_score
        if seasonal_factor > 1.05:
            factors.append("Favorable seasonal timing")
        
        # Economic momentum
        if economic_data:
            econ_impact = self._calculate_economic_impact(economic_data)
            econ_score = (econ_impact - 1) * 60
            score += econ_score
            if econ_impact > 1.05:
                factors.append("Positive economic indicators")
        
        # Normalize to 0-100
        score = max(0, min(score, 100))
        
        # Determine direction and strength
        if score >= 65:
            direction = "UP"
            strength = "STRONG" if score >= 80 else "MODERATE"
        elif score <= 35:
            direction = "DOWN"
            strength = "STRONG" if score <= 20 else "MODERATE"
        else:
            direction = "STABLE"
            strength = "NEUTRAL"
        
        return MarketMomentum(
            score=round(score, 2),
            direction=direction,
            strength=strength,
            contributing_factors=factors
        )
    
    def _calculate_confidence_interval(
        self,
        predicted_value: float,
        months_ahead: int
    ) -> Tuple[float, float]:
        """
        Calculate prediction confidence interval.
        
        TRADE SECRET: Confidence interval methodology
        """
        # Uncertainty grows with forecast horizon (proprietary formula)
        base_uncertainty = 0.08
        horizon_factor = 1 + (months_ahead * 0.03)
        uncertainty = base_uncertainty * horizon_factor
        
        lower = predicted_value * (1 - uncertainty)
        upper = predicted_value * (1 + uncertainty)
        
        return (round(lower, 2), round(upper, 2))
    
    def _generate_watermark(self, forecast_data: Dict) -> str:
        """Generate proprietary watermark for output verification."""
        data_str = f"{self._model_id}-{datetime.utcnow().isoformat()}-{forecast_data.get('period', '')}"
        return f"PDH-{hashlib.sha256(data_str.encode()).hexdigest()[:12]}"
    
    def forecast(
        self,
        region: str,
        sector: str,
        months_ahead: int = 6,
        economic_data: Optional[Dict] = None,
        base_value: Optional[float] = None
    ) -> List[DemandForecast]:
        """
        Generate demand forecasts for specified horizon.
        
        Proprietary algorithm combining seasonality, regional factors,
        sector growth, and economic indicators.
        
        Args:
            region: Target region (state code)
            sector: Target sector
            months_ahead: Forecast horizon (1-12 months)
            economic_data: Optional economic indicators
            base_value: Optional custom base value
            
        Returns:
            List of DemandForecast for each month
        """
        forecasts = []
        base = base_value or self._base_demand
        current_date = datetime.now()
        
        # Calculate market momentum
        momentum = self.calculate_market_momentum(region, sector, economic_data)
        
        for i in range(1, months_ahead + 1):
            target_date = current_date + timedelta(days=30 * i)
            target_month = target_date.month
            
            # Apply proprietary adjustments
            value = base
            value = self._apply_seasonality(value, target_month)
            value = self._apply_regional_factor(value, region)
            value = self._apply_sector_factor(value, sector)
            value *= self._calculate_economic_impact(economic_data)
            
            # Apply growth trend (compounding monthly)
            growth_rate = 0.02 * (momentum.score / 50)  # Proprietary formula
            value *= (1 + growth_rate) ** i
            
            # Calculate confidence interval
            ci = self._calculate_confidence_interval(value, i)
            
            # Determine trend
            if i == 1:
                trend = momentum.direction
            else:
                prev_value = forecasts[-1].predicted_demand
                if value > prev_value * 1.02:
                    trend = "INCREASING"
                elif value < prev_value * 0.98:
                    trend = "DECREASING"
                else:
                    trend = "STABLE"
            
            # Build factor breakdown
            factors = {
                "seasonality": self._SEASONALITY.get(target_month, 1.0),
                "regional": self._REGIONAL_FACTORS.get(region, 1.0),
                "sector": self._SECTOR_MULTIPLIERS.get(sector, 1.0),
                "economic": self._calculate_economic_impact(economic_data),
                "momentum": momentum.score / 100
            }
            
            forecast_data = {"period": target_date.strftime("%Y-%m")}
            
            forecasts.append(DemandForecast(
                period=target_date.strftime("%Y-%m"),
                predicted_demand=round(value, 2),
                confidence_interval=ci,
                momentum_score=momentum.score,
                trend=trend,
                factors={k: round(v, 4) for k, v in factors.items()},
                model_version=f"{self.VERSION} {self.COPYRIGHT}",
                watermark=self._generate_watermark(forecast_data)
            ))
        
        return forecasts
    
    def get_regional_outlook(
        self,
        regions: List[str],
        sector: str,
        economic_data: Optional[Dict] = None
    ) -> Dict[str, Dict]:
        """Generate comparative regional outlook."""
        outlook = {}
        
        for region in regions:
            momentum = self.calculate_market_momentum(region, sector, economic_data)
            forecast = self.forecast(region, sector, months_ahead=3, economic_data=economic_data)
            
            outlook[region] = {
                "momentum_score": momentum.score,
                "direction": momentum.direction,
                "strength": momentum.strength,
                "3_month_forecast": forecast[-1].predicted_demand if forecast else None,
                "growth_rate": round((forecast[-1].predicted_demand / forecast[0].predicted_demand - 1) * 100, 2) if len(forecast) > 1 else 0
            }
        
        return outlook
    
    def get_model_info(self) -> Dict[str, str]:
        """Return model metadata."""
        return {
            "name": "Construction Demand Forecasting Engine",
            "version": self.VERSION,
            "copyright": self.COPYRIGHT,
            "patent_status": self.PATENT_STATUS,
            "model_id": self._model_id,
            "license": "PROPRIETARY - All Rights Reserved"
        }
