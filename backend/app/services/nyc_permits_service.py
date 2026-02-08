"""
NYC DOB Open Data Permits Service - Free, no API key required.
Uses NYC Department of Buildings Permit Issuance dataset (Socrata: ipu4-2q9a).
"""
import os
import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta


NYC_DOB_URL = "https://data.cityofnewyork.us/resource/ipu4-2q9a.json"

BOROUGH_MAP = {"MANHATTAN": "New York", "BROOKLYN": "Brooklyn", "QUEENS": "Queens",
               "BRONX": "Bronx", "STATEN ISLAND": "Staten Island"}


class NYCPermitsService:
    """Fetches recent construction permits from NYC DOB Open Data (free)."""

    def __init__(self):
        self.app_token = os.environ.get("SOCRATA_APP_TOKEN", "")

    async def get_recent_permits(
        self, limit: int = 100, days_back: int = 30
    ) -> List[Dict[str, Any]]:
        try:
            params = {
                "$limit": limit,
                "$order": "issuance_date DESC",
            }
            headers = {"Accept": "application/json"}
            if self.app_token:
                headers["X-App-Token"] = self.app_token

            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.get(NYC_DOB_URL, headers=headers, params=params)
                if resp.status_code == 200:
                    return [self._normalize(r) for r in resp.json()]
                print(f"NYC DOB returned {resp.status_code}")
                return []
        except Exception as e:
            print(f"NYC permits error: {e}")
            return []

    def _normalize(self, raw: Dict) -> Dict[str, Any]:
        borough = (raw.get("borough") or "").upper()
        cost_str = raw.get("estimated_job_cost__") or raw.get("initial_cost") or "0"
        try:
            cost = float(str(cost_str).replace(",", "").replace("$", ""))
        except (ValueError, TypeError):
            cost = None

        house = raw.get("house__", "")
        street = raw.get("street_name", "")
        addr = f"{house} {street}".strip()

        # Build a meaningful description from job_type
        jt = raw.get("job_type", "")
        job_desc = {"A1": "Major Alteration", "A2": "Minor Alteration", "A3": "Minor Alteration",
                    "NB": "New Building", "DM": "Demolition", "SG": "Sign"}.get(jt, jt)
        wt = raw.get("work_type", "")
        desc = f"{job_desc} - {wt}".strip(" -") if wt else job_desc

        return {
            "permit_id": raw.get("job__") or raw.get("permit_si_no") or "",
            "address": addr,
            "city": BOROUGH_MAP.get(borough, borough.title()),
            "state": "NY",
            "geo": {"lat": None, "lng": None},
            "work_type": desc or "General Construction",
            "estimated_cost": cost if cost and cost > 0 else None,
            "filing_date": raw.get("issuance_date") or raw.get("filing_date") or "",
            "status": raw.get("permit_status") or "issued",
            "contractor_name": raw.get("owner_s_first_name", ""),
            "contractor_license": raw.get("applicant_license__") or None,
            "description": f"{desc} at {addr}, {BOROUGH_MAP.get(borough, borough.title())}, NY",
            "source": "nyc_dob_open_data",
            "raw": raw,
        }
