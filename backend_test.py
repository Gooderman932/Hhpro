#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime

class HDrywallAPITester:
    def __init__(self, base_url="https://job-trade-match.preview.emergentagent.com"):
        self.base_url = base_url
        self.token = None
        self.user_id = None
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def log_test(self, name, success, details=""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name}")
        else:
            print(f"❌ {name} - {details}")
        
        self.test_results.append({
            "test": name,
            "success": success,
            "details": details
        })

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.base_url}/api/{endpoint}"
        test_headers = {'Content-Type': 'application/json'}
        
        if self.token:
            test_headers['Authorization'] = f'Bearer {self.token}'
        
        if headers:
            test_headers.update(headers)

        try:
            if method == 'GET':
                response = requests.get(url, headers=test_headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=test_headers)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=test_headers)
            elif method == 'DELETE':
                response = requests.delete(url, headers=test_headers)

            success = response.status_code == expected_status
            details = f"Status: {response.status_code}"
            
            if not success:
                details += f" (Expected {expected_status})"
                try:
                    error_data = response.json()
                    details += f" - {error_data.get('detail', 'Unknown error')}"
                except:
                    details += f" - {response.text[:100]}"

            self.log_test(name, success, details)
            
            return success, response.json() if success and response.content else {}

        except Exception as e:
            self.log_test(name, False, f"Error: {str(e)}")
            return False, {}

    def test_health_endpoints(self):
        """Test basic health endpoints"""
        print("\n🔍 Testing Health Endpoints...")
        self.run_test("Health Check", "GET", "health", 200)
        self.run_test("Root Endpoint", "GET", "", 200)

    def test_trade_codes(self):
        """Test trade codes endpoint"""
        print("\n🔍 Testing Trade Codes...")
        success, data = self.run_test("Get Trade Codes", "GET", "trade-codes", 200)
        if success and isinstance(data, dict) and len(data) > 0:
            self.log_test("Trade Codes Data Valid", True, f"Found {len(data)} trade codes")
        elif success:
            self.log_test("Trade Codes Data Valid", False, "Empty or invalid trade codes")

    def test_products_endpoints(self):
        """Test products endpoints"""
        print("\n🔍 Testing Products...")
        success, products = self.run_test("Get Products", "GET", "products", 200)
        if success and isinstance(products, list):
            self.log_test("Products Data Valid", True, f"Found {len(products)} products")
            if len(products) >= 12:
                self.log_test("Seeded Products Check", True, f"Found {len(products)} products (expected 12+)")
            else:
                self.log_test("Seeded Products Check", False, f"Only {len(products)} products found, expected 12+")
        elif success:
            self.log_test("Products Data Valid", False, "Invalid products data structure")
        
        # Test product categories
        self.run_test("Get Product Categories", "GET", "product-categories", 200)

    def test_market_data_tiers(self):
        """Test market data tiers"""
        print("\n🔍 Testing Market Data Tiers...")
        success, tiers = self.run_test("Get Market Data Tiers", "GET", "market-data/tiers", 200)
        if success and isinstance(tiers, list) and len(tiers) == 3:
            self.log_test("Market Data Tiers Valid", True, f"Found {len(tiers)} tiers")
            # Check tier structure
            required_fields = ['tier_id', 'name', 'price', 'features']
            for tier in tiers:
                if all(field in tier for field in required_fields):
                    self.log_test(f"Tier {tier['tier_id']} Structure", True)
                else:
                    self.log_test(f"Tier {tier['tier_id']} Structure", False, "Missing required fields")
        elif success:
            self.log_test("Market Data Tiers Valid", False, f"Expected 3 tiers, got {len(tiers) if isinstance(tiers, list) else 'invalid'}")

    def test_user_registration_contractor(self):
        """Test contractor registration"""
        print("\n🔍 Testing User Registration (Contractor)...")
        timestamp = datetime.now().strftime('%H%M%S')
        test_data = {
            "email": f"contractor_{timestamp}@test.com",
            "password": "TestPass123!",
            "name": f"Test Contractor {timestamp}",
            "user_type": "contractor"
        }
        
        success, response = self.run_test("Register Contractor", "POST", "auth/register", 200, test_data)
        if success and 'access_token' in response and 'user' in response:
            self.token = response['access_token']
            self.user_id = response['user']['user_id']
            self.log_test("Contractor Registration Token", True, "Token received")
            return True
        elif success:
            self.log_test("Contractor Registration Token", False, "Missing token or user data")
        return False

    def test_user_registration_subcontractor(self):
        """Test subcontractor registration"""
        print("\n🔍 Testing User Registration (Subcontractor)...")
        timestamp = datetime.now().strftime('%H%M%S')
        test_data = {
            "email": f"subcontractor_{timestamp}@test.com",
            "password": "TestPass123!",
            "name": f"Test Subcontractor {timestamp}",
            "user_type": "subcontractor"
        }
        
        success, response = self.run_test("Register Subcontractor", "POST", "auth/register", 200, test_data)
        if success and 'access_token' in response and 'user' in response:
            self.log_test("Subcontractor Registration Token", True, "Token received")
            return True, response['access_token'], response['user']['user_id']
        elif success:
            self.log_test("Subcontractor Registration Token", False, "Missing token or user data")
        return False, None, None

    def test_user_login(self):
        """Test user login"""
        print("\n🔍 Testing User Login...")
        # First register a user to login with
        timestamp = datetime.now().strftime('%H%M%S')
        register_data = {
            "email": f"login_test_{timestamp}@test.com",
            "password": "TestPass123!",
            "name": f"Login Test {timestamp}",
            "user_type": "contractor"
        }
        
        reg_success, reg_response = self.run_test("Register for Login Test", "POST", "auth/register", 200, register_data)
        if not reg_success:
            return False
        
        # Now test login
        login_data = {
            "email": register_data["email"],
            "password": register_data["password"]
        }
        
        success, response = self.run_test("User Login", "POST", "auth/login", 200, login_data)
        if success and 'access_token' in response:
            self.log_test("Login Token Valid", True, "Token received")
            return True
        elif success:
            self.log_test("Login Token Valid", False, "Missing token")
        return False

    def test_auth_me(self):
        """Test auth/me endpoint"""
        print("\n🔍 Testing Auth Me...")
        if not self.token:
            self.log_test("Auth Me", False, "No token available")
            return False
        
        success, response = self.run_test("Get Current User", "GET", "auth/me", 200)
        if success and 'user_id' in response:
            self.log_test("Auth Me Data Valid", True, f"User ID: {response['user_id']}")
            return True
        elif success:
            self.log_test("Auth Me Data Valid", False, "Missing user data")
        return False

    def test_job_creation(self):
        """Test job creation (contractor only)"""
        print("\n🔍 Testing Job Creation...")
        if not self.token:
            self.log_test("Job Creation", False, "No token available")
            return None
        
        job_data = {
            "title": "Test Drywall Installation Job",
            "description": "Looking for experienced drywall installers for commercial project",
            "trade_codes": ["09"],
            "location": "123 Test St, Test City, TX",
            "city": "Test City",
            "state": "TX",
            "pay_rate": "35.00",
            "pay_type": "hourly",
            "duration": "2 weeks",
            "certifications_required": ["OSHA 10"],
            "experience_years": 3
        }
        
        success, response = self.run_test("Create Job", "POST", "jobs", 201, job_data)
        if success and 'job_id' in response:
            self.log_test("Job Creation Data Valid", True, f"Job ID: {response['job_id']}")
            return response['job_id']
        elif success:
            self.log_test("Job Creation Data Valid", False, "Missing job_id")
        return None

    def test_jobs_listing(self):
        """Test jobs listing"""
        print("\n🔍 Testing Jobs Listing...")
        success, jobs = self.run_test("Get Jobs", "GET", "jobs", 200)
        if success and isinstance(jobs, list):
            self.log_test("Jobs Listing Valid", True, f"Found {len(jobs)} jobs")
            return True
        elif success:
            self.log_test("Jobs Listing Valid", False, "Invalid jobs data structure")
        return False

    def test_worker_profile_creation(self):
        """Test worker profile creation (subcontractor only)"""
        print("\n🔍 Testing Worker Profile Creation...")
        # Register a subcontractor first
        sub_success, sub_token, sub_user_id = self.test_user_registration_subcontractor()
        if not sub_success:
            return None
        
        # Switch to subcontractor token
        original_token = self.token
        original_user_id = self.user_id
        self.token = sub_token
        self.user_id = sub_user_id
        
        profile_data = {
            "headline": "Experienced Drywall Specialist",
            "bio": "10+ years of commercial and residential drywall installation experience",
            "trade_codes": ["09"],
            "skills": ["Drywall Installation", "Taping", "Texturing", "Repair"],
            "experience_years": 10,
            "certifications": ["OSHA 10", "Lead Safe Certified"],
            "location": "Dallas, TX",
            "city": "Dallas",
            "state": "TX",
            "availability": "immediate",
            "hourly_rate_min": 30.0,
            "hourly_rate_max": 45.0
        }
        
        success, response = self.run_test("Create Worker Profile", "POST", "profiles", 201, profile_data)
        profile_id = None
        if success and 'profile_id' in response:
            self.log_test("Profile Creation Data Valid", True, f"Profile ID: {response['profile_id']}")
            profile_id = response['profile_id']
        elif success:
            self.log_test("Profile Creation Data Valid", False, "Missing profile_id")
        
        # Restore original token
        self.token = original_token
        self.user_id = original_user_id
        
        return profile_id

    def test_profiles_listing(self):
        """Test worker profiles listing"""
        print("\n🔍 Testing Worker Profiles Listing...")
        success, profiles = self.run_test("Get Worker Profiles", "GET", "profiles", 200)
        if success and isinstance(profiles, list):
            self.log_test("Profiles Listing Valid", True, f"Found {len(profiles)} profiles")
            return True
        elif success:
            self.log_test("Profiles Listing Valid", False, "Invalid profiles data structure")
        return False

    def test_cart_functionality(self):
        """Test cart functionality"""
        print("\n🔍 Testing Cart Functionality...")
        
        # Get products first
        success, products = self.run_test("Get Products for Cart", "GET", "products", 200)
        if not success or not products:
            self.log_test("Cart Test Setup", False, "No products available")
            return False
        
        product_id = products[0]['product_id']
        
        # Test add to cart
        cart_data = {"product_id": product_id, "quantity": 2}
        success, response = self.run_test("Add to Cart", "POST", "cart/add", 200, cart_data)
        
        # Test get cart
        success, cart = self.run_test("Get Cart", "GET", "cart", 200)
        if success and 'items' in cart and len(cart['items']) > 0:
            self.log_test("Cart Items Valid", True, f"Found {len(cart['items'])} items")
        elif success:
            self.log_test("Cart Items Valid", False, "Empty or invalid cart")
        
        return True

    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting HDrywall Repair Platform API Tests")
        print("=" * 60)
        
        # Basic health tests
        self.test_health_endpoints()
        self.test_trade_codes()
        self.test_products_endpoints()
        self.test_market_data_tiers()
        
        # Auth tests
        contractor_registered = self.test_user_registration_contractor()
        self.test_user_login()
        
        if contractor_registered:
            self.test_auth_me()
            
            # Job tests (contractor required)
            job_id = self.test_job_creation()
            self.test_jobs_listing()
            
            # Profile tests
            profile_id = self.test_worker_profile_creation()
            self.test_profiles_listing()
            
            # Cart tests
            self.test_cart_functionality()
        
        # Print summary
        print("\n" + "=" * 60)
        print(f"📊 Test Summary: {self.tests_passed}/{self.tests_run} tests passed")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All tests passed!")
            return 0
        else:
            print(f"❌ {self.tests_run - self.tests_passed} tests failed")
            return 1

def main():
    tester = HDrywallAPITester()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())