"""External data integration services."""
import os
import httpx
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from ..models.user_data import PermitData, EconomicIndicator


class FREDService:
    """Federal Reserve Economic Data API service."""
    
    BASE_URL = "https://api.stlouisfed.org/fred"
    
    # Key construction-related FRED series
    INDICATORS = {
        "TTLCONS": {"name": "Total Construction Spending", "category": "construction"},
        "PRRESCONS": {"name": "Private Residential Construction", "category": "housing"},
        "PNRESCONS": {"name": "Private Nonresidential Construction", "category": "commercial"},
        "HOUST": {"name": "Housing Starts", "category": "housing"},
        "PERMIT": {"name": "Building Permits", "category": "permits"},
        "WPUSI012011": {"name": "PPI: Lumber", "category": "materials"},
        "WPU101": {"name": "PPI: Iron and Steel", "category": "materials"},
        "PCU23712371": {"name": "PPI: Concrete Products", "category": "materials"},
        "CES2000000001": {"name": "Construction Employment", "category": "employment"},
        "CES2000000003": {"name": "Construction Avg Hourly Earnings", "category": "wages"},
    }
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("FRED_API_KEY", "demo")
    
    async def fetch_series(self, series_id: str, limit: int = 12) -> Dict[str, Any]:
        """Fetch time series data from FRED."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.BASE_URL}/series/observations",
                    params={
                        "series_id": series_id,
                        "api_key": self.api_key,
                        "file_type": "json",
                        "sort_order": "desc",
                        "limit": limit
                    },
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    observations = data.get("observations", [])
                    return {
                        "series_id": series_id,
                        "observations": observations,
                        "success": True
                    }
            except Exception as e:
                print(f"FRED API error for {series_id}: {e}")
        
        return {"series_id": series_id, "observations": [], "success": False}
    
    async def get_all_indicators(self) -> List[Dict[str, Any]]:
        """Fetch all construction-related indicators."""
        results = []
        
        for series_id, info in self.INDICATORS.items():
            data = await self.fetch_series(series_id, limit=6)
            
            if data["success"] and data["observations"]:
                obs = data["observations"]
                current = float(obs[0]["value"]) if obs[0]["value"] != "." else None
                previous = float(obs[1]["value"]) if len(obs) > 1 and obs[1]["value"] != "." else None
                
                pct_change = None
                if current and previous and previous != 0:
                    pct_change = ((current - previous) / previous) * 100
                
                results.append({
                    "code": series_id,
                    "name": info["name"],
                    "category": info["category"],
                    "value": current,
                    "previous_value": previous,
                    "percent_change": round(pct_change, 2) if pct_change else None,
                    "date": obs[0]["date"],
                    "trend": "up" if pct_change and pct_change > 0 else "down" if pct_change and pct_change < 0 else "stable"
                })
        
        return results
    
    def cache_indicators(self, db: Session, indicators: List[Dict[str, Any]]):
        """Cache indicators in database."""
        for ind in indicators:
            existing = db.query(EconomicIndicator).filter(
                EconomicIndicator.indicator_code == ind["code"],
                EconomicIndicator.period_date == datetime.strptime(ind["date"], "%Y-%m-%d")
            ).first()
            
            if not existing:
                record = EconomicIndicator(
                    indicator_code=ind["code"],
                    indicator_name=ind["name"],
                    category=ind["category"],
                    value=ind["value"],
                    previous_value=ind["previous_value"],
                    percent_change=ind["percent_change"],
                    region="national",
                    period_date=datetime.strptime(ind["date"], "%Y-%m-%d"),
                    period_type="monthly"
                )
                db.add(record)
        
        db.commit()


class PermitDataService:
    """Construction permit data service."""
    
    # Simulated permit data for demo - in production, integrate with real APIs
    # Options: BuildZoom API, PermitData.org, City Open Data Portals
    
    SAMPLE_PERMITS = [
        {"permit_type": "commercial", "sector": "Office", "value_range": (500000, 5000000)},
        {"permit_type": "commercial", "sector": "Retail", "value_range": (200000, 2000000)},
        {"permit_type": "commercial", "sector": "Healthcare", "value_range": (1000000, 20000000)},
        {"permit_type": "residential", "sector": "Multi-Family", "value_range": (500000, 10000000)},
        {"permit_type": "residential", "sector": "Single-Family", "value_range": (200000, 1000000)},
        {"permit_type": "industrial", "sector": "Warehouse", "value_range": (1000000, 15000000)},
        {"permit_type": "renovation", "sector": "Commercial Renovation", "value_range": (100000, 2000000)},
    ]
    
    CITIES = {
        "TX": ["Austin", "Houston", "Dallas", "San Antonio", "Fort Worth"],
        "AZ": ["Phoenix", "Scottsdale", "Tucson", "Mesa", "Tempe"],
        "FL": ["Miami", "Tampa", "Orlando", "Jacksonville", "Fort Lauderdale"],
        "CA": ["Los Angeles", "San Diego", "San Francisco", "San Jose", "Sacramento"],
        "CO": ["Denver", "Colorado Springs", "Aurora", "Boulder", "Fort Collins"],
    }
    
    CONTRACTORS = [
        "ABC Construction Co", "BuildRight Inc", "Premier Builders", "Quality Construction",
        "Metro Builders", "Apex Construction", "Summit Development", "CoreBuild LLC",
        "Landmark Construction", "Precision Builders", "Elite Construction Group"
    ]
    
    async def fetch_permits(
        self,
        states: List[str] = None,
        cities: List[str] = None,
        permit_type: str = None,
        min_value: float = None,
        max_value: float = None,
        limit: int = 25
    ) -> List[Dict[str, Any]]:
        """Fetch construction permits based on filters."""
        import random
        
        permits = []
        states = states or list(self.CITIES.keys())
        
        for i in range(limit):
            state = random.choice(states)
            available_cities = self.CITIES.get(state, ["Unknown"])
            city = random.choice(cities) if cities and any(c in available_cities for c in cities) else random.choice(available_cities)
            
            permit_info = random.choice(self.SAMPLE_PERMITS)
            if permit_type and permit_info["permit_type"] != permit_type:
                continue
            
            value = random.randint(int(permit_info["value_range"][0]), int(permit_info["value_range"][1]))
            
            if min_value and value < min_value:
                continue
            if max_value and value > max_value:
                continue
            
            issue_date = datetime.now() - timedelta(days=random.randint(1, 30))
            
            permits.append({
                "permit_number": f"PER-{state}-{random.randint(100000, 999999)}",
                "permit_type": permit_info["permit_type"],
                "sector": permit_info["sector"],
                "project_name": f"{permit_info['sector']} Project - {city}",
                "description": f"New {permit_info['sector'].lower()} construction project",
                "estimated_value": value,
                "address": f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Commerce', 'Industrial', 'Park'])} {random.choice(['St', 'Ave', 'Blvd', 'Dr'])}",
                "city": city,
                "state": state,
                "zip_code": f"{random.randint(10000, 99999)}",
                "owner_name": f"{random.choice(['Smith', 'Johnson', 'Williams', 'Brown', 'Davis'])} {random.choice(['Properties', 'Investments', 'Development', 'Holdings', 'Group'])}",
                "contractor_name": random.choice(self.CONTRACTORS),
                "issue_date": issue_date.isoformat(),
                "expiration_date": (issue_date + timedelta(days=365)).isoformat()
            })
        
        return permits
    
    def cache_permits(self, db: Session, permits: List[Dict[str, Any]]):
        """Cache permits in database."""
        for permit in permits:
            existing = db.query(PermitData).filter(
                PermitData.permit_number == permit["permit_number"]
            ).first()
            
            if not existing:
                record = PermitData(
                    permit_number=permit["permit_number"],
                    permit_type=permit["permit_type"],
                    project_name=permit["project_name"],
                    description=permit["description"],
                    estimated_value=permit["estimated_value"],
                    address=permit["address"],
                    city=permit["city"],
                    state=permit["state"],
                    zip_code=permit["zip_code"],
                    owner_name=permit["owner_name"],
                    contractor_name=permit["contractor_name"],
                    sector=permit["sector"],
                    issue_date=datetime.fromisoformat(permit["issue_date"]),
                    expiration_date=datetime.fromisoformat(permit["expiration_date"])
                )
                db.add(record)
        
        db.commit()


class IndustryBenchmarkService:
    """Industry benchmark calculations."""
    
    @staticmethod
    def calculate_benchmarks(db: Session, user_sector: str = None) -> Dict[str, Any]:
        """Calculate industry benchmarks from permit data."""
        from sqlalchemy import func
        
        # Average project values by sector
        sector_avgs = db.query(
            PermitData.sector,
            func.avg(PermitData.estimated_value).label("avg_value"),
            func.count(PermitData.id).label("count")
        ).group_by(PermitData.sector).all()
        
        sector_benchmarks = [
            {
                "sector": s.sector,
                "average_value": round(s.avg_value, 0) if s.avg_value else 0,
                "project_count": s.count
            }
            for s in sector_avgs
        ]
        
        # Regional activity
        regional_activity = db.query(
            PermitData.state,
            func.count(PermitData.id).label("permit_count"),
            func.sum(PermitData.estimated_value).label("total_value")
        ).group_by(PermitData.state).order_by(func.count(PermitData.id).desc()).limit(10).all()
        
        regional_data = [
            {
                "state": r.state,
                "permit_count": r.permit_count,
                "total_value": round(r.total_value, 0) if r.total_value else 0
            }
            for r in regional_activity
        ]
        
        # Top contractors
        top_contractors = db.query(
            PermitData.contractor_name,
            func.count(PermitData.id).label("project_count"),
            func.sum(PermitData.estimated_value).label("total_value")
        ).group_by(PermitData.contractor_name).order_by(func.sum(PermitData.estimated_value).desc()).limit(10).all()
        
        contractor_rankings = [
            {
                "name": c.contractor_name,
                "project_count": c.project_count,
                "total_value": round(c.total_value, 0) if c.total_value else 0,
                "market_share": 0  # Calculate later
            }
            for c in top_contractors
        ]
        
        return {
            "sector_benchmarks": sector_benchmarks,
            "regional_activity": regional_data,
            "top_contractors": contractor_rankings,
            "generated_at": datetime.utcnow().isoformat()
        }
