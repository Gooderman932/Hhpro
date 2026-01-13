#!/bin/bash
# Health Monitoring Script for Construction Intelligence Platform
#
# Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.
# PROPRIETARY AND CONFIDENTIAL - Unauthorized use prohibited.

set -e

# Configuration
HEALTH_ENDPOINT="http://localhost/health"
BACKEND_ENDPOINT="http://localhost:8000/health"
MAX_RETRIES=3
RETRY_DELAY=5

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Function to check endpoint
check_endpoint() {
    local endpoint=$1
    local name=$2
    local retries=0
    
    while [ $retries -lt $MAX_RETRIES ]; do
        if curl -f -s "$endpoint" > /dev/null 2>&1; then
            echo -e "${GREEN}✓ $name is healthy${NC}"
            return 0
        fi
        retries=$((retries + 1))
        if [ $retries -lt $MAX_RETRIES ]; then
            echo -e "${YELLOW}⚠ $name not responding, retrying in ${RETRY_DELAY}s... (attempt $retries/$MAX_RETRIES)${NC}"
            sleep $RETRY_DELAY
        fi
    done
    
    echo -e "${RED}✗ $name is unhealthy${NC}"
    return 1
}

# Function to check container
check_container() {
    local container=$1
    local status=$(docker-compose -f docker-compose.prod.yml ps -q "$container" 2>/dev/null)
    
    if [ -z "$status" ]; then
        echo -e "${RED}✗ $container is not running${NC}"
        return 1
    fi
    
    local health=$(docker inspect --format='{{.State.Health.Status}}' "$(docker-compose -f docker-compose.prod.yml ps -q "$container")" 2>/dev/null || echo "unknown")
    
    if [ "$health" = "healthy" ] || [ "$health" = "unknown" ]; then
        echo -e "${GREEN}✓ $container is running${NC}"
        return 0
    else
        echo -e "${RED}✗ $container is unhealthy (status: $health)${NC}"
        return 1
    fi
}

# Function to check disk space
check_disk_space() {
    local usage=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
    
    if [ "$usage" -lt 80 ]; then
        echo -e "${GREEN}✓ Disk space OK (${usage}% used)${NC}"
        return 0
    elif [ "$usage" -lt 90 ]; then
        echo -e "${YELLOW}⚠ Disk space warning (${usage}% used)${NC}"
        return 0
    else
        echo -e "${RED}✗ Disk space critical (${usage}% used)${NC}"
        return 1
    fi
}

# Function to check memory
check_memory() {
    local usage=$(free | awk 'NR==2 {printf "%.0f", $3/$2 * 100}')
    
    if [ "$usage" -lt 80 ]; then
        echo -e "${GREEN}✓ Memory OK (${usage}% used)${NC}"
        return 0
    elif [ "$usage" -lt 90 ]; then
        echo -e "${YELLOW}⚠ Memory warning (${usage}% used)${NC}"
        return 0
    else
        echo -e "${RED}✗ Memory critical (${usage}% used)${NC}"
        return 1
    fi
}

echo "=================================="
echo "Health Check Report"
echo "$(date)"
echo "=================================="
echo ""

# Track overall health
all_healthy=0

# Check containers
echo "Container Status:"
check_container "postgres" || all_healthy=1
check_container "redis" || all_healthy=1
check_container "backend" || all_healthy=1
check_container "frontend" || all_healthy=1
check_container "nginx" || all_healthy=1
echo ""

# Check endpoints
echo "Endpoint Health:"
check_endpoint "$HEALTH_ENDPOINT" "Main Application" || all_healthy=1
check_endpoint "$BACKEND_ENDPOINT" "Backend API" || all_healthy=1
echo ""

# Check system resources
echo "System Resources:"
check_disk_space || all_healthy=1
check_memory || all_healthy=1
echo ""

# Summary
if [ $all_healthy -eq 0 ]; then
    echo -e "${GREEN}=================================="
    echo "Overall Status: HEALTHY ✓"
    echo "==================================${NC}"
    exit 0
else
    echo -e "${RED}=================================="
    echo "Overall Status: UNHEALTHY ✗"
    echo "==================================${NC}"
    echo ""
    echo "Review logs for details:"
    echo "  docker-compose -f docker-compose.prod.yml logs"
    exit 1
fi
