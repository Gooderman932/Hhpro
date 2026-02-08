"""
Test Admin Revenue Dashboard Endpoints
Tests for:
- GET /api/admin/revenue - Admin-only revenue metrics
- GET /api/admin/revenue/export - CSV export for admin
- Access control (403 for non-admin)
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')
if not BASE_URL:
    BASE_URL = "https://construdata-2.preview.emergentagent.com"

# Test credentials from the review request
ADMIN_USER = {"email": "malcolmgoodmen@gmail.com", "password": "Test123!"}
NON_ADMIN_USER = {"email": "nopay@test.com", "password": "test123"}


class TestAdminAuthentication:
    """Test admin authentication and access control"""
    
    def test_admin_login_success(self):
        """Admin user can login successfully"""
        response = requests.post(f"{BASE_URL}/api/auth/token", json={
            "username": ADMIN_USER["email"],
            "password": ADMIN_USER["password"]
        })
        assert response.status_code == 200, f"Login failed: {response.text}"
        data = response.json()
        assert "access_token" in data, "Missing access_token in response"
        assert data.get("token_type") == "bearer"
        print(f"PASS: Admin login successful")
        
    def test_non_admin_login_success(self):
        """Non-admin user can login successfully"""
        response = requests.post(f"{BASE_URL}/api/auth/token", json={
            "username": NON_ADMIN_USER["email"],
            "password": NON_ADMIN_USER["password"]
        })
        assert response.status_code == 200, f"Login failed: {response.text}"
        data = response.json()
        assert "access_token" in data
        print(f"PASS: Non-admin login successful")


class TestAdminRevenueEndpoint:
    """Test GET /api/admin/revenue endpoint"""
    
    @pytest.fixture
    def admin_token(self):
        """Get admin user token"""
        response = requests.post(f"{BASE_URL}/api/auth/token", json={
            "username": ADMIN_USER["email"],
            "password": ADMIN_USER["password"]
        })
        if response.status_code != 200:
            pytest.skip("Admin login failed")
        return response.json()["access_token"]
    
    @pytest.fixture
    def non_admin_token(self):
        """Get non-admin user token"""
        response = requests.post(f"{BASE_URL}/api/auth/token", json={
            "username": NON_ADMIN_USER["email"],
            "password": NON_ADMIN_USER["password"]
        })
        if response.status_code != 200:
            pytest.skip("Non-admin login failed")
        return response.json()["access_token"]
    
    def test_admin_revenue_returns_200_for_admin(self, admin_token):
        """Admin user gets 200 with revenue data"""
        response = requests.get(
            f"{BASE_URL}/api/admin/revenue?days=90",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        data = response.json()
        
        # Verify response structure
        assert "summary" in data, "Missing 'summary' in response"
        assert "tier_breakdown" in data, "Missing 'tier_breakdown' in response"
        assert "ltv_by_tier" in data, "Missing 'ltv_by_tier' in response"
        assert "revenue_trend" in data, "Missing 'revenue_trend' in response"
        assert "recent_transactions" in data, "Missing 'recent_transactions' in response"
        assert "recent_signups" in data, "Missing 'recent_signups' in response"
        assert "alerts" in data, "Missing 'alerts' in response"
        assert "period_days" in data, "Missing 'period_days' in response"
        
        print(f"PASS: Admin revenue endpoint returns full data structure")
    
    def test_admin_revenue_returns_403_for_non_admin(self, non_admin_token):
        """Non-admin user gets 403 Access Denied"""
        response = requests.get(
            f"{BASE_URL}/api/admin/revenue",
            headers={"Authorization": f"Bearer {non_admin_token}"}
        )
        assert response.status_code == 403, f"Expected 403, got {response.status_code}: {response.text}"
        data = response.json()
        assert "detail" in data
        assert "admin" in data["detail"].lower() or "access" in data["detail"].lower()
        print(f"PASS: Non-admin gets 403 with message: {data['detail']}")
    
    def test_admin_revenue_returns_401_without_auth(self):
        """Request without auth gets 401"""
        response = requests.get(f"{BASE_URL}/api/admin/revenue")
        assert response.status_code in [401, 403], f"Expected 401 or 403, got {response.status_code}"
        print(f"PASS: Unauthenticated request returns {response.status_code}")
    
    def test_admin_revenue_summary_fields(self, admin_token):
        """Verify all summary fields are present and correct types"""
        response = requests.get(
            f"{BASE_URL}/api/admin/revenue?days=90",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        summary = response.json()["summary"]
        
        # Check all required summary fields
        required_fields = [
            "mrr", "arr", "total_active_subscribers", "arpu",
            "churn_rate_pct", "conversion_rate_pct", "total_users",
            "growth_rate_pct", "top_tier_by_revenue"
        ]
        for field in required_fields:
            assert field in summary, f"Missing field '{field}' in summary"
        
        # Check types
        assert isinstance(summary["mrr"], (int, float)), "mrr should be numeric"
        assert isinstance(summary["arr"], (int, float)), "arr should be numeric"
        assert isinstance(summary["total_active_subscribers"], int), "total_active_subscribers should be int"
        assert isinstance(summary["arpu"], (int, float)), "arpu should be numeric"
        assert isinstance(summary["churn_rate_pct"], (int, float)), "churn_rate_pct should be numeric"
        assert isinstance(summary["conversion_rate_pct"], (int, float)), "conversion_rate_pct should be numeric"
        assert isinstance(summary["total_users"], int), "total_users should be int"
        assert isinstance(summary["growth_rate_pct"], (int, float)), "growth_rate_pct should be numeric"
        assert isinstance(summary["top_tier_by_revenue"], str), "top_tier_by_revenue should be string"
        
        print(f"PASS: All summary fields present with correct types")
        print(f"  MRR: ${summary['mrr']}, ARR: ${summary['arr']}")
        print(f"  Active subscribers: {summary['total_active_subscribers']}")
        print(f"  ARPU: ${summary['arpu']}, Churn: {summary['churn_rate_pct']}%")
    
    def test_admin_revenue_tier_breakdown(self, admin_token):
        """Verify tier breakdown has counts and revenue for each tier"""
        response = requests.get(
            f"{BASE_URL}/api/admin/revenue",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        tier_breakdown = response.json()["tier_breakdown"]
        
        assert "counts" in tier_breakdown, "Missing 'counts' in tier_breakdown"
        assert "revenue" in tier_breakdown, "Missing 'revenue' in tier_breakdown"
        
        # Check tiers exist in counts
        for tier in ["basic", "professional", "enterprise"]:
            assert tier in tier_breakdown["counts"], f"Missing '{tier}' in counts"
            assert tier in tier_breakdown["revenue"], f"Missing '{tier}' in revenue"
            assert isinstance(tier_breakdown["counts"][tier], int), f"{tier} count should be int"
            assert isinstance(tier_breakdown["revenue"][tier], (int, float)), f"{tier} revenue should be numeric"
        
        print(f"PASS: Tier breakdown structure correct")
        print(f"  Counts: {tier_breakdown['counts']}")
        print(f"  Revenue: {tier_breakdown['revenue']}")
    
    def test_admin_revenue_ltv_by_tier(self, admin_token):
        """Verify LTV calculations exist for each tier"""
        response = requests.get(
            f"{BASE_URL}/api/admin/revenue",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        ltv_by_tier = response.json()["ltv_by_tier"]
        
        for tier in ["basic", "professional", "enterprise"]:
            assert tier in ltv_by_tier, f"Missing LTV for '{tier}'"
            assert isinstance(ltv_by_tier[tier], (int, float)), f"LTV for {tier} should be numeric"
            assert ltv_by_tier[tier] >= 0, f"LTV for {tier} should be non-negative"
        
        print(f"PASS: LTV by tier: {ltv_by_tier}")
    
    def test_admin_revenue_trend(self, admin_token):
        """Verify revenue trend is an array with date/revenue pairs"""
        response = requests.get(
            f"{BASE_URL}/api/admin/revenue?days=30",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        revenue_trend = response.json()["revenue_trend"]
        
        assert isinstance(revenue_trend, list), "revenue_trend should be list"
        assert len(revenue_trend) == 30, f"Expected 30 days of data, got {len(revenue_trend)}"
        
        # Check structure of first entry
        if revenue_trend:
            entry = revenue_trend[0]
            assert "date" in entry, "Missing 'date' in trend entry"
            assert "revenue" in entry, "Missing 'revenue' in trend entry"
        
        print(f"PASS: Revenue trend has {len(revenue_trend)} data points")
    
    def test_admin_revenue_recent_transactions(self, admin_token):
        """Verify recent transactions structure"""
        response = requests.get(
            f"{BASE_URL}/api/admin/revenue",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        transactions = response.json()["recent_transactions"]
        
        assert isinstance(transactions, list), "recent_transactions should be list"
        
        if transactions:
            tx = transactions[0]
            required_fields = ["id", "email", "tier", "amount", "status", "date"]
            for field in required_fields:
                assert field in tx, f"Missing '{field}' in transaction"
        
        print(f"PASS: Recent transactions: {len(transactions)} items")
    
    def test_admin_revenue_recent_signups(self, admin_token):
        """Verify recent signups structure"""
        response = requests.get(
            f"{BASE_URL}/api/admin/revenue",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        signups = response.json()["recent_signups"]
        
        assert isinstance(signups, list), "recent_signups should be list"
        
        if signups:
            signup = signups[0]
            required_fields = ["id", "email", "name", "date"]
            for field in required_fields:
                assert field in signup, f"Missing '{field}' in signup"
        
        print(f"PASS: Recent signups: {len(signups)} items")
    
    def test_admin_revenue_alerts(self, admin_token):
        """Verify alerts structure"""
        response = requests.get(
            f"{BASE_URL}/api/admin/revenue",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        alerts = response.json()["alerts"]
        
        assert "failed_payments" in alerts, "Missing 'failed_payments' in alerts"
        assert "cancelled_last_30d" in alerts, "Missing 'cancelled_last_30d' in alerts"
        assert "past_due_accounts" in alerts, "Missing 'past_due_accounts' in alerts"
        
        assert isinstance(alerts["failed_payments"], int)
        assert isinstance(alerts["cancelled_last_30d"], int)
        assert isinstance(alerts["past_due_accounts"], list)
        
        print(f"PASS: Alerts - failed payments: {alerts['failed_payments']}, cancelled: {alerts['cancelled_last_30d']}")
    
    def test_admin_revenue_date_range_30days(self, admin_token):
        """Test 30-day date range"""
        response = requests.get(
            f"{BASE_URL}/api/admin/revenue?days=30",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["period_days"] == 30
        assert len(data["revenue_trend"]) == 30
        print(f"PASS: 30-day range works correctly")
    
    def test_admin_revenue_date_range_60days(self, admin_token):
        """Test 60-day date range"""
        response = requests.get(
            f"{BASE_URL}/api/admin/revenue?days=60",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["period_days"] == 60
        assert len(data["revenue_trend"]) == 60
        print(f"PASS: 60-day range works correctly")
    
    def test_admin_revenue_date_range_90days(self, admin_token):
        """Test 90-day date range (default)"""
        response = requests.get(
            f"{BASE_URL}/api/admin/revenue?days=90",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["period_days"] == 90
        assert len(data["revenue_trend"]) == 90
        print(f"PASS: 90-day range works correctly")


class TestAdminRevenueExport:
    """Test GET /api/admin/revenue/export endpoint"""
    
    @pytest.fixture
    def admin_token(self):
        """Get admin user token"""
        response = requests.post(f"{BASE_URL}/api/auth/token", json={
            "username": ADMIN_USER["email"],
            "password": ADMIN_USER["password"]
        })
        if response.status_code != 200:
            pytest.skip("Admin login failed")
        return response.json()["access_token"]
    
    @pytest.fixture
    def non_admin_token(self):
        """Get non-admin user token"""
        response = requests.post(f"{BASE_URL}/api/auth/token", json={
            "username": NON_ADMIN_USER["email"],
            "password": NON_ADMIN_USER["password"]
        })
        if response.status_code != 200:
            pytest.skip("Non-admin login failed")
        return response.json()["access_token"]
    
    def test_export_csv_for_admin(self, admin_token):
        """Admin can export CSV"""
        response = requests.get(
            f"{BASE_URL}/api/admin/revenue/export",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        # Check content type
        content_type = response.headers.get("content-type", "")
        assert "text/csv" in content_type, f"Expected text/csv, got {content_type}"
        
        # Check content disposition header
        content_disp = response.headers.get("content-disposition", "")
        assert "attachment" in content_disp, "Missing attachment in content-disposition"
        assert ".csv" in content_disp, "Missing .csv extension in filename"
        
        # Check CSV content has headers
        content = response.text
        assert "Transaction ID" in content, "Missing header row in CSV"
        assert "Email" in content, "Missing Email column"
        assert "Tier" in content, "Missing Tier column"
        assert "Amount" in content, "Missing Amount column"
        
        print(f"PASS: CSV export works for admin")
        print(f"  Content-Type: {content_type}")
        print(f"  Content-Disposition: {content_disp}")
        lines = content.strip().split("\n")
        print(f"  CSV rows: {len(lines)} (including header)")
    
    def test_export_returns_403_for_non_admin(self, non_admin_token):
        """Non-admin user gets 403 on export"""
        response = requests.get(
            f"{BASE_URL}/api/admin/revenue/export",
            headers={"Authorization": f"Bearer {non_admin_token}"}
        )
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
        print(f"PASS: Non-admin gets 403 on export attempt")
    
    def test_export_returns_401_without_auth(self):
        """Unauthenticated request gets 401"""
        response = requests.get(f"{BASE_URL}/api/admin/revenue/export")
        assert response.status_code in [401, 403], f"Expected 401 or 403, got {response.status_code}"
        print(f"PASS: Unauthenticated export request returns {response.status_code}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
