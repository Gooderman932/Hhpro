"""Demand forecasting model for predicting construction market trends."""
from typing import Dict, Any, List
import numpy as np
from datetime import datetime, timedelta


class DemandForecastModel:
    """Model for forecasting construction demand."""
    
    def __init__(self):
        self.historical_data = []
    
    def add_historical_data(self, date: datetime, value: float, metadata: Dict[str, Any] = None) -> None:
        """Add historical data point."""
        self.historical_data.append({
            "date": date,
            "value": value,
            "metadata": metadata or {}
        })
    
    def forecast(self, months_ahead: int = 6) -> List[Dict[str, Any]]:
        """Forecast demand for the specified number of months."""
        if not self.historical_data:
            # Return default forecast if no historical data
            return self._default_forecast(months_ahead)
        
        # Sort historical data by date
        sorted_data = sorted(self.historical_data, key=lambda x: x["date"])
        values = [d["value"] for d in sorted_data]
        
        # Simple moving average for trend
        if len(values) >= 3:
            trend = (values[-1] - values[0]) / len(values)
        else:
            trend = 0
        
        # Generate forecast
        forecast = []
        last_value = values[-1] if values else 100
        
        for i in range(1, months_ahead + 1):
            predicted_value = last_value + (trend * i)
            # Add some noise/seasonality (simplified)
            seasonal_factor = 1 + 0.1 * np.sin(i * np.pi / 6)
            predicted_value *= seasonal_factor
            
            forecast.append({
                "month": i,
                "predicted_value": max(0, predicted_value),
                "confidence_lower": max(0, predicted_value * 0.8),
                "confidence_upper": predicted_value * 1.2,
            })
        
        return forecast
    
    def _default_forecast(self, months_ahead: int) -> List[Dict[str, Any]]:
        """Generate default forecast when no historical data is available."""
        base_value = 100
        return [
            {
                "month": i,
                "predicted_value": base_value,
                "confidence_lower": base_value * 0.8,
                "confidence_upper": base_value * 1.2,
            }
            for i in range(1, months_ahead + 1)
        ]
    
    def analyze_seasonality(self) -> Dict[str, Any]:
        """Analyze seasonal patterns in the data."""
        if len(self.historical_data) < 12:
            return {"message": "Insufficient data for seasonality analysis"}
        
        # Group by month
        monthly_values = {}
        for data_point in self.historical_data:
            month = data_point["date"].month
            if month not in monthly_values:
                monthly_values[month] = []
            monthly_values[month].append(data_point["value"])
        
        # Calculate average by month
        seasonality = {
            month: np.mean(values)
            for month, values in monthly_values.items()
        }
        
        return {
            "seasonality_by_month": seasonality,
            "peak_month": max(seasonality, key=seasonality.get),
            "trough_month": min(seasonality, key=seasonality.get),
        }
