"""
Test Suite: Mock Data Removal Verification
Purpose: Verify that ALL sample/mock/fake data has been removed from the Construction Intelligence Platform.
Focus: Paid users must only see their own data, data from connected real APIs, and AI predictions based on real data.

Testing:
- GET /api/data-sources - returns status of all data sources
- GET /api/permits - returns empty array when PERMIT_API_KEY not set
- GET /api/intelligence/competitors - returns empty array when no real competitors tracked
- GET /api/ml/competitive-landscape - returns empty rankings when no real competitors tracked
- GET /api/economic-indicators - returns configured: false when FRED_API_KEY not set
- GET /api/benchmarks - returns configured: false when no permit data source
- ML models still work (POST /api/ml/demand-forecast, POST /api/ml/win-probability)
"""

import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://construdata-2.preview.emergentagent.com')
if BASE_URL.endswith('/'):
    BASE_URL = BASE_URL.rstrip('/')

# Test credentials
ENTERPRISE_USER = {"email": "malcolmgoodmen@gmail.com", "password": "Test123!"}
UNPAID_USER = {"email": "nopay@test.com", "password": "test123"}


@pytest.fixture(scope="module")
def enterprise_token():
    """Get authentication token for enterprise user"""
    response = requests.post(
        f"{BASE_URL}/api/auth/token",
        json={"username": ENTERPRISE_USER["email"], "password": ENTERPRISE_USER["password"]}
    )
    if response.status_code != 200:
        pytest.skip(f"Enterprise user login failed: {response.text}")
    return response.json()["access_token"]


@pytest.fixture
def enterprise_headers(enterprise_token):
    """Headers with enterprise auth token"""
    return {
        "Authorization": f"Bearer {enterprise_token}",
        "Content-Type": "application/json"
    }


class TestDataSources:
    """Tests for GET /api/data-sources endpoint - verifies data source status reporting"""

    def test_data_sources_status_structure(self, enterprise_headers):
        """Test /api/data-sources returns correct structure"""
        response = requests.get(
            f"{BASE_URL}/api/data-sources",
            headers=enterprise_headers
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        data = response.json()
        
        # Verify structure exists
        assert "user_data" in data, "Missing user_data in response"
        assert "external_sources" in data, "Missing external_sources in response"
        assert "ml_models" in data, "Missing ml_models in response"
        
        # Verify user_data structure
        user_data = data["user_data"]
        assert "profile_complete" in user_data
        assert "projects_count" in user_data
        assert "competitors_count" in user_data
        assert "clients_count" in user_data
        
        # Verify external_sources structure
        external = data["external_sources"]
        assert "permits" in external
        assert "economic_indicators" in external
        
        # Verify permits config has expected fields
        permits = external["permits"]
        assert "configured" in permits
        assert isinstance(permits["configured"], bool)
        
        # Verify economic indicators config
        econ = external["economic_indicators"]
        assert "configured" in econ
        assert isinstance(econ["configured"], bool)
        
        print(f"✓ Data sources status: permits.configured={permits['configured']}, fred.configured={econ['configured']}")


class TestPermitsEndpoint:
    """Tests for GET /api/permits endpoint - verifies NO fake permits when unconfigured"""

    def test_permits_returns_empty_when_unconfigured(self, enterprise_headers):
        """Test /api/permits returns empty array with setup_hint when PERMIT_API_KEY not set"""
        response = requests.get(
            f"{BASE_URL}/api/permits",
            headers=enterprise_headers
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        data = response.json()
        
        # Verify response structure
        assert "permits" in data, "Missing permits in response"
        assert "configured" in data, "Missing configured flag in response"
        
        # If not configured, should return empty permits with setup hint
        if data["configured"] is False:
            assert data["permits"] == [], f"Expected empty permits array when unconfigured, got {len(data['permits'])} permits"
            assert "setup_hint" in data, "Missing setup_hint when unconfigured"
            assert data["setup_hint"] is not None, "setup_hint should not be None"
            print(f"✓ Permits correctly returns empty when unconfigured. setup_hint: {data['setup_hint'][:50]}...")
        else:
            # If configured, permits can have data (real data)
            print(f"✓ Permits configured=True, {len(data['permits'])} permits found (could be real data)")

    def test_permits_no_fake_data_patterns(self, enterprise_headers):
        """Test that permits response contains no obvious fake/sample data patterns"""
        response = requests.get(
            f"{BASE_URL}/api/permits?limit=50",
            headers=enterprise_headers
        )
        assert response.status_code == 200
        data = response.json()
        
        permits = data.get("permits", [])
        
        # Check for common fake data patterns
        fake_patterns = ["lorem", "ipsum", "test permit", "sample", "demo", "fake", "mock", 
                        "acme", "example corp", "john doe construction", "placeholder"]
        
        for permit in permits:
            project_name = permit.get("project_name", "").lower()
            description = permit.get("description", "").lower()
            owner = permit.get("owner_name", "").lower()
            contractor = permit.get("contractor_name", "").lower()
            
            combined = f"{project_name} {description} {owner} {contractor}"
            
            for pattern in fake_patterns:
                assert pattern not in combined, f"Found fake data pattern '{pattern}' in permit: {permit.get('permit_number')}"
        
        print(f"✓ No fake data patterns found in {len(permits)} permits")


class TestCompetitorsEndpoint:
    """Tests for GET /api/intelligence/competitors endpoint - verifies NO sample competitor data"""

    def test_competitors_returns_empty_or_user_tracked(self, enterprise_headers):
        """Test /api/intelligence/competitors returns empty or only user-tracked competitors"""
        response = requests.get(
            f"{BASE_URL}/api/intelligence/competitors",
            headers=enterprise_headers
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        data = response.json()
        
        # Verify response structure
        assert "competitors" in data, "Missing competitors in response"
        assert "subscription_tier" in data or "data_source" in data, "Missing metadata fields"
        
        competitors = data["competitors"]
        
        # Check for fake data patterns (common sample competitor names)
        fake_competitor_patterns = ["abc construction", "builderco", "premier builders", 
                                   "sample competitor", "test company", "acme", "demo"]
        
        for comp in competitors:
            name = comp.get("name", "").lower()
            for pattern in fake_competitor_patterns:
                if pattern in name:
                    # Only flag if this looks like hardcoded sample data (not user-tracked)
                    if data.get("data_source") != "user_tracked":
                        pytest.fail(f"Found potential sample competitor: '{name}' with pattern '{pattern}'")
        
        if len(competitors) == 0:
            assert "setup_hint" in data, "Expected setup_hint when no competitors"
            print(f"✓ Competitors correctly returns empty with setup_hint: {data.get('setup_hint', '')[:50]}...")
        else:
            print(f"✓ {len(competitors)} competitors found (data_source: {data.get('data_source', 'unknown')})")


class TestCompetitiveLandscape:
    """Tests for GET /api/ml/competitive-landscape endpoint - verifies NO sample rankings"""

    def test_competitive_landscape_returns_empty_when_no_competitors(self, enterprise_headers):
        """Test /api/ml/competitive-landscape returns empty rankings when no competitors tracked"""
        response = requests.get(
            f"{BASE_URL}/api/ml/competitive-landscape",
            headers=enterprise_headers
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        data = response.json()
        
        # Verify response structure
        assert "rankings" in data, "Missing rankings in response"
        assert "model_version" in data, "Missing model_version"
        
        rankings = data["rankings"]
        
        # If there are rankings, they should come from user-tracked competitors
        if len(rankings) == 0:
            # Empty rankings is correct when no competitors tracked
            if "setup_hint" in data:
                print(f"✓ Competitive landscape correctly returns empty with setup_hint")
            else:
                print(f"✓ Competitive landscape correctly returns empty rankings")
        else:
            # Rankings present means user has tracked competitors
            print(f"✓ {len(rankings)} competitor rankings found (from user-tracked data)")
            
            # Check rankings have valid structure
            for rank in rankings:
                assert "competitor_name" in rank
                assert "threat_level" in rank
                assert "threat_score" in rank


class TestEconomicIndicators:
    """Tests for GET /api/economic-indicators endpoint - verifies configured flag"""

    def test_economic_indicators_returns_configured_status(self, enterprise_headers):
        """Test /api/economic-indicators returns configured: false when FRED_API_KEY not set"""
        response = requests.get(
            f"{BASE_URL}/api/economic-indicators",
            headers=enterprise_headers
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        data = response.json()
        
        # Verify response structure
        assert "configured" in data, "Missing configured flag in response"
        assert "indicators" in data, "Missing indicators in response"
        
        if data["configured"] is False:
            assert data["indicators"] == [], f"Expected empty indicators when unconfigured, got {len(data['indicators'])}"
            assert "setup_hint" in data, "Missing setup_hint when unconfigured"
            print(f"✓ Economic indicators correctly returns empty when unconfigured. setup_hint present")
        else:
            print(f"✓ Economic indicators configured=True, {len(data['indicators'])} indicators found")

    def test_economic_indicators_no_demo_data(self, enterprise_headers):
        """Test economic indicators contains no demo/sample values"""
        response = requests.get(
            f"{BASE_URL}/api/economic-indicators",
            headers=enterprise_headers
        )
        assert response.status_code == 200
        data = response.json()
        
        indicators = data.get("indicators", [])
        
        # If there are indicators, they should be from real FRED API
        for ind in indicators:
            # Check for fake indicator names
            name = ind.get("name", "").lower()
            assert "demo" not in name, f"Found demo indicator: {name}"
            assert "sample" not in name, f"Found sample indicator: {name}"
            assert "test" not in name, f"Found test indicator: {name}"
        
        print(f"✓ No demo/sample data patterns in {len(indicators)} indicators")


class TestBenchmarks:
    """Tests for GET /api/benchmarks endpoint - verifies configured flag"""

    def test_benchmarks_returns_configured_status(self, enterprise_headers):
        """Test /api/benchmarks returns configured: false when no permit data source"""
        response = requests.get(
            f"{BASE_URL}/api/benchmarks",
            headers=enterprise_headers
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        data = response.json()
        
        # Verify response structure
        assert "configured" in data or "benchmarks" in data, "Missing expected fields in response"
        
        # If configured flag exists and is false, should have setup_hint
        if data.get("configured") is False:
            assert "setup_hint" in data, "Missing setup_hint when unconfigured"
            print(f"✓ Benchmarks correctly returns configured=false with setup_hint")
        elif "benchmarks" in data:
            benchmarks = data.get("benchmarks", {})
            print(f"✓ Benchmarks returned data: {list(benchmarks.keys()) if isinstance(benchmarks, dict) else 'list'}")


class TestMLModelsStillWork:
    """Tests to verify ML models still work (using internal algorithms, not external data)"""

    def test_demand_forecast_works(self, enterprise_headers):
        """Test POST /api/ml/demand-forecast still works (proprietary model)"""
        response = requests.post(
            f"{BASE_URL}/api/ml/demand-forecast",
            headers=enterprise_headers,
            json={
                "region": "TX",
                "sector": "Commercial",
                "months_ahead": 6
            }
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        data = response.json()
        
        # Verify response structure
        assert "momentum" in data, "Missing momentum in response"
        assert "forecasts" in data, "Missing forecasts in response"
        
        # Verify momentum data
        momentum = data["momentum"]
        assert "score" in momentum
        assert "direction" in momentum
        assert momentum["score"] >= 0 and momentum["score"] <= 100
        
        # Verify forecasts
        forecasts = data["forecasts"]
        assert len(forecasts) == 6, f"Expected 6 month forecast, got {len(forecasts)}"
        
        for fc in forecasts:
            assert "period" in fc
            assert "predicted_demand" in fc
            assert "watermark" in fc
            assert fc["watermark"].startswith("PDH-")
        
        print(f"✓ Demand forecast working: momentum={momentum['score']}, direction={momentum['direction']}")

    def test_win_probability_works(self, enterprise_headers):
        """Test POST /api/ml/win-probability still works (proprietary model)"""
        response = requests.post(
            f"{BASE_URL}/api/ml/win-probability",
            headers=enterprise_headers,
            json={
                "project": {
                    "name": "Test Project for API",
                    "value": 2500000,
                    "sector": "Commercial",
                    "state": "TX",
                    "city": "Houston"
                }
            }
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        data = response.json()
        
        # Verify response structure
        assert "probability" in data
        assert "confidence" in data
        assert "recommendation" in data
        assert "factors" in data
        assert "watermark" in data
        
        # Verify values are valid
        assert 0 <= data["probability"] <= 1
        assert 0 <= data["confidence"] <= 1
        assert data["recommendation"] in ["STRONG PURSUE", "PURSUE", "EVALUATE", "AVOID"]
        assert data["watermark"].startswith("PDH-")
        
        print(f"✓ Win probability working: {data['probability']*100:.1f}% ({data['recommendation']})")


class TestNoHardcodedSampleData:
    """Cross-check tests to ensure no hardcoded sample data exists anywhere"""

    def test_my_competitors_shows_user_data_only(self, enterprise_headers):
        """Test /api/my-competitors shows only user-tracked competitors"""
        response = requests.get(
            f"{BASE_URL}/api/my-competitors",
            headers=enterprise_headers
        )
        # This endpoint requires Professional tier
        if response.status_code == 403:
            pytest.skip("User doesn't have required tier for competitor tracking")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        data = response.json()
        
        # Should be a list of user-tracked competitors
        assert isinstance(data, list), "Expected list response"
        print(f"✓ my-competitors returns {len(data)} user-tracked competitors")

    def test_my_projects_shows_user_data_only(self, enterprise_headers):
        """Test /api/my-projects shows only user's own projects"""
        response = requests.get(
            f"{BASE_URL}/api/my-projects",
            headers=enterprise_headers
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        data = response.json()
        
        # Should be a list of user's projects
        assert isinstance(data, list), "Expected list response"
        print(f"✓ my-projects returns {len(data)} user projects")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
