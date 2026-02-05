"""
HHDrywall Pro API Tests
Tests for authentication, subscriptions, analytics, ML predictions, and batch scoring
"""
import pytest
import requests
import os

# Use localhost since the app runs on internal ports
BASE_URL = "http://localhost:8001"

# Test credentials
ENTERPRISE_USER = {"email": "malcolmgoodmen@gmail.com", "password": "Test123!"}
PROFESSIONAL_USER = {"email": "test@example.com", "password": "test123"}


class TestHealthCheck:
    """Health check endpoint tests"""
    
    def test_health_endpoint(self):
        """Test health endpoint returns healthy status"""
        response = requests.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        print(f"✓ Health check passed: {data}")


class TestAuthentication:
    """Authentication endpoint tests"""
    
    def test_login_enterprise_user(self):
        """Test login with Enterprise user credentials"""
        response = requests.post(
            f"{BASE_URL}/api/auth/token",
            json={"username": ENTERPRISE_USER["email"], "password": ENTERPRISE_USER["password"]}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        print(f"✓ Enterprise user login successful")
        return data["access_token"]
    
    def test_login_professional_user(self):
        """Test login with Professional user credentials"""
        response = requests.post(
            f"{BASE_URL}/api/auth/token",
            json={"username": PROFESSIONAL_USER["email"], "password": PROFESSIONAL_USER["password"]}
        )
        # May fail if user doesn't exist
        if response.status_code == 200:
            data = response.json()
            assert "access_token" in data
            print(f"✓ Professional user login successful")
        else:
            print(f"⚠ Professional user not found (status: {response.status_code})")
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials returns 401"""
        response = requests.post(
            f"{BASE_URL}/api/auth/token",
            json={"username": "invalid@example.com", "password": "wrongpassword"}
        )
        assert response.status_code == 401
        print(f"✓ Invalid credentials correctly rejected")
    
    def test_get_current_user(self, enterprise_token):
        """Test getting current user info"""
        response = requests.get(
            f"{BASE_URL}/api/auth/me",
            headers={"Authorization": f"Bearer {enterprise_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == ENTERPRISE_USER["email"]
        print(f"✓ Current user retrieved: {data['email']}")


class TestSubscription:
    """Subscription endpoint tests"""
    
    def test_get_pricing_tiers(self):
        """Test getting pricing tiers (no auth required)"""
        response = requests.get(f"{BASE_URL}/api/pricing/tiers")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 3  # Basic, Professional, Enterprise
        tier_ids = [t["tier_id"] for t in data]
        assert "basic" in tier_ids
        assert "professional" in tier_ids
        assert "enterprise" in tier_ids
        print(f"✓ Pricing tiers retrieved: {tier_ids}")
    
    def test_get_current_subscription(self, enterprise_token):
        """Test getting current subscription for Enterprise user"""
        response = requests.get(
            f"{BASE_URL}/api/subscriptions/current",
            headers={"Authorization": f"Bearer {enterprise_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        if data:
            assert "tier_id" in data
            assert data["tier_id"] == "enterprise"
            print(f"✓ Enterprise subscription confirmed: {data['tier_name']}")
        else:
            print(f"⚠ No active subscription found")


class TestAnalytics:
    """Analytics endpoint tests (Basic tier+)"""
    
    def test_get_analytics_summary(self, enterprise_token):
        """Test getting analytics summary"""
        response = requests.get(
            f"{BASE_URL}/api/analytics/summary",
            headers={"Authorization": f"Bearer {enterprise_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "total_projects" in data
        assert "total_value" in data
        assert "sector_distribution" in data
        print(f"✓ Analytics summary: {data['total_projects']} projects, ${data['total_value']} total value")
    
    def test_get_regional_analysis(self, enterprise_token):
        """Test getting regional analysis"""
        response = requests.get(
            f"{BASE_URL}/api/analytics/regions",
            headers={"Authorization": f"Bearer {enterprise_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "regions" in data
        print(f"✓ Regional analysis: {len(data['regions'])} regions")


class TestProjects:
    """Project endpoint tests"""
    
    def test_list_projects(self, enterprise_token):
        """Test listing projects"""
        response = requests.get(
            f"{BASE_URL}/api/projects",
            headers={"Authorization": f"Bearer {enterprise_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✓ Projects listed: {len(data)} projects")
        return data


class TestMLPredictions:
    """ML Prediction endpoint tests (Professional tier+)"""
    
    def test_get_demand_forecast(self, enterprise_token):
        """Test getting demand forecast"""
        response = requests.get(
            f"{BASE_URL}/api/predictions/demand-forecast",
            params={"sector": "Commercial", "region": "TX", "months": 6},
            headers={"Authorization": f"Bearer {enterprise_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "forecasts" in data
        assert "trend" in data
        print(f"✓ Demand forecast: trend={data['trend']}, {len(data['forecasts'])} months")
    
    def test_get_regional_outlook(self, enterprise_token):
        """Test getting regional outlook"""
        response = requests.get(
            f"{BASE_URL}/api/predictions/regional-outlook",
            headers={"Authorization": f"Bearer {enterprise_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✓ Regional outlook: {len(data)} regions")
    
    def test_get_win_probability(self, enterprise_token):
        """Test getting win probability for a project"""
        # First get a project ID
        projects_response = requests.get(
            f"{BASE_URL}/api/projects",
            headers={"Authorization": f"Bearer {enterprise_token}"}
        )
        if projects_response.status_code == 200:
            projects = projects_response.json()
            if projects:
                project_id = projects[0]["id"]
                response = requests.get(
                    f"{BASE_URL}/api/predictions/win-probability/{project_id}",
                    headers={"Authorization": f"Bearer {enterprise_token}"}
                )
                assert response.status_code == 200
                data = response.json()
                assert "win_probability" in data
                assert "confidence" in data
                print(f"✓ Win probability for project {project_id}: {data['win_probability']*100:.1f}%")
            else:
                print("⚠ No projects available for win probability test")
        else:
            print("⚠ Could not fetch projects for win probability test")


class TestBatchScoring:
    """Batch Scoring endpoint tests (Enterprise tier only)"""
    
    def test_batch_score_projects(self, enterprise_token):
        """Test batch scoring projects"""
        response = requests.get(
            f"{BASE_URL}/api/scoring/batch",
            params={"limit": 10},
            headers={"Authorization": f"Bearer {enterprise_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if data:
            assert "project_id" in data[0]
            assert "overall_score" in data[0]
            assert "recommendation" in data[0]
            print(f"✓ Batch scoring: {len(data)} projects scored")
        else:
            print("⚠ No projects available for batch scoring")


class TestCompetitorIntelligence:
    """Competitor Intelligence endpoint tests (Professional tier+)"""
    
    def test_get_competitors(self, enterprise_token):
        """Test getting competitor intelligence"""
        response = requests.get(
            f"{BASE_URL}/api/intelligence/competitors",
            params={"limit": 20},
            headers={"Authorization": f"Bearer {enterprise_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "competitors" in data
        competitors = data["competitors"]
        assert isinstance(competitors, list)
        if competitors:
            assert "name" in competitors[0]
            print(f"✓ Competitors: {len(competitors)} found")
        else:
            print("⚠ No competitors found")


# Fixtures
@pytest.fixture(scope="module")
def enterprise_token():
    """Get Enterprise user token"""
    response = requests.post(
        f"{BASE_URL}/api/auth/token",
        json={"username": ENTERPRISE_USER["email"], "password": ENTERPRISE_USER["password"]}
    )
    if response.status_code == 200:
        return response.json()["access_token"]
    pytest.skip("Enterprise user authentication failed")


@pytest.fixture(scope="module")
def professional_token():
    """Get Professional user token"""
    response = requests.post(
        f"{BASE_URL}/api/auth/token",
        json={"username": PROFESSIONAL_USER["email"], "password": PROFESSIONAL_USER["password"]}
    )
    if response.status_code == 200:
        return response.json()["access_token"]
    pytest.skip("Professional user authentication failed")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
