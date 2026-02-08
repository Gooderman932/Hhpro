"""
Federal Procurement Service - SAM.gov & USAspending.gov
Fetches construction-related federal contract opportunities and award stats.
"""
import os
import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime

SAM_BASE = "https://api.sam.gov/prod/opportunities/v2"
USA_SPENDING_BASE = "https://api.usaspending.gov/api/v2"

# Construction-related NAICS codes
CONSTRUCTION_NAICS = [
    "236220",  # Commercial building construction
    "236210",  # Industrial building construction
    "236115",  # New single-family housing
    "236116",  # New multifamily housing
    "236117",  # New housing for-sale builders
    "236118",  # Residential remodelers
    "237110",  # Water and sewer line
    "237310",  # Highway, street, bridge
    "238110",  # Poured concrete
    "238120",  # Structural steel
    "238130",  # Framing
    "238140",  # Masonry
    "238150",  # Glass and glazing
    "238160",  # Roofing
    "238170",  # Siding
    "238190",  # Other specialty trade
    "238210",  # Electrical
    "238220",  # Plumbing/HVAC
    "238290",  # Other building equipment
    "238310",  # Drywall and insulation
    "238320",  # Painting
    "238330",  # Flooring
    "238340",  # Tile and terrazzo
    "238350",  # Finish carpentry
    "238390",  # Other building finishing
    "238910",  # Site preparation
    "238990",  # All other specialty trade
]

# State FIPS for USAspending
STATE_FIPS = {
    "AL":"01","AK":"02","AZ":"04","AR":"05","CA":"06","CO":"08","CT":"09","DE":"10",
    "DC":"11","FL":"12","GA":"13","HI":"15","ID":"16","IL":"17","IN":"18","IA":"19",
    "KS":"20","KY":"21","LA":"22","ME":"23","MD":"24","MA":"25","MI":"26","MN":"27",
    "MS":"28","MO":"29","MT":"30","NE":"31","NV":"32","NH":"33","NJ":"34","NM":"35",
    "NY":"36","NC":"37","ND":"38","OH":"39","OK":"40","OR":"41","PA":"42","RI":"44",
    "SC":"45","SD":"46","TN":"47","TX":"48","UT":"49","VT":"50","VA":"51","WA":"53",
    "WV":"54","WI":"55","WY":"56","PR":"72",
}


class FederalProcurementService:
    """Federal procurement data from SAM.gov and USAspending.gov."""

    def __init__(self):
        self.sam_key = os.environ.get("SAM_API_KEY", "")
        self.usa_key = os.environ.get("USASPENDING_API_KEY", "")

    async def get_construction_opportunities(
        self, state_code: Optional[str] = None, limit: int = 25
    ) -> List[Dict[str, Any]]:
        """Fetch active federal construction opportunities from SAM.gov."""
        results: List[Dict[str, Any]] = []

        # Try SAM.gov API first
        if self.sam_key:
            results = await self._fetch_sam(state_code, limit)

        # Fallback / supplement with USAspending recent awards
        if len(results) < limit:
            usa_results = await self._fetch_usaspending_opportunities(state_code, limit - len(results))
            results.extend(usa_results)

        return results[:limit]

    async def _fetch_sam(self, state: Optional[str], limit: int) -> List[Dict]:
        """Fetch opportunities from SAM.gov API."""
        import requests
        from datetime import datetime, timedelta
        
        try:
            # Build date range - SAM.gov requires max 1 year range
            today = datetime.utcnow()
            posted_from = (today - timedelta(days=90)).strftime("%m/%d/%Y")  # Last 90 days
            posted_to = today.strftime("%m/%d/%Y")
            
            # Build parameters for SAM.gov Opportunities API
            params = {
                "api_key": self.sam_key,
                "limit": str(min(limit, 100)),
                "postedFrom": posted_from,
                "postedTo": posted_to,
                "ptype": "o,k,p",  # Solicitation, Combined Synopsis, Presolicitation
            }
            
            # Add NAICS codes for construction
            params["naics"] = ",".join(CONSTRUCTION_NAICS[:5])
            
            # Add state filter if provided
            if state:
                params["state"] = state
            
            print(f"[SAM.gov] Fetching opportunities ({posted_from} to {posted_to})...")
            
            resp = requests.get(
                f"{SAM_BASE}/search",
                params=params,
                timeout=20,
                headers={"Accept": "application/json"}
            )
            
            if resp.status_code == 200:
                data = resp.json()
                opps = data.get("opportunitiesData") or []
                total = data.get("totalRecords", 0)
                print(f"[SAM.gov] Found {len(opps)} of {total} total opportunities")
                return [self._normalize_sam(o) for o in opps[:limit]]
            else:
                print(f"[SAM.gov] Error {resp.status_code}: {resp.text[:200]}")
                
        except Exception as e:
            print(f"[SAM.gov] Error: {e}")
        
        return []

    async def _fetch_usaspending_opportunities(self, state: Optional[str], limit: int) -> List[Dict]:
        """Fetch recent construction awards from USAspending as opportunity proxies."""
        import requests
        import asyncio
        from concurrent.futures import ThreadPoolExecutor
        
        payload = {
            "filters": {
                "time_period": [{"start_date": "2024-01-01", "end_date": "2025-12-31"}],
                "naics_codes": ["236220", "236210", "237110", "238310"],
                "award_type_codes": ["A", "B", "C", "D"]
            },
            "fields": [
                "Award ID", "Recipient Name", "Description", "Award Amount",
                "Start Date", "End Date", "Awarding Agency", "Place of Performance State Code",
                "Place of Performance City Name", "NAICS Code", "internal_id"
            ],
            "limit": min(limit * 3, 100),
            "page": 1,
            "sort": "Award Amount",
            "order": "desc"
        }
        
        def sync_fetch():
            try:
                # Disable SSL verification as workaround for container environments
                import urllib3
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                
                session = requests.Session()
                resp = session.post(
                    f"{USA_SPENDING_BASE}/search/spending_by_award/",
                    json=payload,
                    headers={
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "User-Agent": "Mozilla/5.0 (compatible; HHDrywallPro/2.0)"
                    },
                    timeout=30,
                    verify=False  # Workaround for container SSL issues
                )
                if resp.status_code == 200:
                    data = resp.json()
                    results = data.get("results") or []
                    print(f"USAspending returned {len(results)} results")
                    return results
                else:
                    print(f"USAspending returned {resp.status_code}: {resp.text[:100]}")
            except Exception as e:
                print(f"USAspending error: {e}")
            return []
        
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as pool:
            results = await loop.run_in_executor(pool, sync_fetch)
        
        normalized = [self._normalize_usaspending(r) for r in results]
        if state:
            filtered = [o for o in normalized if o.get("place_of_performance_state") == state]
            if filtered:
                return filtered[:limit]
        
        return normalized[:limit]

    async def get_award_stats(self, state_code: Optional[str] = None, fy: Optional[int] = None) -> Dict[str, Any]:
        """Aggregate award stats for construction NAICS in a state."""
        try:
            year = fy or datetime.utcnow().year
            filters: Dict[str, Any] = {
                "time_period": [{"start_date": f"{year}-01-01", "end_date": f"{year}-12-31"}],
                "naics_codes": CONSTRUCTION_NAICS[:15],
            }
            if state_code and state_code in STATE_FIPS:
                filters["place_of_performance_locations"] = [{"country": "USA", "state": state_code}]

            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.post(
                    f"{USA_SPENDING_BASE}/search/spending_by_award_count/",
                    json={"filters": filters},
                    headers={"Content-Type": "application/json"},
                )
                if resp.status_code == 200:
                    data = resp.json()
                    return {
                        "state": state_code or "US",
                        "fiscal_year": year,
                        "results": data.get("results", {}),
                        "source": "USAspending.gov",
                    }
        except Exception as e:
            print(f"USAspending stats error: {e}")

        return {"state": state_code or "US", "fiscal_year": fy or datetime.utcnow().year, "results": {}, "source": "USAspending.gov (unavailable)"}

    def _normalize_sam(self, raw: Dict) -> Dict[str, Any]:
        return {
            "opportunity_id": raw.get("noticeId") or raw.get("solicitationNumber") or "",
            "title": raw.get("title") or "",
            "agency": raw.get("department") or raw.get("subtierAgency") or "",
            "naics": raw.get("naicsCode") or "",
            "place_of_performance_state": raw.get("placeOfPerformance", {}).get("state", {}).get("code", ""),
            "place_of_performance_city": raw.get("placeOfPerformance", {}).get("city", {}).get("name"),
            "estimated_value": _to_float(raw.get("award", {}).get("amount")),
            "response_deadline": raw.get("responseDeadLine") or raw.get("archiveDate"),
            "notice_type": raw.get("noticeType") or raw.get("type") or "",
            "url": raw.get("uiLink") or f"https://sam.gov/opp/{raw.get('noticeId', '')}",
            "description": raw.get("description") or raw.get("title") or "",
            "source": "sam.gov",
            "raw": raw,
        }

    def _normalize_usaspending(self, raw: Dict) -> Dict[str, Any]:
        return {
            "opportunity_id": raw.get("Award ID") or raw.get("internal_id") or "",
            "title": raw.get("Description") or raw.get("Recipient Name") or "",
            "agency": raw.get("Awarding Agency") or "",
            "naics": raw.get("NAICS Code") or "",
            "place_of_performance_state": raw.get("Place of Performance State Code") or "",
            "place_of_performance_city": raw.get("Place of Performance City Name"),
            "estimated_value": _to_float(raw.get("Award Amount")),
            "response_deadline": raw.get("End Date"),
            "notice_type": "Award",
            "url": f"https://www.usaspending.gov/award/{raw.get('internal_id', '')}",
            "description": raw.get("Description") or "",
            "source": "usaspending.gov",
            "raw": raw,
        }


def _to_float(val) -> Optional[float]:
    if val is None:
        return None
    try:
        return float(str(val).replace(",", "").replace("$", ""))
    except (ValueError, TypeError):
        return None
