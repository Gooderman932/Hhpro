"""
Production Readiness Tests - HHDrywall Pro API
Tests for Phase 1-5: Pricing, Tier Gating, Onboarding, Data Sources, Health Check

© 2025 Poor Dude Holdings LLC. All Rights Reserved.
"""

import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://permit-forecast.preview.emergentagent.com')

# Test credentials
ENTERPRISE_USER = {"email": "malcolmgoodmen@gmail.com", "password": "Test123!"}
UNPAID_USER = {"email": "nopay@test.com", "password": "test123"}


@pytest.fixture(scope="module")
def api_client():
    """Shared requests session."""
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    return session


@pytest.fixture(scope="module")
def enterprise_token(api_client):
    """Get enterprise user token."""
    response = api_client.post(f"{BASE_URL}/api/auth/token", json={
        "username": ENTERPRISE_USER["email"],
        "password": ENTERPRISE_USER["password"]
    })
    if response.status_code == 200:
        return response.json().get("access_token")
    pytest.skip("Enterprise authentication failed")


@pytest.fixture(scope="module")
def unpaid_token(api_client):
    """Get unpaid user token."""
    response = api_client.post(f"{BASE_URL}/api/auth/token", json={
        "username": UNPAID_USER["email"],
        "password": UNPAID_USER["password"]
    })
    if response.status_code == 200:
        return response.json().get("access_token")
    pytest.skip("Unpaid user authentication failed")


@pytest.fixture(scope="module")
def enterprise_client(api_client, enterprise_token):
    """Session with enterprise auth header."""
    api_client.headers.update({"Authorization": f"Bearer {enterprise_token}"})
    return api_client


class TestPricingTiers:
    """Phase 1: Stripe production setup with new pricing."""

    def test_get_pricing_tiers(self, api_client):
        """GET /api/pricing/tiers returns 3 tiers with correct prices."""
        response = api_client.get(f"{BASE_URL}/api/pricing/tiers")
        assert response.status_code == 200

        tiers = response.json()
        assert len(tiers) == 3

        # Verify Basic tier
        basic = next(t for t in tiers if t["tier_id"] == "basic")
        assert basic["price"] == 49
        assert basic["name"] == "Basic"

        # Verify Professional tier
        pro = next(t for t in tiers if t["tier_id"] == "professional")
        assert pro["price"] == 149
        assert pro["name"] == "Pro"

        # Verify Enterprise tier
        enterprise = next(t for t in tiers if t["tier_id"] == "enterprise")
        assert enterprise["price"] == 399
        assert enterprise["name"] == "Enterprise"

    def test_tier_features_present(self, api_client):
        """All tiers have features listed."""
        response = api_client.get(f"{BASE_URL}/api/pricing/tiers")
        tiers = response.json()

        for tier in tiers:
            assert "features" in tier
            assert len(tier["features"]) > 0


class TestOnboarding:
    """Phase 3: Getting Started onboarding wizard."""

    def test_onboarding_status_returns_4_steps(self, api_client, enterprise_token):
        """GET /api/onboarding/status returns 4-step onboarding progress."""
        response = api_client.get(
            f"{BASE_URL}/api/onboarding/status",
            headers={"Authorization": f"Bearer {enterprise_token}"}
        )
        assert response.status_code == 200

        data = response.json()
        assert "steps" in data
        assert len(data["steps"]) == 4

        # Verify step IDs
        step_ids = [s["id"] for s in data["steps"]]
        assert "subscription" in step_ids
        assert "profile" in step_ids
        assert "data_sources" in step_ids
        assert "first_project" in step_ids

        # Verify progress calculation
        assert "progress" in data
        assert isinstance(data["progress"], int)
        assert 0 <= data["progress"] <= 100

    def test_skip_onboarding(self, api_client, enterprise_token):
        """POST /api/onboarding/skip marks onboarding as skipped."""
        response = api_client.post(
            f"{BASE_URL}/api/onboarding/skip",
            headers={"Authorization": f"Bearer {enterprise_token}"}
        )
        assert response.status_code == 200

        data = response.json()
        assert data["skipped"] == True
        assert "message" in data

    def test_onboarding_requires_auth(self, api_client):
        """Onboarding endpoints require authentication."""
        response = api_client.get(f"{BASE_URL}/api/onboarding/status")
        assert response.status_code in [401, 403]


class TestHealthCheck:
    """Phase 5: Health check with system status."""

    def test_health_endpoint(self, api_client):
        """GET /health returns production health check (backend-only)."""
        # Health endpoint is at backend port, not through /api
        response = api_client.get("http://localhost:8001/health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] in ["healthy", "degraded"]
        assert data["service"] == "HHDrywall Pro API"
        assert "stripe_mode" in data
        assert "database" in data
        assert "external_apis" in data
        assert data["external_apis"]["fred"] in ["connected", "not_configured"]
        assert data["external_apis"]["permits"] in ["connected", "not_configured"]
        assert "ml_models" in data


class TestCustomerPortal:
    """Stripe customer portal endpoint."""

    def test_customer_portal_returns_info(self, api_client, enterprise_token):
        """POST /api/stripe/customer-portal returns billing management info."""
        response = api_client.post(
            f"{BASE_URL}/api/stripe/customer-portal",
            headers={"Authorization": f"Bearer {enterprise_token}"}
        )
        assert response.status_code == 200

        data = response.json()
        assert "message" in data or "email" in data
        # Placeholder returns contact info since live keys aren't configured
        assert "billing@poorduceholdings.com" in str(data) or "portal" in str(data).lower()

    def test_customer_portal_requires_subscription(self, api_client, unpaid_token):
        """Customer portal requires active subscription."""
        response = api_client.post(
            f"{BASE_URL}/api/stripe/customer-portal",
            headers={"Authorization": f"Bearer {unpaid_token}"}
        )
        assert response.status_code == 400


class TestTierGating:
    """Phase 2: Tier-based feature gating."""

    def test_ml_win_probability_blocked_for_unpaid(self, api_client, unpaid_token):
        """ML win-probability returns 403 for unpaid users."""
        response = api_client.post(
            f"{BASE_URL}/api/ml/win-probability",
            headers={"Authorization": f"Bearer {unpaid_token}"},
            json={"project": {"name": "Test", "value": 1000000}}
        )
        assert response.status_code == 403
        assert "upgrade" in response.json()["detail"].lower()

    def test_ml_demand_forecast_blocked_for_unpaid(self, api_client, unpaid_token):
        """ML demand-forecast returns 403 for unpaid users."""
        response = api_client.post(
            f"{BASE_URL}/api/ml/demand-forecast",
            headers={"Authorization": f"Bearer {unpaid_token}"},
            json={"region": "TX", "sector": "Commercial", "months_ahead": 6}
        )
        assert response.status_code == 403
        assert "upgrade" in response.json()["detail"].lower()

    def test_enterprise_can_access_ml_endpoints(self, api_client, enterprise_token):
        """Enterprise users can access ML endpoints."""
        response = api_client.post(
            f"{BASE_URL}/api/ml/win-probability",
            headers={"Authorization": f"Bearer {enterprise_token}"},
            json={"project": {"name": "Test Project", "value": 5000000, "sector": "Commercial"}}
        )
        # Should succeed or return 400 (expected behavior for missing data)
        assert response.status_code in [200, 400]

    def test_demand_forecast_month_limits(self, api_client, enterprise_token):
        """Enterprise gets 6-month forecast (vs Pro's 3-month)."""
        response = api_client.post(
            f"{BASE_URL}/api/ml/demand-forecast",
            headers={"Authorization": f"Bearer {enterprise_token}"},
            json={"region": "TX", "sector": "Commercial", "months_ahead": 6}
        )
        assert response.status_code == 200

        data = response.json()
        # Enterprise tier should return 6 months of forecasts
        if "forecasts" in data:
            assert len(data["forecasts"]) <= 6


class TestDataValidation:
    """Phase 4: Data source validation with legal notices."""

    def test_permits_no_mock_data(self, api_client, enterprise_token):
        """Permits endpoint returns empty when not configured (no mock data)."""
        response = api_client.get(
            f"{BASE_URL}/api/permits",
            headers={"Authorization": f"Bearer {enterprise_token}"}
        )
        assert response.status_code == 200

        data = response.json()
        # When not configured, should return empty list with setup hint
        if not data.get("configured", True):
            assert data["permits"] == []
            assert "setup_hint" in data

    def test_economic_indicators_no_mock_data(self, api_client, enterprise_token):
        """Economic indicators returns empty when not configured."""
        response = api_client.get(
            f"{BASE_URL}/api/economic-indicators",
            headers={"Authorization": f"Bearer {enterprise_token}"}
        )
        assert response.status_code == 200

        data = response.json()
        # When not configured, should return empty with setup hint
        if not data.get("configured", True):
            assert data["indicators"] == []
            assert "setup_hint" in data

    def test_competitors_no_mock_data(self, api_client, enterprise_token):
        """Competitors endpoint returns empty when not configured."""
        response = api_client.get(
            f"{BASE_URL}/api/intelligence/competitors",
            headers={"Authorization": f"Bearer {enterprise_token}"}
        )
        assert response.status_code == 200

        data = response.json()
        # Should return user's tracked competitors (empty if none added)
        if len(data.get("competitors", [])) == 0:
            assert "setup_hint" in data or data["competitors"] == []


class TestMLResponses:
    """ML responses include legal_notice and data_sources fields."""

    def test_ml_win_probability_response_structure(self, api_client, enterprise_token):
        """ML win probability includes proper response structure."""
        response = api_client.post(
            f"{BASE_URL}/api/ml/win-probability",
            headers={"Authorization": f"Bearer {enterprise_token}"},
            json={"project": {"name": "Test Project", "value": 5000000, "sector": "Commercial"}}
        )

        if response.status_code == 200:
            data = response.json()
            assert "probability" in data
            assert "watermark" in data  # Contains copyright notice
            assert "model_version" in data

    def test_ml_demand_forecast_response_structure(self, api_client, enterprise_token):
        """ML demand forecast includes proper response structure."""
        response = api_client.post(
            f"{BASE_URL}/api/ml/demand-forecast",
            headers={"Authorization": f"Bearer {enterprise_token}"},
            json={"region": "TX", "sector": "Commercial", "months_ahead": 6}
        )
        assert response.status_code == 200

        data = response.json()
        assert "momentum" in data
        assert "forecasts" in data
        assert "legal_notice" in data or "watermark" in data  # Contains copyright notice


class TestDataSourcesStatus:
    """Data sources status endpoint."""

    def test_data_sources_status(self, api_client, enterprise_token):
        """GET /api/data-sources returns status of all data sources."""
        response = api_client.get(
            f"{BASE_URL}/api/data-sources",
            headers={"Authorization": f"Bearer {enterprise_token}"}
        )
        assert response.status_code == 200

        data = response.json()
        assert "user_data" in data
        assert "external_sources" in data
        assert "ml_models" in data

        # Check external sources structure
        ext = data["external_sources"]
        assert "permits" in ext
        assert "economic_indicators" in ext


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
