"""
Win probability model for predicting project win rates.

Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.
PROPRIETARY AND CONFIDENTIAL - Unauthorized use prohibited.

This module contains proprietary ML algorithms and predictive models.
"""
from typing import Dict, Any, List
import numpy as np
from sklearn.ensemble import RandomForestClassifier


class WinProbabilityModel:
    """Model for predicting win probability on projects."""
    
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_trained = False
    
    def train(self, features: List[Dict[str, Any]], labels: List[bool]) -> None:
        """Train the model on historical data."""
        X = self._prepare_features(features)
        y = np.array(labels)
        
        self.model.fit(X, y)
        self.is_trained = True
    
    def predict(self, features: Dict[str, Any]) -> float:
        """Predict win probability for a single project."""
        if not self.is_trained:
            # Return default probability if not trained
            return 0.5
        
        X = self._prepare_features([features])
        probability = self.model.predict_proba(X)[0][1]
        return float(probability)
    
    def _prepare_features(self, features_list: List[Dict[str, Any]]) -> np.ndarray:
        """Prepare features for the model."""
        # Extract relevant features
        feature_matrix = []
        
        for features in features_list:
            feature_vector = [
                features.get("project_value", 0) / 1_000_000,  # Normalize to millions
                features.get("historical_win_rate", 0.5),
                features.get("past_projects", 0) / 10,  # Normalize
                features.get("sector_experience", 0),
                features.get("competition_level", 0.5),
            ]
            feature_matrix.append(feature_vector)
        
        return np.array(feature_matrix)
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance scores."""
        if not self.is_trained:
            return {}
        
        feature_names = [
            "project_value",
            "historical_win_rate",
            "past_projects",
            "sector_experience",
            "competition_level",
        ]
        
        importance_dict = {
            name: float(importance)
            for name, importance in zip(feature_names, self.model.feature_importances_)
        }
        
        return importance_dict
