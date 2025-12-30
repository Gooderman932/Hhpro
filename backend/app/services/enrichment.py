"""Data enrichment service for enhancing project data."""
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from ..models.project import Project


class EnrichmentService:
    """Service for enriching project data with additional information."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def enrich_project(self, project: Project) -> Project:
        """Enrich a project with additional data."""
        # Add geocoding if coordinates are missing
        if not project.latitude or not project.longitude:
            self._add_geocoding(project)
        
        # Standardize sector classification
        if project.sector:
            project.sector = self._standardize_sector(project.sector)
        
        # Verify project data
        project.is_verified = self._verify_project(project)
        
        self.db.commit()
        self.db.refresh(project)
        return project
    
    def _add_geocoding(self, project: Project) -> None:
        """Add geocoding to project (placeholder for actual geocoding API)."""
        # In production, this would call a geocoding API like Google Maps
        # For now, we'll just mark it as needing geocoding
        if project.city and project.state:
            # Placeholder - would get actual coordinates
            pass
    
    def _standardize_sector(self, sector: str) -> str:
        """Standardize sector names."""
        sector_mapping = {
            "commercial": "Commercial",
            "residential": "Residential",
            "infrastructure": "Infrastructure",
            "industrial": "Industrial",
            "institutional": "Institutional",
            "healthcare": "Healthcare",
            "education": "Education",
            "transportation": "Transportation",
            "utilities": "Utilities",
        }
        
        sector_lower = sector.lower()
        return sector_mapping.get(sector_lower, sector.title())
    
    def _verify_project(self, project: Project) -> bool:
        """Verify project data completeness and quality."""
        required_fields = [
            project.title,
            project.project_type,
            project.city,
            project.state,
        ]
        
        return all(field is not None for field in required_fields)
