"""Data ingestion service for importing project data."""
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from ..models.project import Project
from ..utils.data_utils import normalize_string, parse_currency


class DataIngestionService:
    """Service for ingesting project data from various sources."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def ingest_project(self, data: Dict[str, Any], tenant_id: int, source: str) -> Project:
        """Ingest a single project from raw data."""
        project = Project(
            title=data.get("title", "Untitled Project"),
            description=data.get("description"),
            project_type=data.get("project_type", "opportunity"),
            sector=normalize_string(data.get("sector")),
            status=data.get("status", "active"),
            value=self._parse_value(data.get("value")),
            address=data.get("address"),
            city=normalize_string(data.get("city")),
            state=data.get("state", "").upper() if data.get("state") else None,
            zip_code=data.get("zip_code"),
            country=data.get("country", "USA"),
            source=source,
            source_url=data.get("source_url"),
            tenant_id=tenant_id,
        )
        
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project
    
    def ingest_batch(
        self,
        data_list: List[Dict[str, Any]],
        tenant_id: int,
        source: str
    ) -> List[Project]:
        """Ingest multiple projects in batch."""
        projects = []
        for data in data_list:
            try:
                project = self.ingest_project(data, tenant_id, source)
                projects.append(project)
            except Exception as e:
                print(f"Error ingesting project: {e}")
                continue
        
        return projects
    
    def _parse_value(self, value: Any) -> Optional[float]:
        """Parse project value from various formats."""
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            return parse_currency(value)
        return None
