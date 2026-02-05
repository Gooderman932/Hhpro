"""
Win Probability Model - Random Forest classifier for predicting project win likelihood.
Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.
"""
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from typing import Dict, Any, Optional
import pickle
import os


class WinProbabilityModel:
    """Random Forest model for win probability prediction."""
    
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.is_trained = False
        self.model_version = "1.0.0"
        self.feature_names = [
            'project_value', 'company_experience', 'past_win_rate',
            'competitor_count', 'relationship_strength', 'sector_fit',
            'geographic_proximity', 'timing_score'
        ]
    
    def _extract_features(self, project_data: Dict[str, Any], company_data: Dict[str, Any]) -> np.ndarray:
        """Extract features from project and company data."""
        features = [
            project_data.get('value', 0) / 1_000_000,  # Normalize to millions
            company_data.get('years_experience', 5) / 20,
            company_data.get('past_win_rate', 0.3),
            project_data.get('competitor_count', 5) / 10,
            company_data.get('relationship_strength', 0.5),
            company_data.get('sector_fit', 0.5),
            company_data.get('geographic_proximity', 0.5),
            project_data.get('timing_score', 0.5)
        ]
        return np.array(features).reshape(1, -1)
    
    def train(self, X: np.ndarray, y: np.ndarray):
        """Train the model."""
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
        self.is_trained = True
    
    def predict(self, project_data: Dict[str, Any], company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict win probability for a project."""
        features = self._extract_features(project_data, company_data)
        
        if self.is_trained:
            features_scaled = self.scaler.transform(features)
            probability = self.model.predict_proba(features_scaled)[0][1]
        else:
            # Heuristic-based prediction when model isn't trained
            probability = self._heuristic_prediction(project_data, company_data)
        
        # Determine confidence based on data completeness
        confidence = self._calculate_confidence(project_data, company_data)
        
        return {
            'win_probability': round(float(probability), 3),
            'confidence': round(float(confidence), 3),
            'model_version': self.model_version,
            'features_used': self.feature_names,
            'feature_values': features.flatten().tolist()
        }
    
    def _heuristic_prediction(self, project_data: Dict, company_data: Dict) -> float:
        """Heuristic-based prediction when model isn't trained."""
        base_prob = 0.3
        
        # Adjust based on past win rate
        past_win_rate = company_data.get('past_win_rate', 0.3)
        base_prob += (past_win_rate - 0.3) * 0.5
        
        # Adjust based on sector fit
        sector_fit = company_data.get('sector_fit', 0.5)
        base_prob += (sector_fit - 0.5) * 0.3
        
        # Adjust based on relationship strength
        relationship = company_data.get('relationship_strength', 0.5)
        base_prob += (relationship - 0.5) * 0.2
        
        # Adjust based on competition
        competitors = project_data.get('competitor_count', 5)
        if competitors > 10:
            base_prob *= 0.8
        elif competitors < 3:
            base_prob *= 1.2
        
        return max(0.05, min(0.95, base_prob))
    
    def _calculate_confidence(self, project_data: Dict, company_data: Dict) -> float:
        """Calculate prediction confidence based on data completeness."""
        required_fields = ['value', 'sector', 'city', 'state']
        company_fields = ['years_experience', 'past_win_rate']
        
        project_completeness = sum(1 for f in required_fields if project_data.get(f)) / len(required_fields)
        company_completeness = sum(1 for f in company_fields if company_data.get(f)) / len(company_fields)
        
        base_confidence = 0.5 + (project_completeness * 0.25) + (company_completeness * 0.25)
        
        if self.is_trained:
            base_confidence += 0.1
        
        return min(0.95, base_confidence)
    
    def save(self, path: str):
        """Save model to disk."""
        with open(path, 'wb') as f:
            pickle.dump({'model': self.model, 'scaler': self.scaler, 'is_trained': self.is_trained}, f)
    
    def load(self, path: str):
        """Load model from disk."""
        if os.path.exists(path):
            with open(path, 'rb') as f:
                data = pickle.load(f)
                self.model = data['model']
                self.scaler = data['scaler']
                self.is_trained = data['is_trained']
