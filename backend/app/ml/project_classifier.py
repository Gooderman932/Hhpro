"""
Project Classification Service
Automatically classifies construction projects by type, size, and stage using ML + LLM
"""
import re
from typing import Dict, List, Optional, Tuple
import numpy as np
import openai
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
from loguru import logger

from app.config import settings
from app.models.project import ProjectType, ProjectStage


class ProjectClassifier:
    """
    Multi-label classifier for construction projects
    """
    
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # ML models
        self.type_classifier = None
        self.stage_classifier = None
        self.vectorizer = TfidfVectorizer(max_features=500, ngram_range=(1, 3))
        self.label_encoders = {}
        
        # Project type keywords (for rule-based fallback)
        self.type_keywords = {
            ProjectType.COMMERCIAL: [
                'office', 'retail', 'shopping', 'mall', 'store', 'restaurant', 
                'hotel', 'commercial', 'mixed-use'
            ],
            ProjectType.RESIDENTIAL: [
                'apartment', 'condo', 'housing', 'residential', 'home', 'townhouse',
                'multifamily', 'single-family', 'duplex'
            ],
            ProjectType.INDUSTRIAL: [
                'warehouse', 'manufacturing', 'factory', 'industrial', 'plant',
                'distribution', 'assembly', 'production'
            ],
            ProjectType.INFRASTRUCTURE: [
                'road', 'bridge', 'highway', 'tunnel', 'transit', 'rail', 'airport',
                'port', 'utility', 'water', 'sewer', 'pipeline'
            ],
            ProjectType.DATA_CENTER: [
                'data center', 'datacenter', 'server', 'colocation', 'cloud',
                'hyperscale', 'edge computing'
            ],
            ProjectType.LOGISTICS: [
                'logistics', 'fulfillment', 'distribution center', 'cold storage',
                'warehouse', 'e-commerce', 'sortation'
            ],
            ProjectType.HEALTHCARE: [
                'hospital', 'medical', 'healthcare', 'clinic', 'surgery center',
                'nursing home', 'care facility', 'lab', 'pharmacy'
            ],
            ProjectType.EDUCATION: [
                'school', 'university', 'college', 'education', 'campus', 
                'classroom', 'library', 'dormitory', 'student housing'
            ],
            ProjectType.HOSPITALITY: [
                'hotel', 'resort', 'casino', 'convention center', 'hospitality',
                'restaurant', 'entertainment venue'
            ]
        }
        
        self.stage_keywords = {
            ProjectStage.PLANNING: [
                'proposed', 'planning', 'concept', 'feasibility', 'preliminary',
                'under consideration', 'seeking approval'
            ],
            ProjectStage.PERMIT: [
                'permit', 'application', 'approval', 'zoning', 'submitted',
                'under review', 'pending'
            ],
            ProjectStage.TENDER: [
                'tender', 'bid', 'rfp', 'rfq', 'solicitation', 'seeking bids',
                'invitation to bid', 'request for proposal'
            ],
            ProjectStage.AWARDED: [
                'awarded', 'selected', 'won', 'contract signed', 'chosen contractor',
                'announcement'
            ],
            ProjectStage.CONSTRUCTION: [
                'under construction', 'building', 'construction', 'site work',
                'foundation', 'framing', 'in progress'
            ],
            ProjectStage.COMPLETED: [
                'completed', 'finished', 'delivered', 'opened', 'inaugurated',
                'substantial completion', 'final inspection'
            ]
        }
    
    def classify_project_type_rule_based(self, text: str) -> Tuple[ProjectType, float]:
        """
        Rule-based classification using keyword matching
        Returns (project_type, confidence)
        """
        text_lower = text.lower()
        scores = {}
        
        for proj_type, keywords in self.type_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            scores[proj_type] = score
        
        if not scores or max(scores.values()) == 0:
            return ProjectType.OTHER, 0.3
        
        best_type = max(scores, key=scores.get)
        # Normalize confidence based on keyword matches
        confidence = min(scores[best_type] / 3, 1.0)
        
        return best_type, confidence
    
    def classify_project_stage_rule_based(self, text: str) -> Tuple[ProjectStage, float]:
        """Rule-based stage classification"""
        text_lower = text.lower()
        scores = {}
        
        for stage, keywords in self.stage_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            scores[stage] = score
        
        if not scores or max(scores.values()) == 0:
            return ProjectStage.PLANNING, 0.3
        
        best_stage = max(scores, key=scores.get)
        confidence = min(scores[best_stage] / 2, 1.0)
        
        return best_stage, confidence
    
    def classify_with_llm(self, title: str, description: str) -> Dict:
        """
        Use OpenAI to classify project with high accuracy
        More expensive but very accurate
        """
        text = f"{title}\n\n{description}"[:2000]  # Limit to 2000 chars
        
        prompt = f"""Classify this construction project:

Project: {text}

Provide classification in JSON format:
{{
    "project_type": "commercial|residential|industrial|infrastructure|data_center|logistics|healthcare|education|hospitality|mixed_use|other",
    "stage": "planning|permit|tender|bidding|awarded|construction|completed|cancelled",
    "estimated_size": "small|medium|large|mega",
    "confidence": 0.85,
    "reasoning": "Brief explanation"
}}

Use these definitions:
- commercial: office, retail, mixed-use buildings
- residential: apartments, condos, housing
- industrial: manufacturing, warehouses, factories
- infrastructure: roads, bridges, utilities, airports
- data_center: data centers, server facilities
- logistics: distribution centers, fulfillment centers
- healthcare: hospitals, clinics, medical facilities
- education: schools, universities, libraries
- hospitality: hotels, resorts, restaurants

Size:
- small: < $5M or < 50,000 sf
- medium: $5M-$50M or 50,000-250,000 sf
- large: $50M-$500M or 250,000-1M sf
- mega: > $500M or > 1M sf"""

        try:
            response = self.openai_client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert in construction project classification. Return valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
            # Validate and convert to enums
            try:
                result['project_type'] = ProjectType(result['project_type'])
            except:
                result['project_type'] = ProjectType.OTHER
            
            try:
                result['stage'] = ProjectStage(result['stage'])
            except:
                result['stage'] = ProjectStage.PLANNING
            
            return result
            
        except Exception as e:
            logger.error(f"LLM classification failed: {e}")
            return None
    
    def classify_project(self, 
                        title: str, 
                        description: str = "",
                        use_llm: bool = None) -> Dict:
        """
        Classify project using best available method
        
        Strategy:
        1. Try LLM if use_llm=True and API key available (most accurate)
        2. Try trained ML model if available
        3. Fallback to rule-based
        
        Returns:
            {
                'project_type': ProjectType,
                'stage': ProjectStage,
                'confidence': 0.85,
                'size_category': 'medium',
                'method': 'llm|ml|rules'
            }
        """
        text = f"{title} {description}"
        
        # Determine whether to use LLM
        if use_llm is None:
            # Use LLM if confidence threshold not met by rules
            use_llm = settings.OPENAI_API_KEY is not None
        
        # Try LLM first (if enabled)
        if use_llm and settings.OPENAI_API_KEY:
            llm_result = self.classify_with_llm(title, description)
            if llm_result:
                return {
                    **llm_result,
                    'method': 'llm'
                }
        
        # Try ML model (if trained)
        if self.type_classifier is not None:
            try:
                ml_result = self._classify_with_ml(text)
                if ml_result['confidence'] >= settings.MIN_CONFIDENCE_THRESHOLD:
                    return {
                        **ml_result,
                        'method': 'ml'
                    }
            except Exception as e:
                logger.error(f"ML classification failed: {e}")
        
        # Fallback to rule-based
        proj_type, type_conf = self.classify_project_type_rule_based(text)
        stage, stage_conf = self.classify_project_stage_rule_based(text)
        
        return {
            'project_type': proj_type,
            'stage': stage,
            'confidence': (type_conf + stage_conf) / 2,
            'method': 'rules',
            'size_category': self._estimate_size_from_text(text)
        }
    
    def _classify_with_ml(self, text: str) -> Dict:
        """Classify using trained ML model"""
        # Vectorize
        X = self.vectorizer.transform([text])
        
        # Predict type
        type_pred = self.type_classifier.predict(X)[0]
        type_proba = self.type_classifier.predict_proba(X)[0]
        type_conf = max(type_proba)
        
        # Predict stage
        stage_pred = self.stage_classifier.predict(X)[0]
        stage_proba = self.stage_classifier.predict_proba(X)[0]
        stage_conf = max(stage_proba)
        
        # Decode labels
        project_type = self.label_encoders['type'].inverse_transform([type_pred])[0]
        stage = self.label_encoders['stage'].inverse_transform([stage_pred])[0]
        
        return {
            'project_type': ProjectType(project_type),
            'stage': ProjectStage(stage),
            'confidence': (type_conf + stage_conf) / 2,
            'size_category': self._estimate_size_from_text(text)
        }
    
    def _estimate_size_from_text(self, text: str) -> str:
        """Estimate project size category from text"""
        # Extract numbers
        numbers = re.findall(r'\$?[\d,]+\.?\d*\s?(?:million|billion|M|B|K)?', text, re.IGNORECASE)
        
        # Look for square footage
        sf_match = re.search(r'([\d,]+)\s?(?:sf|sq\.?\s?ft\.?|square feet)', text, re.IGNORECASE)
        if sf_match:
            sf = int(sf_match.group(1).replace(',', ''))
            if sf < 50000:
                return 'small'
            elif sf < 250000:
                return 'medium'
            elif sf < 1000000:
                return 'large'
            else:
                return 'mega'
        
        # Look for dollar amounts
        dollar_match = re.search(r'\$?([\d,]+(?:\.\d+)?)\s?(million|billion|M|B)?', text, re.IGNORECASE)
        if dollar_match:
            amount = float(dollar_match.group(1).replace(',', ''))
            unit = dollar_match.group(2).lower() if dollar_match.group(2) else ''
            
            if 'b' in unit or 'billion' in unit:
                amount *= 1000  # Convert to millions
            
            if amount < 5:
                return 'small'
            elif amount < 50:
                return 'medium'
            elif amount < 500:
                return 'large'
            else:
                return 'mega'
        
        return 'unknown'
    
    def train(self, training_data: List[Dict]) -> Dict:
        """
        Train ML classifiers
        
        Args:
            training_data: List of dicts with 'text', 'project_type', 'stage'
        """
        logger.info(f"Training project classifier with {len(training_data)} samples")
        
        texts = [d['text'] for d in training_data]
        types = [d['project_type'] for d in training_data]
        stages = [d['stage'] for d in training_data]
        
        # Vectorize texts
        X = self.vectorizer.fit_transform(texts)
        
        # Encode labels
        self.label_encoders['type'] = LabelEncoder()
        self.label_encoders['stage'] = LabelEncoder()
        
        y_type = self.label_encoders['type'].fit_transform(types)
        y_stage = self.label_encoders['stage'].fit_transform(stages)
        
        # Train classifiers
        self.type_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.stage_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        
        self.type_classifier.fit(X, y_type)
        self.stage_classifier.fit(X, y_stage)
        
        # Evaluate
        type_score = self.type_classifier.score(X, y_type)
        stage_score = self.stage_classifier.score(X, y_stage)
        
        logger.info(f"Training complete - Type acc: {type_score:.3f}, Stage acc: {stage_score:.3f}")
        
        return {
            'type_accuracy': float(type_score),
            'stage_accuracy': float(stage_score),
            'n_samples': len(training_data)
        }


# Global classifier instance
project_classifier = ProjectClassifier()


def classify_project(title: str, description: str = "", use_llm: bool = None) -> Dict:
    """
    Convenience function for project classification
    
    Example:
        result = classify_project(
            "New 500,000 SF Data Center in Dallas",
            "Proposed hyperscale data center facility..."
        )
        
        print(result['project_type'])  # ProjectType.DATA_CENTER
        print(result['confidence'])     # 0.92
    """
    return project_classifier.classify_project(title, description, use_llm)
