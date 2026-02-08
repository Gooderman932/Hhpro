"""
Commercial Permit Data Service - Pluggable provider (Shovels.ai / BatchData)
"""
import os
import httpx
from typing import List, Dict, Any, Optional


class CommercialPermitsService:
    """Fetches permits from paid commercial APIs (Shovels.ai or BatchData)."""

    PROVIDERS = {
        "shovels": {
            "base_url": "https://api.shovels.ai/v2",
            "search": "/permits/search",
        },
        "batchdata": {
            "base_url": "https://api.batchdata.com/api/v1",
            "search": "/permits/search",
        },
    }

    def __init__(self):
        self.api_key = os.environ.get("PERMIT_API_KEY", "")
        self.provider = os.environ.get("PERMIT_API_PROVIDER", "shovels").lower()
        self.configured = bool(self.api_key)
        self.config = self.PROVIDERS.get(self.provider, self.PROVIDERS["shovels"])

    async def search(
        self,
        location: Optional[str] = None,
        state: Optional[str] = None,
        limit: int = 25,
    ) -> List[Dict[str, Any]]:
        if not self.configured:
            return []

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                headers = {"Authorization": f"Bearer {self.api_key}", "Accept": "application/json"}

                if self.provider == "shovels":
                    params: Dict[str, Any] = {"limit": limit}
                    if location:
                        params["location"] = location
                    if state:
                        params["state"] = state
                    resp = await client.get(
                        f"{self.config['base_url']}{self.config['search']}",
                        headers=headers, params=params,
                    )
                elif self.provider == "batchdata":
                    params = {"limit": limit}
                    if location:
                        params["address"] = location
                    if state:
                        params["state"] = state
                    headers["X-Api-Key"] = self.api_key
                    resp = await client.get(
                        f"{self.config['base_url']}{self.config['search']}",
                        headers=headers, params=params,
                    )
                else:
                    return []

                if resp.status_code == 200:
                    data = resp.json()
                    raw_permits = data.get("results") or data.get("permits") or data.get("data") or []
                    return [self._normalize(p) for p in raw_permits[:limit]]
                else:
                    print(f"Permit API {self.provider} returned {resp.status_code}")
                    return []
        except Exception as e:
            print(f"Permit API error ({self.provider}): {e}")
            return []

    def _normalize(self, raw: Dict) -> Dict[str, Any]:
        """Map any provider's raw format into our standard schema."""
        return {
            "permit_id": str(raw.get("id") or raw.get("permit_id") or raw.get("permit_number", "")),
            "address": raw.get("address") or raw.get("site_address") or "",
            "city": raw.get("city") or raw.get("jurisdiction") or "",
            "state": raw.get("state") or "",
            "geo": {
                "lat": raw.get("latitude") or raw.get("lat"),
                "lng": raw.get("longitude") or raw.get("lng") or raw.get("lon"),
            },
            "work_type": raw.get("work_type") or raw.get("permit_type") or raw.get("type") or "General",
            "estimated_cost": _to_float(raw.get("estimated_cost") or raw.get("job_value") or raw.get("valuation")),
            "filing_date": raw.get("filing_date") or raw.get("issue_date") or raw.get("date") or "",
            "status": raw.get("status") or raw.get("permit_status") or "issued",
            "contractor_name": raw.get("contractor_name") or raw.get("contractor") or None,
            "contractor_license": raw.get("contractor_license") or raw.get("license_number") or None,
            "description": raw.get("description") or raw.get("work_description") or raw.get("job_description") or "",
            "source": self.provider,
            "raw": raw,
        }


def _to_float(val) -> Optional[float]:
    if val is None:
        return None
    try:
        return float(str(val).replace(",", "").replace("$", ""))
    except (ValueError, TypeError):
        return None
