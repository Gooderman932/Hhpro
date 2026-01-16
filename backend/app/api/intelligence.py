"""Competitive intelligence API endpoints."""
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from ..database import get_db
from ..models.project import Project, ProjectParticipation
from ..models.company import Company
from ..models.user import User
from ..utils.auth_utils import get_current_active_user

router = APIRouter(prefix="/intelligence", tags=["Intelligence"])


@router.get("/competitors")
async def get_competitors(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> List[Dict[str, Any]]:
    """Get competitive intelligence on other companies."""
    tenant_id = current_user.tenant_id
    
    # Get companies with most project participations
    competitor_data = db.query(
        Company.id,
        Company.name,
        Company.company_type,
        func.count(ProjectParticipation.id).label("project_count"),
        func.sum(
            func.cast(ProjectParticipation.won, int)
        ).label("wins")
    ).join(
        ProjectParticipation, Company.id == ProjectParticipation.company_id
    ).filter(
        Company.tenant_id == tenant_id
    ).group_by(
        Company.id, Company.name, Company.company_type
    ).order_by(
        func.count(ProjectParticipation.id).desc()
    ).limit(limit).all()
    
    competitors = [
        {
            "id": comp_id,
            "name": name,
            "company_type": comp_type,
            "project_count": proj_count,
            "wins": wins or 0,
            "win_rate": (wins / proj_count) if proj_count > 0 and wins else 0
        }
        for comp_id, name, comp_type, proj_count, wins in competitor_data
    ]
    
    return competitors


@router.get("/market-share")
async def get_market_share(
    sector: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Get market share analysis by sector."""
    tenant_id = current_user.tenant_id
    
    query = db.query(
        Company.name,
        func.count(ProjectParticipation.id).label("participation_count"),
        func.sum(Project.value).label("total_value")
    ).join(
        ProjectParticipation, Company.id == ProjectParticipation.company_id
    ).join(
        Project, ProjectParticipation.project_id == Project.id
    ).filter(
        Company.tenant_id == tenant_id,
        Project.tenant_id == tenant_id
    )
    
    if sector:
        query = query.filter(Project.sector == sector)
    
    market_data = query.group_by(Company.name).order_by(
        func.count(ProjectParticipation.id).desc()
    ).limit(20).all()
    
    total_participations = sum(count for _, count, _ in market_data)
    
    market_share = [
        {
            "company": name,
            "participations": count,
            "market_share": (count / total_participations * 100) if total_participations > 0 else 0,
            "total_value": float(value) if value else 0
        }
        for name, count, value in market_data
    ]
    
    return {"sector": sector or "all", "market_share": market_share}


@router.get("/relationships")
async def get_relationship_graph(
    company_id: int = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Get relationship graph for a company."""
    tenant_id = current_user.tenant_id
    
    # Get the main company
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.tenant_id == tenant_id
    ).first()
    
    if not company:
        return {"error": "Company not found"}
    
    # Get projects the company is involved in
    projects = db.query(Project).join(
        ProjectParticipation, Project.id == ProjectParticipation.project_id
    ).filter(
        ProjectParticipation.company_id == company_id,
        Project.tenant_id == tenant_id
    ).all()
    
    # Get other companies on the same projects
    related_companies = db.query(
        Company.id,
        Company.name,
        func.count(ProjectParticipation.project_id).label("shared_projects")
    ).join(
        ProjectParticipation, Company.id == ProjectParticipation.company_id
    ).filter(
        ProjectParticipation.project_id.in_([p.id for p in projects]),
        Company.id != company_id,
        Company.tenant_id == tenant_id
    ).group_by(Company.id, Company.name).all()
    
    relationships = [
        {
            "company_id": comp_id,
            "company_name": name,
            "shared_projects": count
        }
        for comp_id, name, count in related_companies
    ]
    
    return {
        "company": {
            "id": company.id,
            "name": company.name,
        },
        "relationships": relationships
    }
