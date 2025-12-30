"""Project classification service using AI."""
from typing import Optional
from sqlalchemy.orm import Session
from ..models.project import Project


class ClassificationService:
    """Service for classifying projects using AI/ML."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def classify_project(self, project: Project) -> dict:
        """Classify a project into sector and type categories."""
        # In production, this would use OpenAI or a trained model
        # For now, use rule-based classification
        
        classification = {
            "sector": self._classify_sector(project),
            "project_type": self._classify_type(project),
            "confidence": 0.85,
        }
        
        # Update project if sector is not set
        if not project.sector and classification["sector"]:
            project.sector = classification["sector"]
            self.db.commit()
        
        return classification
    
    def _classify_sector(self, project: Project) -> Optional[str]:
        """Classify project sector based on description and title."""
        if project.sector:
            return project.sector
        
        text = f"{project.title} {project.description or ''}".lower()
        
        # Simple keyword-based classification
        if any(word in text for word in ["hospital", "clinic", "medical", "healthcare"]):
            return "Healthcare"
        elif any(word in text for word in ["school", "university", "college", "education"]):
            return "Education"
        elif any(word in text for word in ["office", "retail", "shopping", "commercial"]):
            return "Commercial"
        elif any(word in text for word in ["apartment", "housing", "residential", "home"]):
            return "Residential"
        elif any(word in text for word in ["bridge", "road", "highway", "infrastructure"]):
            return "Infrastructure"
        elif any(word in text for word in ["factory", "warehouse", "industrial", "manufacturing"]):
            return "Industrial"
        
        return None
    
    def _classify_type(self, project: Project) -> str:
        """Classify project type."""
        if project.project_type:
            return project.project_type
        
        text = f"{project.title} {project.description or ''}".lower()
        
        if any(word in text for word in ["permit", "building permit"]):
            return "permit"
        elif any(word in text for word in ["tender", "bid", "rfp"]):
            return "tender"
        else:
            return "opportunity"
