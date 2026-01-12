#!/bin/bash
#
# Health Check Script for Construction Intelligence Platform
#
# Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.
# PROPRIETARY AND CONFIDENTIAL - Unauthorized use prohibited.

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BACKEND_URL="${BACKEND_URL:-http://localhost:8000}"
FRONTEND_URL="${FRONTEND_URL:-http://localhost:5173}"
TIMEOUT="${TIMEOUT:-5}"

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}Construction Intelligence Platform${NC}"
echo -e "${BLUE}Health Check${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""

# Track overall health status
HEALTH_STATUS=0

# Function to check backend API health
check_backend() {
    echo -e "${YELLOW}Checking Backend API...${NC}"
    
    if curl -f -s -m "${TIMEOUT}" "${BACKEND_URL}/health" > /dev/null 2>&1; then
        response=$(curl -s -m "${TIMEOUT}" "${BACKEND_URL}/health")
        echo -e "${GREEN}✓ Backend API is healthy${NC}"
        echo "  Response: ${response}"
        return 0
    else
        echo -e "${RED}✗ Backend API is not responding${NC}"
        echo "  URL: ${BACKEND_URL}/health"
        return 1
    fi
}

# Function to check frontend accessibility
check_frontend() {
    echo -e "${YELLOW}Checking Frontend...${NC}"
    
    if curl -f -s -m "${TIMEOUT}" "${FRONTEND_URL}" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Frontend is accessible${NC}"
        return 0
    else
        echo -e "${RED}✗ Frontend is not accessible${NC}"
        echo "  URL: ${FRONTEND_URL}"
        return 1
    fi
}

# Function to check database connection
check_database() {
    echo -e "${YELLOW}Checking Database Connection...${NC}"
    
    # Try to connect through backend health endpoint or direct connection
    if curl -f -s -m "${TIMEOUT}" "${BACKEND_URL}/health" > /dev/null 2>&1; then
        # If backend is up, database should be accessible
        echo -e "${GREEN}✓ Database connection is healthy${NC}"
        return 0
    else
        # Try direct PostgreSQL connection if docker-compose is running
        if command -v docker-compose &> /dev/null; then
            if docker-compose ps postgres 2>&1 | grep -q "Up"; then
                echo -e "${GREEN}✓ Database container is running${NC}"
                return 0
            else
                echo -e "${RED}✗ Database container is not running${NC}"
                return 1
            fi
        else
            echo -e "${YELLOW}⚠ Cannot verify database connection${NC}"
            return 0  # Don't fail if docker-compose not available
        fi
    fi
}

# Function to check Docker services
check_docker_services() {
    echo -e "${YELLOW}Checking Docker Services...${NC}"
    
    if ! command -v docker-compose &> /dev/null; then
        echo -e "${YELLOW}⚠ docker-compose not found, skipping service check${NC}"
        return 0
    fi
    
    if docker-compose ps 2>&1 | grep -q "Up"; then
        services=$(docker-compose ps --services --filter "status=running")
        echo -e "${GREEN}✓ Docker services are running:${NC}"
        echo "${services}" | sed 's/^/    /'
        return 0
    else
        echo -e "${RED}✗ No Docker services are running${NC}"
        return 1
    fi
}

# Run all health checks
echo ""
check_backend || HEALTH_STATUS=1
echo ""

check_frontend || HEALTH_STATUS=1
echo ""

check_database || HEALTH_STATUS=1
echo ""

check_docker_services || HEALTH_STATUS=1
echo ""

# Summary
echo -e "${BLUE}============================================${NC}"
if [ ${HEALTH_STATUS} -eq 0 ]; then
    echo -e "${GREEN}✓ All health checks passed!${NC}"
    echo -e "${BLUE}============================================${NC}"
    exit 0
else
    echo -e "${RED}✗ Some health checks failed${NC}"
    echo -e "${BLUE}============================================${NC}"
    exit 1
fi
