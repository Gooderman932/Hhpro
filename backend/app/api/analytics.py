"""Analytics API endpoints."""
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from ..database import get_db
from ..models.project import Project
from ..models.user import User
from ..utils.auth_utils import get_current_active_user

router = APIRouter(prefix="", tags=["Analytics"])


@router.get("/summary")
async def get_analytics_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Get analytics summary for the dashboard."""
    tenant_id = current_user.tenant_id
    
    # Total projects
    total_projects = db.query(func.count(Project.id)).filter(
        Project.tenant_id == tenant_id
    ).scalar()
    
    # Active projects
    active_projects = db.query(func.count(Project.id)).filter(
        Project.tenant_id == tenant_id,
        Project.status == "active"
    ).scalar()
    
    # Total value
    total_value = db.query(func.sum(Project.value)).filter(
        Project.tenant_id == tenant_id
    ).scalar() or 0
    
    # Projects by sector
    projects_by_sector = db.query(
        Project.sector,
        func.count(Project.id).label("count")
    ).filter(
        Project.tenant_id == tenant_id,
        Project.sector.isnot(None)
    ).group_by(Project.sector).all()
    
    sector_distribution = {sector: count for sector, count in projects_by_sector}
    
    return {
        "total_projects": total_projects,
        "active_projects": active_projects,
        "total_value": total_value,
        "sector_distribution": sector_distribution,
    }


@router.get("/trends")
async def get_project_trends(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Get project trends over time."""
    tenant_id = current_user.tenant_id
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Projects created over time
    projects_over_time = db.query(
        func.date(Project.created_at).label("date"),
        func.count(Project.id).label("count")
    ).filter(
        Project.tenant_id == tenant_id,
        Project.created_at >= start_date
    ).group_by(func.date(Project.created_at)).all()
    
    trends = [
        {"date": str(date), "count": count}
        for date, count in projects_over_time
    ]
    
    return {"trends": trends}


@router.get("/regions")
async def get_regional_analysis(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Get regional analysis of projects."""
    tenant_id = current_user.tenant_id
    
    # Projects by state
    projects_by_state = db.query(
        Project.state,
        func.count(Project.id).label("count"),
        func.sum(Project.value).label("total_value")
    ).filter(
        Project.tenant_id == tenant_id,
        Project.state.isnot(None)
    ).group_by(Project.state).all()
    
    regional_data = [
        {
            "state": state,
            "project_count": count,
            "total_value": float(total_value) if total_value else 0
        }
        for state, count, total_value in projects_by_state
    ]
    
    return {"regions": regional_data}
