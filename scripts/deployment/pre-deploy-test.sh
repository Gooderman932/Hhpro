#!/bin/bash
# Pre-deployment Testing Script
# 
# Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.
# PROPRIETARY AND CONFIDENTIAL - Unauthorized use prohibited.

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=================================="
echo "Pre-Deployment Testing"
echo "==================================${NC}"
echo ""

FAILED_TESTS=0
PASSED_TESTS=0

# Function to run test
run_test() {
    local test_name=$1
    local test_command=$2
    
    echo -ne "Testing: $test_name ... "
    
    if eval "$test_command" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PASS${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi
}

# Check prerequisites
echo -e "${YELLOW}Checking Prerequisites...${NC}"
run_test "Docker installed" "docker --version"
run_test "Docker Compose installed" "docker-compose --version"
run_test "Git installed" "git --version"
run_test "Curl installed" "curl --version"
run_test "OpenSSL installed" "openssl version"
echo ""

# Check configuration
echo -e "${YELLOW}Checking Configuration...${NC}"
run_test ".env file exists" "[ -f .env ]"

if [ -f .env ]; then
    source .env
    run_test "SECRET_KEY is set" "[ ! -z \"$SECRET_KEY\" ]"
    run_test "SECRET_KEY changed from default" "[ \"$SECRET_KEY\" != \"CHANGE_THIS_TO_A_RANDOM_SECRET_KEY_AT_LEAST_32_CHARS\" ]"
    run_test "POSTGRES_PASSWORD is set" "[ ! -z \"$POSTGRES_PASSWORD\" ]"
    run_test "POSTGRES_PASSWORD changed from default" "[ \"$POSTGRES_PASSWORD\" != \"CHANGE_THIS_TO_A_STRONG_PASSWORD\" ]"
    run_test "CORS_ORIGINS is configured" "[ ! -z \"$CORS_ORIGINS\" ]"
    run_test "ENVIRONMENT set to production" "[ \"$ENVIRONMENT\" = \"production\" ]"
fi
echo ""

# Check Docker configuration
echo -e "${YELLOW}Checking Docker Configuration...${NC}"
run_test "docker-compose.prod.yml exists" "[ -f docker-compose.prod.yml ]"
run_test "Backend Dockerfile.prod exists" "[ -f backend/Dockerfile.prod ]"
run_test "Frontend Dockerfile.prod exists" "[ -f frontend/Dockerfile.prod ]"
run_test "Nginx config exists" "[ -f nginx/nginx.conf ]"
echo ""

# Check scripts
echo -e "${YELLOW}Checking Deployment Scripts...${NC}"
run_test "Deploy script exists" "[ -f scripts/deployment/deploy.sh ]"
run_test "Deploy script is executable" "[ -x scripts/deployment/deploy.sh ]"
run_test "Backup script exists" "[ -f scripts/deployment/backup.sh ]"
run_test "Backup script is executable" "[ -x scripts/deployment/backup.sh ]"
run_test "Health check script exists" "[ -f scripts/deployment/health-check.sh ]"
run_test "Health check script is executable" "[ -x scripts/deployment/health-check.sh ]"
echo ""

# Check documentation
echo -e "${YELLOW}Checking Documentation...${NC}"
run_test "README.md exists" "[ -f README.md ]"
run_test "DEPLOYMENT.md exists" "[ -f DEPLOYMENT.md ]"
run_test "SECURITY.md exists" "[ -f SECURITY.md ]"
run_test "QUICK_DEPLOY.md exists" "[ -f QUICK_DEPLOY.md ]"
run_test "PRODUCTION_CHECKLIST.md exists" "[ -f PRODUCTION_CHECKLIST.md ]"
echo ""

# Check for common security issues
echo -e "${YELLOW}Security Checks...${NC}"
run_test ".env not in git" "! git ls-files | grep -q '^\.env$'"
run_test ".env.production not in git" "! git ls-files | grep -q '^\.env\.production$'"
run_test "No secrets in git history" "! git grep -i 'password.*=.*[^C][^H][^A][^N][^G][^E]' $(git rev-list --all) -- .env* 2>/dev/null"
echo ""

# Optional: SSL certificate checks
if [ -d "nginx/ssl" ] && [ "$(ls -A nginx/ssl)" ]; then
    echo -e "${YELLOW}Checking SSL Certificates...${NC}"
    run_test "fullchain.pem exists" "[ -f nginx/ssl/fullchain.pem ]"
    run_test "privkey.pem exists" "[ -f nginx/ssl/privkey.pem ]"
    
    if [ -f nginx/ssl/fullchain.pem ]; then
        run_test "Certificate is valid" "openssl x509 -in nginx/ssl/fullchain.pem -noout -text"
        
        # Check expiration
        EXPIRY_DATE=$(openssl x509 -in nginx/ssl/fullchain.pem -noout -enddate | cut -d= -f2)
        EXPIRY_EPOCH=$(date -d "$EXPIRY_DATE" +%s 2>/dev/null || date -j -f "%b %d %T %Y %Z" "$EXPIRY_DATE" +%s 2>/dev/null)
        NOW_EPOCH=$(date +%s)
        DAYS_LEFT=$(( ($EXPIRY_EPOCH - $NOW_EPOCH) / 86400 ))
        
        if [ $DAYS_LEFT -gt 30 ]; then
            echo -e "Testing: Certificate expiration ... ${GREEN}✓ PASS${NC} ($DAYS_LEFT days left)"
            PASSED_TESTS=$((PASSED_TESTS + 1))
        elif [ $DAYS_LEFT -gt 0 ]; then
            echo -e "Testing: Certificate expiration ... ${YELLOW}⚠ WARNING${NC} (expires in $DAYS_LEFT days)"
            PASSED_TESTS=$((PASSED_TESTS + 1))
        else
            echo -e "Testing: Certificate expiration ... ${RED}✗ FAIL${NC} (expired)"
            FAILED_TESTS=$((FAILED_TESTS + 1))
        fi
    fi
    echo ""
fi

# Build test (dry run)
echo -e "${YELLOW}Testing Docker Build (this may take a few minutes)...${NC}"
if docker-compose -f docker-compose.prod.yml config > /dev/null 2>&1; then
    echo -e "Testing: Docker Compose configuration ... ${GREEN}✓ PASS${NC}"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "Testing: Docker Compose configuration ... ${RED}✗ FAIL${NC}"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi
echo ""

# Summary
echo -e "${BLUE}=================================="
echo "Test Summary"
echo "==================================${NC}"
echo -e "Total Tests: $((PASSED_TESTS + FAILED_TESTS))"
echo -e "${GREEN}Passed: $PASSED_TESTS${NC}"
echo -e "${RED}Failed: $FAILED_TESTS${NC}"
echo ""

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    echo -e "${GREEN}System is ready for production deployment.${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Review PRODUCTION_CHECKLIST.md"
    echo "  2. Run: ./scripts/deployment/deploy.sh"
    echo "  3. Run: make db-init"
    echo "  4. Run: ./scripts/deployment/health-check.sh"
    exit 0
else
    echo -e "${RED}✗ Some tests failed!${NC}"
    echo -e "${YELLOW}Please fix the issues above before deploying.${NC}"
    echo ""
    echo "Common fixes:"
    echo "  - Configure .env file: cp .env.production .env && nano .env"
    echo "  - Install Docker: curl -fsSL https://get.docker.com | sh"
    echo "  - Make scripts executable: chmod +x scripts/deployment/*.sh"
    exit 1
fi
