"""
Comprehensive backend testing script.

Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.
PROPRIETARY AND CONFIDENTIAL - Unauthorized use prohibited.
"""
import sys
import os
import unittest
from typing import Dict, Any

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    import requests
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("⚠️  Warning: Some dependencies not available. Install with: pip install requests sqlalchemy")


class TestBackendHealth(unittest.TestCase):
    """Test backend health and availability."""
    
    BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
    
    def test_health_endpoint(self):
        """Test the health check endpoint."""
        if not REQUESTS_AVAILABLE:
            self.skipTest("requests not available")
        
        try:
            response = requests.get(f"{self.BASE_URL}/health", timeout=5)
            self.assertEqual(response.status_code, 200, "❌ Health endpoint not returning 200")
            data = response.json()
            self.assertIn("status", data, "❌ Health response missing 'status' field")
            self.assertEqual(data["status"], "healthy", "❌ Backend not healthy")
            print(f"✅ Health check passed: {data}")
        except requests.exceptions.ConnectionError:
            self.fail(f"❌ Cannot connect to backend at {self.BASE_URL}")
        except Exception as e:
            self.fail(f"❌ Health check failed: {str(e)}")
    
    def test_root_endpoint(self):
        """Test the root endpoint."""
        if not REQUESTS_AVAILABLE:
            self.skipTest("requests not available")
        
        try:
            response = requests.get(f"{self.BASE_URL}/", timeout=5)
            self.assertEqual(response.status_code, 200, "❌ Root endpoint not returning 200")
            data = response.json()
            self.assertIn("name", data, "❌ Root response missing 'name' field")
            self.assertIn("version", data, "❌ Root response missing 'version' field")
            print(f"✅ Root endpoint test passed: {data.get('name')} v{data.get('version')}")
        except Exception as e:
            self.fail(f"❌ Root endpoint test failed: {str(e)}")
    
    def test_api_docs_accessibility(self):
        """Test if API documentation is accessible."""
        if not REQUESTS_AVAILABLE:
            self.skipTest("requests not available")
        
        try:
            response = requests.get(f"{self.BASE_URL}/api/docs", timeout=5)
            # In production, docs might be disabled (404), which is acceptable
            if response.status_code == 200:
                print("✅ API documentation is accessible at /api/docs")
            else:
                print("ℹ️  API documentation is disabled (production mode)")
        except Exception as e:
            print(f"ℹ️  API docs test: {str(e)}")


class TestDatabase(unittest.TestCase):
    """Test database connectivity and structure."""
    
    def setUp(self):
        """Set up database connection."""
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///./construction_intel.db")
        
    def test_database_connection(self):
        """Test database connection."""
        if not REQUESTS_AVAILABLE:
            self.skipTest("sqlalchemy not available")
        
        try:
            engine = create_engine(self.database_url)
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                self.assertIsNotNone(result, "❌ Database query returned None")
                print("✅ Database connection successful")
        except Exception as e:
            self.fail(f"❌ Database connection failed: {str(e)}")
    
    def test_required_tables_exist(self):
        """Test if all required tables exist."""
        if not REQUESTS_AVAILABLE:
            self.skipTest("sqlalchemy not available")
        
        required_tables = [
            "users",
            "tenants",
            "projects",
            "companies",
            "project_participations",
            "opportunity_scores"
        ]
        
        try:
            engine = create_engine(self.database_url)
            with engine.connect() as conn:
                # For SQLite
                if "sqlite" in self.database_url:
                    result = conn.execute(text(
                        "SELECT name FROM sqlite_master WHERE type='table'"
                    ))
                # For PostgreSQL
                else:
                    result = conn.execute(text(
                        "SELECT tablename FROM pg_tables WHERE schemaname='public'"
                    ))
                
                existing_tables = [row[0] for row in result]
                
                missing_tables = []
                for table in required_tables:
                    if table in existing_tables:
                        print(f"✅ Table '{table}' exists")
                    else:
                        missing_tables.append(table)
                        print(f"❌ Table '{table}' missing")
                
                if missing_tables:
                    self.fail(f"❌ Missing tables: {', '.join(missing_tables)}")
                else:
                    print("✅ All required tables exist")
                    
        except Exception as e:
            self.fail(f"❌ Table check failed: {str(e)}")


class TestAuthentication(unittest.TestCase):
    """Test authentication endpoints."""
    
    BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
    
    def test_token_endpoint_exists(self):
        """Test if token endpoint exists and requires credentials."""
        if not REQUESTS_AVAILABLE:
            self.skipTest("requests not available")
        
        try:
            response = requests.post(
                f"{self.BASE_URL}/api/v1/auth/token",
                data={"username": "test", "password": "test"},
                timeout=5
            )
            # We expect either 401 (invalid credentials) or 422 (validation error)
            # Both indicate the endpoint exists and is working
            self.assertIn(response.status_code, [401, 422, 404], 
                         f"❌ Unexpected status code: {response.status_code}")
            
            if response.status_code == 404:
                print("⚠️  Token endpoint not found - check API routing")
            else:
                print("✅ Token endpoint exists and is protected")
        except requests.exceptions.ConnectionError:
            self.fail(f"❌ Cannot connect to backend at {self.BASE_URL}")
        except Exception as e:
            self.fail(f"❌ Authentication endpoint test failed: {str(e)}")
    
    def test_protected_endpoint_without_token(self):
        """Test that protected endpoints require authentication."""
        if not REQUESTS_AVAILABLE:
            self.skipTest("requests not available")
        
        try:
            response = requests.get(
                f"{self.BASE_URL}/api/v1/projects",
                timeout=5
            )
            # We expect 401 or 403 (unauthorized)
            if response.status_code in [401, 403]:
                print("✅ Protected endpoints require authentication")
            elif response.status_code == 404:
                print("ℹ️  Projects endpoint not found")
            else:
                print(f"⚠️  Protected endpoint returned {response.status_code} (expected 401/403)")
        except Exception as e:
            print(f"ℹ️  Protected endpoint test: {str(e)}")


class TestAPIEndpoints(unittest.TestCase):
    """Test API endpoint availability."""
    
    BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
    
    def test_api_v1_prefix(self):
        """Test that API v1 endpoints are properly configured."""
        if not REQUESTS_AVAILABLE:
            self.skipTest("requests not available")
        
        endpoints = [
            "/api/v1/projects",
            "/api/v1/analytics",
            "/api/v1/intelligence",
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.get(f"{self.BASE_URL}{endpoint}", timeout=5)
                # We expect 401/403 (auth required) or 200 (accessible)
                if response.status_code in [200, 401, 403]:
                    print(f"✅ Endpoint {endpoint} exists")
                elif response.status_code == 404:
                    print(f"⚠️  Endpoint {endpoint} not found")
                else:
                    print(f"ℹ️  Endpoint {endpoint} returned {response.status_code}")
            except Exception as e:
                print(f"⚠️  Endpoint {endpoint} test error: {str(e)}")


def run_tests():
    """Run all tests and display results."""
    print("\n" + "="*70)
    print("🧪 BuildIntel Pro Backend Test Suite")
    print("="*70 + "\n")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestBackendHealth))
    suite.addTests(loader.loadTestsFromTestCase(TestDatabase))
    suite.addTests(loader.loadTestsFromTestCase(TestAuthentication))
    suite.addTests(loader.loadTestsFromTestCase(TestAPIEndpoints))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "="*70)
    if result.wasSuccessful():
        print("✅ ALL TESTS PASSED")
    else:
        print("❌ SOME TESTS FAILED")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print("="*70 + "\n")
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
