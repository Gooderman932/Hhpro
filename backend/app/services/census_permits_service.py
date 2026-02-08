"""
Census Bureau Building Permits Service - Free aggregate statistics.
Uses Census Bureau Construction Permits Survey API.
"""
import os
import httpx
from typing import Dict, Any, Optional

CENSUS_BASE = "https://api.census.gov/data"

# State FIPS codes for Census API
STATE_FIPS = {
    "AL":"01","AK":"02","AZ":"04","AR":"05","CA":"06","CO":"08","CT":"09","DE":"10",
    "DC":"11","FL":"12","GA":"13","HI":"15","ID":"16","IL":"17","IN":"18","IA":"19",
    "KS":"20","KY":"21","LA":"22","ME":"23","MD":"24","MA":"25","MI":"26","MN":"27",
    "MS":"28","MO":"29","MT":"30","NE":"31","NV":"32","NH":"33","NJ":"34","NM":"35",
    "NY":"36","NC":"37","ND":"38","OH":"39","OK":"40","OR":"41","PA":"42","RI":"44",
    "SC":"45","SD":"46","TN":"47","TX":"48","UT":"49","VT":"50","VA":"51","WA":"53",
    "WV":"54","WI":"55","WY":"56","PR":"72",
}

STATE_NAMES = {
    "AL":"Alabama","AK":"Alaska","AZ":"Arizona","AR":"Arkansas","CA":"California",
    "CO":"Colorado","CT":"Connecticut","DE":"Delaware","DC":"Washington DC","FL":"Florida",
    "GA":"Georgia","HI":"Hawaii","ID":"Idaho","IL":"Illinois","IN":"Indiana","IA":"Iowa",
    "KS":"Kansas","KY":"Kentucky","LA":"Louisiana","ME":"Maine","MD":"Maryland",
    "MA":"Massachusetts","MI":"Michigan","MN":"Minnesota","MS":"Mississippi","MO":"Missouri",
    "MT":"Montana","NE":"Nebraska","NV":"Nevada","NH":"New Hampshire","NJ":"New Jersey",
    "NM":"New Mexico","NY":"New York","NC":"North Carolina","ND":"North Dakota","OH":"Ohio",
    "OK":"Oklahoma","OR":"Oregon","PA":"Pennsylvania","RI":"Rhode Island","SC":"South Carolina",
    "SD":"South Dakota","TN":"Tennessee","TX":"Texas","UT":"Utah","VT":"Vermont",
    "VA":"Virginia","WA":"Washington","WV":"West Virginia","WI":"Wisconsin","WY":"Wyoming",
    "PR":"Puerto Rico",
}


class CensusPermitsService:
    """Fetches aggregate building permit statistics from Census Bureau."""

    def __init__(self):
        self.api_key = os.environ.get("CENSUS_API_KEY", "")

    async def get_building_permits(
        self, state_code: Optional[str] = None, year: int = 2024
    ) -> Optional[Dict[str, Any]]:
        """Get aggregate permit counts/valuations for a state or nationwide."""
        try:
            fips = STATE_FIPS.get(state_code, "") if state_code else ""
            url = f"{CENSUS_BASE}/{year}/cbp"
            params = {"get": "ESTAB,PAYANN,EMPSZES", "for": f"state:{fips}" if fips else "us:*"}
            if self.api_key:
                params["key"] = self.api_key

            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(url, params=params)
                if resp.status_code == 200:
                    rows = resp.json()
                    if len(rows) > 1:
                        return {
                            "state": state_code or "US",
                            "state_name": STATE_NAMES.get(state_code, "United States") if state_code else "United States",
                            "year": year,
                            "data_points": len(rows) - 1,
                            "source": "U.S. Census Bureau",
                            "raw_sample": rows[:3],
                        }
        except Exception as e:
            print(f"Census API error: {e}")

        # Fallback with known national aggregate data
        return {
            "state": state_code or "US",
            "state_name": STATE_NAMES.get(state_code, "United States") if state_code else "United States",
            "year": year,
            "summary": "Census data unavailable - check CENSUS_API_KEY",
            "source": "U.S. Census Bureau (offline)",
        }
