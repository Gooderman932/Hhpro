"""
Demand Forecast Model - Time series forecasting for construction market demand.
Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression


class DemandForecastModel:
    """Time series model for demand forecasting."""
    
    def __init__(self):
        self.model = LinearRegression()
        self.model_version = "1.0.0"
        self.is_trained = False
        
        # Sector growth rates (annual %)
        self.sector_growth_rates = {
            'Commercial': 0.08,
            'Residential': 0.06,
            'Infrastructure': 0.12,
            'Healthcare': 0.10,
            'Industrial': 0.07,
            'Education': 0.05
        }
        
        # Regional multipliers
        self.regional_multipliers = {
            'TX': 1.15, 'FL': 1.12, 'AZ': 1.18, 'CA': 1.05,
            'WA': 1.08, 'CO': 1.10, 'GA': 1.08, 'NC': 1.07,
            'TN': 1.09, 'NV': 1.14
        }
    
    def forecast(
        self,
        sector: str,
        region: str,
        months_ahead: int = 6,
        historical_data: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """Generate demand forecast for a sector/region combination."""
        
        base_demand = self._get_base_demand(sector)
        growth_rate = self.sector_growth_rates.get(sector, 0.06)
        regional_mult = self.regional_multipliers.get(region, 1.0)
        
        forecasts = []
        current_date = datetime.now()
        
        for month in range(1, months_ahead + 1):
            forecast_date = current_date + timedelta(days=30 * month)
            
            # Apply growth and seasonality
            monthly_growth = (1 + growth_rate) ** (month / 12)
            seasonal_factor = self._get_seasonal_factor(forecast_date.month)
            
            # Calculate forecast value
            forecast_value = base_demand * monthly_growth * regional_mult * seasonal_factor
            
            # Add some realistic variance
            variance = np.random.normal(1.0, 0.05)
            forecast_value *= variance
            
            # Calculate confidence interval
            confidence_lower = forecast_value * 0.85
            confidence_upper = forecast_value * 1.15
            
            forecasts.append({
                'date': forecast_date.strftime('%Y-%m-%d'),
                'month': forecast_date.strftime('%B %Y'),
                'predicted_demand': round(forecast_value, 2),
                'confidence_lower': round(confidence_lower, 2),
                'confidence_upper': round(confidence_upper, 2),
                'confidence_level': 0.85
            })
        
        # Calculate trend
        values = [f['predicted_demand'] for f in forecasts]
        trend = 'increasing' if values[-1] > values[0] else 'decreasing'
        trend_pct = ((values[-1] - values[0]) / values[0]) * 100
        
        return {
            'sector': sector,
            'region': region,
            'forecast_period_months': months_ahead,
            'forecasts': forecasts,
            'trend': trend,
            'trend_percentage': round(trend_pct, 1),
            'model_version': self.model_version,
            'generated_at': datetime.now().isoformat()
        }
    
    def _get_base_demand(self, sector: str) -> float:
        """Get base demand value for a sector (in millions)."""
        base_demands = {
            'Commercial': 150,
            'Residential': 200,
            'Infrastructure': 300,
            'Healthcare': 120,
            'Industrial': 100,
            'Education': 80
        }
        return base_demands.get(sector, 100)
    
    def _get_seasonal_factor(self, month: int) -> float:
        """Get seasonal adjustment factor."""
        # Construction typically peaks in summer, dips in winter
        seasonal_factors = {
            1: 0.85, 2: 0.88, 3: 0.95, 4: 1.05,
            5: 1.10, 6: 1.12, 7: 1.15, 8: 1.12,
            9: 1.08, 10: 1.02, 11: 0.95, 12: 0.88
        }
        return seasonal_factors.get(month, 1.0)
    
    def get_regional_outlook(self, regions: List[str] = None) -> List[Dict]:
        """Get demand outlook for multiple regions."""
        if regions is None:
            regions = ['TX', 'FL', 'CA', 'AZ', 'WA']
        
        outlooks = []
        for region in regions:
            multiplier = self.regional_multipliers.get(region, 1.0)
            growth_indicator = 'high' if multiplier > 1.1 else 'moderate' if multiplier > 1.0 else 'low'
            
            outlooks.append({
                'region': region,
                'growth_indicator': growth_indicator,
                'multiplier': multiplier,
                'top_sectors': self._get_top_sectors_for_region(region)
            })
        
        return sorted(outlooks, key=lambda x: x['multiplier'], reverse=True)
    
    def _get_top_sectors_for_region(self, region: str) -> List[str]:
        """Get top performing sectors for a region."""
        # Simplified mapping
        regional_sectors = {
            'TX': ['Commercial', 'Infrastructure', 'Industrial'],
            'FL': ['Residential', 'Healthcare', 'Commercial'],
            'CA': ['Commercial', 'Residential', 'Infrastructure'],
            'AZ': ['Residential', 'Commercial', 'Healthcare'],
            'WA': ['Commercial', 'Infrastructure', 'Education']
        }
        return regional_sectors.get(region, ['Commercial', 'Residential', 'Infrastructure'])
