"""
Open Data Permits Aggregator - Real Nationwide Permit Data
Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.
PROPRIETARY AND CONFIDENTIAL

Aggregates REAL construction permits from official city/county open data portals.
No mock data. No demo data. Production-quality intelligence.
"""
import os
import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import asyncio

# =============================================================================
# OPEN DATA ENDPOINTS - Real public APIs, no keys required (app tokens optional)
# =============================================================================

OPEN_DATA_SOURCES = {
    # NEW YORK
    "nyc": {
        "name": "New York City",
        "state": "NY",
        "url": "https://data.cityofnewyork.us/resource/ipu4-2q9a.json",
        "date_field": "issuance_date",
        "limit_param": "$limit",
        "order_param": "$order",
        "order_value": "issuance_date DESC",
    },
    # CALIFORNIA
    "los_angeles": {
        "name": "Los Angeles",
        "state": "CA",
        "url": "https://data.lacity.org/resource/nbyu-2ha9.json",
        "date_field": "issue_date",
        "limit_param": "$limit",
        "order_param": "$order",
        "order_value": "issue_date DESC",
    },
    "san_francisco": {
        "name": "San Francisco",
        "state": "CA",
        "url": "https://data.sfgov.org/resource/i98e-djp9.json",
        "date_field": "filed_date",
        "limit_param": "$limit",
        "order_param": "$order",
        "order_value": "filed_date DESC",
    },
    "san_diego": {
        "name": "San Diego",
        "state": "CA",
        "url": "https://data.sandiego.gov/resource/mqqp-hf7t.json",
        "date_field": "approval_date",
        "limit_param": "$limit",
        "order_param": "$order",
        "order_value": "approval_date DESC",
    },
    # ILLINOIS
    "chicago": {
        "name": "Chicago",
        "state": "IL",
        "url": "https://data.cityofchicago.org/resource/ydr8-5enu.json",
        "date_field": "issue_date",
        "limit_param": "$limit",
        "order_param": "$order",
        "order_value": "issue_date DESC",
    },
    # TEXAS
    "austin": {
        "name": "Austin",
        "state": "TX",
        "url": "https://data.austintexas.gov/resource/3syk-w9eu.json",
        "date_field": "issued_date",
        "limit_param": "$limit",
        "order_param": "$order",
        "order_value": "issued_date DESC",
    },
    "dallas": {
        "name": "Dallas",
        "state": "TX",
        "url": "https://www.dallasopendata.com/resource/mxm9-a5iy.json",
        "date_field": "permit_date",
        "limit_param": "$limit",
        "order_param": "$order",
        "order_value": "permit_date DESC",
    },
    "houston": {
        "name": "Houston",
        "state": "TX",
        "url": "https://data.houstontx.gov/resource/q63f-6kza.json",
        "date_field": "date_issued",
        "limit_param": "$limit",
        "order_param": "$order",
        "order_value": "date_issued DESC",
    },
    # FLORIDA
    "miami_dade": {
        "name": "Miami-Dade County",
        "state": "FL",
        "url": "https://opendata.miamidade.gov/resource/gxhd-rqkv.json",
        "date_field": "issue_date",
        "limit_param": "$limit",
        "order_param": "$order",
        "order_value": "issue_date DESC",
    },
    # COLORADO
    "denver": {
        "name": "Denver",
        "state": "CO",
        "url": "https://data.denvergov.org/resource/auq2-hbhx.json",
        "date_field": "issued_date",
        "limit_param": "$limit",
        "order_param": "$order",
        "order_value": "issued_date DESC",
    },
    # WASHINGTON
    "seattle": {
        "name": "Seattle",
        "state": "WA",
        "url": "https://data.seattle.gov/resource/76t5-zqzr.json",
        "date_field": "issue_date",
        "limit_param": "$limit",
        "order_param": "$order",
        "order_value": "issue_date DESC",
    },
    # MASSACHUSETTS
    "boston": {
        "name": "Boston",
        "state": "MA",
        "url": "https://data.boston.gov/resource/hfgw-p5wb.json",
        "date_field": "issued_date",
        "limit_param": "$limit",
        "order_param": "$order",
        "order_value": "issued_date DESC",
    },
    # PENNSYLVANIA
    "philadelphia": {
        "name": "Philadelphia",
        "state": "PA",
        "url": "https://phl.carto.com/api/v2/sql?q=SELECT * FROM permits ORDER BY permitissuedate DESC LIMIT {limit}&format=json",
        "custom_format": True,
        "date_field": "permitissuedate",
    },
    # GEORGIA
    "atlanta": {
        "name": "Atlanta",
        "state": "GA",
        "url": "https://opendata.atlantaga.gov/resource/hfq8-4kgv.json",
        "date_field": "issue_date",
        "limit_param": "$limit",
        "order_param": "$order",
        "order_value": "issue_date DESC",
    },
    # ARIZONA
    "phoenix": {
        "name": "Phoenix",
        "state": "AZ",
        "url": "https://phoenixopendata.com/resource/g6hx-9yjw.json",
        "date_field": "issue_date",
        "limit_param": "$limit",
        "order_param": "$order",
        "order_value": "issue_date DESC",
    },
    # NORTH CAROLINA
    "charlotte": {
        "name": "Charlotte",
        "state": "NC",
        "url": "https://data.charlottenc.gov/resource/wf8s-ucp4.json",
        "date_field": "issue_date",
        "limit_param": "$limit",
        "order_param": "$order",
        "order_value": "issue_date DESC",
    },
    # OREGON
    "portland": {
        "name": "Portland",
        "state": "OR",
        "url": "https://opendata.portland.gov/resource/sxyr-dz3k.json",
        "date_field": "issued_date",
        "limit_param": "$limit",
        "order_param": "$order",
        "order_value": "issued_date DESC",
    },
    # NEVADA
    "las_vegas": {
        "name": "Las Vegas",
        "state": "NV",
        "url": "https://opendata.lasvegasnevada.gov/resource/w3fs-s9wy.json",
        "date_field": "issue_date",
        "limit_param": "$limit",
        "order_param": "$order",
        "order_value": "issue_date DESC",
    },
    # TENNESSEE
    "nashville": {
        "name": "Nashville",
        "state": "TN",
        "url": "https://data.nashville.gov/resource/3h5w-q8b7.json",
        "date_field": "date_issued",
        "limit_param": "$limit",
        "order_param": "$order",
        "order_value": "date_issued DESC",
    },
    # OHIO
    "columbus": {
        "name": "Columbus",
        "state": "OH",
        "url": "https://opendata.columbus.gov/resource/h5wp-qrpm.json",
        "date_field": "issue_date",
        "limit_param": "$limit",
        "order_param": "$order",
        "order_value": "issue_date DESC",
    },
    # MICHIGAN
    "detroit": {
        "name": "Detroit",
        "state": "MI",
        "url": "https://data.detroitmi.gov/resource/xw2a-a7tf.json",
        "date_field": "permit_issued",
        "limit_param": "$limit",
        "order_param": "$order",
        "order_value": "permit_issued DESC",
    },
    # MINNESOTA
    "minneapolis": {
        "name": "Minneapolis",
        "state": "MN",
        "url": "https://opendata.minneapolismn.gov/resource/axt9-gazq.json",
        "date_field": "date_issued",
        "limit_param": "$limit",
        "order_param": "$order",
        "order_value": "date_issued DESC",
    },
}

# Map states to their available cities
STATE_TO_CITIES = {}
for city_key, cfg in OPEN_DATA_SOURCES.items():
    st = cfg["state"]
    if st not in STATE_TO_CITIES:
        STATE_TO_CITIES[st] = []
    STATE_TO_CITIES[st].append(city_key)


class OpenDataPermitsService:
    """
    Aggregates REAL permit data from official city/county open data portals.
    No API keys required. No mock data. Production quality.
    """

    def __init__(self):
        self.socrata_token = os.environ.get("SOCRATA_APP_TOKEN", "")
        self.timeout = 12.0

    async def search_permits(
        self,
        state: Optional[str] = None,
        city: Optional[str] = None,
        limit: int = 50,
    ) -> Dict[str, Any]:
        """
        Search permits across all available open data sources.
        Returns real permits from official government portals.
        """
        results: List[Dict[str, Any]] = []
        sources_queried: List[str] = []
        sources_failed: List[str] = []

        # Determine which sources to query
        sources_to_query = []
        
        if city:
            # Exact city match
            city_key = city.lower().replace(" ", "_").replace("-", "_")
            if city_key in OPEN_DATA_SOURCES:
                sources_to_query = [city_key]
            else:
                # Fuzzy match
                for key, cfg in OPEN_DATA_SOURCES.items():
                    if city.lower() in cfg["name"].lower() or cfg["name"].lower() in city.lower():
                        sources_to_query.append(key)
        elif state:
            # All cities in that state
            sources_to_query = STATE_TO_CITIES.get(state.upper(), [])
        else:
            # Query top metro areas for broad coverage
            sources_to_query = list(OPEN_DATA_SOURCES.keys())[:10]

        if not sources_to_query:
            # Fallback: query major metros
            sources_to_query = ["nyc", "los_angeles", "chicago", "houston", "phoenix"]

        # Fetch from all applicable sources concurrently
        per_source_limit = max(10, limit // len(sources_to_query)) if sources_to_query else limit
        
        tasks = []
        for source_key in sources_to_query:
            if source_key in OPEN_DATA_SOURCES:
                tasks.append(self._fetch_from_source(source_key, per_source_limit))

        if tasks:
            fetched = await asyncio.gather(*tasks, return_exceptions=True)
            for i, result in enumerate(fetched):
                source_key = sources_to_query[i] if i < len(sources_to_query) else "unknown"
                source_name = OPEN_DATA_SOURCES.get(source_key, {}).get("name", source_key)
                if isinstance(result, Exception):
                    sources_failed.append(source_name)
                elif result:
                    results.extend(result)
                    sources_queried.append(f"{source_name} ({len(result)})")

        return {
            "permits": results[:limit],
            "total_fetched": len(results),
            "sources_queried": sources_queried,
            "sources_failed": sources_failed,
            "coverage_note": self._get_coverage_note(state, city),
        }

    async def _fetch_from_source(self, source_key: str, limit: int) -> List[Dict[str, Any]]:
        """Fetch permits from a specific open data source."""
        cfg = OPEN_DATA_SOURCES.get(source_key)
        if not cfg:
            return []

        try:
            headers = {
                "Accept": "application/json",
                "User-Agent": "HHDrywall-Pro-Construction-Intel/2.0",
            }
            if self.socrata_token:
                headers["X-App-Token"] = self.socrata_token

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                if cfg.get("custom_format"):
                    # Handle custom API formats (like Philadelphia CARTO)
                    url = cfg["url"].format(limit=limit)
                    resp = await client.get(url, headers=headers)
                else:
                    # Standard Socrata format
                    params = {
                        cfg["limit_param"]: limit,
                    }
                    if cfg.get("order_param"):
                        params[cfg["order_param"]] = cfg["order_value"]
                    
                    resp = await client.get(cfg["url"], headers=headers, params=params)

                if resp.status_code == 200:
                    data = resp.json()
                    # Handle CARTO format
                    if isinstance(data, dict) and "rows" in data:
                        data = data["rows"]
                    if isinstance(data, list):
                        return [self._normalize_permit(p, cfg) for p in data]
                else:
                    print(f"[OpenData] {cfg['name']} returned {resp.status_code}")
        except Exception as e:
            print(f"[OpenData] {cfg['name']} error: {e}")
        
        return []

    def _normalize_permit(self, raw: Dict, cfg: Dict) -> Dict[str, Any]:
        """Normalize permit data from any source into standard schema."""
        # Extract common fields with multiple fallbacks
        permit_id = (
            raw.get("permit_number") or raw.get("permitnumber") or 
            raw.get("job__") or raw.get("permit_no") or raw.get("permit_id") or
            raw.get("application_number") or raw.get("record_id") or
            raw.get("id") or str(hash(str(raw)))[:12]
        )
        
        # Address construction
        address_parts = []
        for field in ["address", "full_address", "site_address", "location", "street_address",
                      "house__", "street_name", "property_address", "work_location"]:
            if raw.get(field):
                address_parts.append(str(raw[field]).strip())
                break
        
        # If we have house number and street separately
        if not address_parts:
            house = raw.get("house__") or raw.get("house_number") or raw.get("streetno") or ""
            street = raw.get("street_name") or raw.get("street") or raw.get("streetname") or ""
            if house or street:
                address_parts.append(f"{house} {street}".strip())
        
        address = address_parts[0] if address_parts else "Address not specified"
        
        # City - use source config or extract from data
        city = (
            raw.get("city") or raw.get("borough") or 
            raw.get("jurisdiction") or cfg.get("name", "")
        )
        if isinstance(city, str):
            city = city.title()
        
        # State from config
        state = cfg.get("state", "")
        
        # Cost extraction with multiple field names
        cost = None
        for cost_field in ["estimated_cost", "job_value", "valuation", "estimated_job_cost__",
                          "initial_cost", "permit_value", "total_fee", "construction_cost",
                          "estimated_value", "project_value"]:
            val = raw.get(cost_field)
            if val:
                cost = self._parse_cost(val)
                if cost:
                    break
        
        # Work type / permit type
        work_type = (
            raw.get("permit_type") or raw.get("work_type") or raw.get("permit_subtype") or
            raw.get("job_type") or raw.get("type") or raw.get("permit_type_descr") or
            raw.get("description_short") or "General Construction"
        )
        
        # Description
        description = (
            raw.get("description") or raw.get("work_description") or raw.get("job_description") or
            raw.get("scope_of_work") or raw.get("proposed_use") or
            raw.get("existing_use") or work_type
        )
        
        # Date
        date_field = cfg.get("date_field", "issue_date")
        filing_date = raw.get(date_field) or raw.get("issue_date") or raw.get("filed_date") or ""
        
        # Status
        status = (
            raw.get("status") or raw.get("permit_status") or raw.get("status_current") or
            raw.get("application_status") or "issued"
        )
        
        # Contractor info
        contractor = (
            raw.get("contractor_name") or raw.get("contractor") or 
            raw.get("applicant_name") or raw.get("owner_s_first_name") or None
        )
        
        # Geo coordinates
        lat = raw.get("latitude") or raw.get("lat") or raw.get("y")
        lng = raw.get("longitude") or raw.get("lng") or raw.get("lon") or raw.get("x")
        
        # Handle nested location objects
        if not lat and raw.get("location"):
            loc = raw["location"]
            if isinstance(loc, dict):
                lat = loc.get("latitude") or loc.get("lat")
                lng = loc.get("longitude") or loc.get("lng") or loc.get("lon")
        
        return {
            "permit_id": str(permit_id),
            "address": address,
            "city": city,
            "state": state,
            "geo": {
                "lat": float(lat) if lat else None,
                "lng": float(lng) if lng else None,
            },
            "work_type": str(work_type)[:100] if work_type else "General",
            "estimated_cost": cost,
            "filing_date": str(filing_date)[:10] if filing_date else "",
            "status": str(status).lower() if status else "issued",
            "contractor_name": contractor,
            "contractor_license": raw.get("license_number") or raw.get("contractor_license"),
            "description": str(description)[:500] if description else "",
            "source": f"open_data_{cfg.get('state', '').lower()}",
            "source_name": cfg.get("name", "Unknown"),
        }

    def _parse_cost(self, val) -> Optional[float]:
        """Parse cost from various formats."""
        if val is None:
            return None
        try:
            cleaned = str(val).replace(",", "").replace("$", "").strip()
            cost = float(cleaned)
            return cost if cost > 0 else None
        except (ValueError, TypeError):
            return None

    def _get_coverage_note(self, state: Optional[str], city: Optional[str]) -> str:
        """Generate coverage note for the response."""
        if city:
            return f"Showing permits from {city} open data portal"
        elif state:
            cities = STATE_TO_CITIES.get(state.upper(), [])
            if cities:
                city_names = [OPEN_DATA_SOURCES[c]["name"] for c in cities]
                return f"Coverage in {state}: {', '.join(city_names)}"
            return f"No open data portals available for {state}. Showing major metro coverage."
        return "Showing permits from major U.S. metros with open data portals"

    def get_available_coverage(self) -> Dict[str, List[str]]:
        """Return available coverage by state."""
        coverage = {}
        for state, cities in STATE_TO_CITIES.items():
            coverage[state] = [OPEN_DATA_SOURCES[c]["name"] for c in cities]
        return coverage
