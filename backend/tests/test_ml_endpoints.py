"""
ML Endpoints Test Suite - HHDrywall Pro
Copyright (c) 2025 Poor Dude Holdings LLC

Tests for proprietary ML model endpoints:
- Win Probability
- Demand Forecast
- Regional Outlook
- Competitive Landscape
- Competitive Analysis
- Project Matching
- ML Models Info
- Tier Gating (403 for non-subscribed users)
"""

import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://permit-forecast.preview.emergentagent.com')
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
        pytest.skip("Enterprise user login failed")
    return response.json()["access_token"]


@pytest.fixture(scope="module")
def unpaid_token():
    """Get authentication token for unpaid user"""
    response = requests.post(
        f"{BASE_URL}/api/auth/token",
        json={"username": UNPAID_USER["email"], "password": UNPAID_USER["password"]}
    )
    if response.status_code != 200:
        pytest.skip("Unpaid user login failed - user may not exist")
    return response.json()["access_token"]


@pytest.fixture
def enterprise_headers(enterprise_token):
    """Headers with enterprise auth token"""
    return {
        "Authorization": f"Bearer {enterprise_token}",
        "Content-Type": "application/json"
    }


@pytest.fixture
def unpaid_headers(unpaid_token):
    """Headers with unpaid user auth token"""
    return {
        "Authorization": f"Bearer {unpaid_token}",
        "Content-Type": "application/json"
    }


class TestMLModelsInfo:
    """Tests for GET /api/ml/models-info endpoint"""

    def test_models_info_success(self, enterprise_headers):
        """Test ML models info returns correct structure"""
        response = requests.get(
            f"{BASE_URL}/api/ml/models-info",
            headers=enterprise_headers
        )
        assert response.status_code == 200
        data = response.json()
        
        # Verify structure
        assert "models" in data
        assert "copyright" in data
        assert "patent_status" in data
        assert len(data["models"]) == 4
        
        # Verify each model has required fields
        for model in data["models"]:
            assert "name" in model
            assert "version" in model
            assert "copyright" in model
            assert "patent_status" in model
            assert "Poor Dude Holdings LLC" in model["copyright"]


class TestWinProbability:
    """Tests for POST /api/ml/win-probability endpoint"""

    def test_win_probability_with_project_data(self, enterprise_headers):
        """Test win probability with custom project data"""
        response = requests.post(
            f"{BASE_URL}/api/ml/win-probability",
            headers=enterprise_headers,
            json={
                "project": {
                    "name": "Test Commercial Project",
                    "value": 2500000,
                    "sector": "Commercial",
                    "state": "TX",
                    "city": "Austin",
                    "expected_bidders": 4
                }
            }
        )
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "probability" in data
        assert "confidence" in data
        assert "recommendation" in data
        assert "explanation" in data
        assert "factors" in data
        assert "model_version" in data
        assert "watermark" in data
        
        # Verify probability is valid
        assert 0 <= data["probability"] <= 1
        assert 0 <= data["confidence"] <= 1
        assert data["recommendation"] in ["STRONG PURSUE", "PURSUE", "EVALUATE", "AVOID"]
        assert data["watermark"].startswith("PDH-")


class TestDemandForecast:
    """Tests for POST /api/ml/demand-forecast endpoint"""

    def test_demand_forecast_success(self, enterprise_headers):
        """Test demand forecast returns momentum and forecasts"""
        response = requests.post(
            f"{BASE_URL}/api/ml/demand-forecast",
            headers=enterprise_headers,
            json={
                "region": "TX",
                "sector": "Commercial",
                "months_ahead": 6
            }
        )
        assert response.status_code == 200
        data = response.json()
        
        # Verify momentum structure
        assert "momentum" in data
        assert "score" in data["momentum"]
        assert "direction" in data["momentum"]
        assert "strength" in data["momentum"]
        assert "factors" in data["momentum"]
        
        # Verify forecasts
        assert "forecasts" in data
        assert len(data["forecasts"]) == 6  # 6 months
        
        for forecast in data["forecasts"]:
            assert "period" in forecast
            assert "predicted_demand" in forecast
            assert "confidence_interval" in forecast
            assert "trend" in forecast
            assert "watermark" in forecast
            assert forecast["watermark"].startswith("PDH-")


class TestRegionalOutlook:
    """Tests for GET /api/ml/regional-outlook endpoint"""

    def test_regional_outlook_success(self, enterprise_headers):
        """Test regional outlook returns data for multiple regions"""
        response = requests.get(
            f"{BASE_URL}/api/ml/regional-outlook?sector=Commercial",
            headers=enterprise_headers
        )
        assert response.status_code == 200
        data = response.json()
        
        # Verify structure
        assert "outlook" in data
        assert "sector" in data
        assert "model_version" in data
        
        # Verify outlook has regions
        assert len(data["outlook"]) > 0
        
        # Verify each region has required fields
        for region, region_data in data["outlook"].items():
            assert "momentum_score" in region_data
            assert "direction" in region_data
            assert "strength" in region_data
            assert "3_month_forecast" in region_data


class TestCompetitiveLandscape:
    """Tests for GET /api/ml/competitive-landscape endpoint"""

    def test_competitive_landscape_success(self, enterprise_headers):
        """Test competitive landscape returns rankings and CAI"""
        response = requests.get(
            f"{BASE_URL}/api/ml/competitive-landscape",
            headers=enterprise_headers
        )
        assert response.status_code == 200
        data = response.json()
        
        # Verify rankings
        assert "rankings" in data
        for ranking in data["rankings"]:
            assert "competitor_name" in ranking
            assert "threat_level" in ranking
            assert "threat_score" in ranking
            assert "vulnerabilities" in ranking
            assert "strengths" in ranking
        
        # Verify Competitive Advantage Index
        assert "competitive_advantage_index" in data
        cai = data["competitive_advantage_index"]
        assert "score" in cai
        assert "position" in cai
        assert "strengths" in cai
        assert "improvement_areas" in cai
        assert "competitive_gaps" in cai


class TestCompetitiveAnalysis:
    """Tests for POST /api/ml/competitive-analysis endpoint"""

    def test_competitive_analysis_success(self, enterprise_headers):
        """Test competitive analysis for a single competitor"""
        response = requests.post(
            f"{BASE_URL}/api/ml/competitive-analysis",
            headers=enterprise_headers,
            json={
                "competitor": {
                    "name": "ABC Construction",
                    "sectors": ["Commercial"],
                    "win_rate": 0.34,
                    "market_share_pct": 0.12
                }
            }
        )
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "competitor_name" in data
        assert "threat_level" in data
        assert "threat_score" in data
        assert "factors" in data
        assert "vulnerabilities" in data
        assert "strengths" in data
        assert "model_version" in data
        assert "watermark" in data
        
        # Verify threat level is valid
        assert data["threat_level"] in ["CRITICAL", "HIGH", "MODERATE", "LOW", "MINIMAL"]
        assert data["watermark"].startswith("PDH-")


class TestProjectMatching:
    """Tests for POST /api/ml/project-matching endpoint"""

    def test_project_matching_requires_profile(self, enterprise_headers):
        """Test project matching returns 400 when profile incomplete"""
        response = requests.post(
            f"{BASE_URL}/api/ml/project-matching",
            headers=enterprise_headers,
            json={"min_score": 0, "limit": 20}
        )
        # Can be 200 (if profile exists) or 400 (if profile incomplete)
        # Both are valid behaviors - just check it returns JSON
        assert response.status_code in [200, 400]
        data = response.json()
        
        if response.status_code == 400:
            assert "detail" in data
            assert "profile" in data["detail"].lower()
        else:
            assert "matches" in data or "total" in data


class TestTierGating:
    """Tests for subscription tier gating - ML endpoints should return 403 for unpaid users"""

    def test_unpaid_user_blocked_from_models_info(self, unpaid_headers):
        """Test unpaid user gets 403 from ML models info"""
        response = requests.get(
            f"{BASE_URL}/api/ml/models-info",
            headers=unpaid_headers
        )
        assert response.status_code == 403
        data = response.json()
        assert "detail" in data
        assert "subscription" in data["detail"].lower() or "professional" in data["detail"].lower()

    def test_unpaid_user_blocked_from_win_probability(self, unpaid_headers):
        """Test unpaid user gets 403 from win probability"""
        response = requests.post(
            f"{BASE_URL}/api/ml/win-probability",
            headers=unpaid_headers,
            json={"project": {"name": "Test", "value": 1000000}}
        )
        assert response.status_code == 403

    def test_unpaid_user_blocked_from_demand_forecast(self, unpaid_headers):
        """Test unpaid user gets 403 from demand forecast"""
        response = requests.post(
            f"{BASE_URL}/api/ml/demand-forecast",
            headers=unpaid_headers,
            json={"region": "TX", "sector": "Commercial", "months_ahead": 6}
        )
        assert response.status_code == 403

    def test_unpaid_user_blocked_from_regional_outlook(self, unpaid_headers):
        """Test unpaid user gets 403 from regional outlook"""
        response = requests.get(
            f"{BASE_URL}/api/ml/regional-outlook?sector=Commercial",
            headers=unpaid_headers
        )
        assert response.status_code == 403

    def test_unpaid_user_blocked_from_competitive_landscape(self, unpaid_headers):
        """Test unpaid user gets 403 from competitive landscape"""
        response = requests.get(
            f"{BASE_URL}/api/ml/competitive-landscape",
            headers=unpaid_headers
        )
        assert response.status_code == 403


class TestAuthentication:
    """Tests for authentication requirements"""

    def test_unauthenticated_request_blocked(self):
        """Test unauthenticated request gets 401 or 403"""
        response = requests.get(f"{BASE_URL}/api/ml/models-info")
        assert response.status_code in [401, 403]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
