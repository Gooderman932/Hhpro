#!/bin/bash
#
# Deployment Helper Script for Construction Intelligence Platform
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
ENVIRONMENT="${1:-staging}"
IMAGE_TAG="${2:-latest}"
RUN_MIGRATIONS="${3:-false}"

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}Construction Intelligence Platform${NC}"
echo -e "${BLUE}Deployment Helper${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""

# Validate environment
if [[ ! "${ENVIRONMENT}" =~ ^(staging|production)$ ]]; then
    echo -e "${RED}Error: Invalid environment '${ENVIRONMENT}'${NC}"
    echo "Usage: $0 <staging|production> [image_tag] [run_migrations]"
    exit 1
fi

echo -e "${YELLOW}Deployment Configuration:${NC}"
echo "  Environment: ${ENVIRONMENT}"
echo "  Image Tag: ${IMAGE_TAG}"
echo "  Run Migrations: ${RUN_MIGRATIONS}"
echo ""

# Pre-deployment checks
echo -e "${BLUE}Running pre-deployment checks...${NC}"

# Check if required tools are installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}✗ Docker not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker is available${NC}"

if ! command -v docker-compose &> /dev/null; then
    echo -e "${YELLOW}⚠ docker-compose not found, using docker compose plugin${NC}"
fi

# Check if environment variables are set
if [ "${ENVIRONMENT}" == "production" ]; then
    echo -e "${YELLOW}Checking production environment variables...${NC}"
    
    required_vars=("SECRET_KEY" "DATABASE_URL" "POSTGRES_PASSWORD" "REDIS_PASSWORD")
    missing_vars=()
    
    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            missing_vars+=("${var}")
        fi
    done
    
    if [ ${#missing_vars[@]} -ne 0 ]; then
        echo -e "${RED}✗ Missing required environment variables:${NC}"
        printf '  - %s\n' "${missing_vars[@]}"
        echo ""
        echo "Please set these variables before deploying to production."
        exit 1
    fi
    echo -e "${GREEN}✓ All required environment variables are set${NC}"
fi

# Confirm deployment for production
if [ "${ENVIRONMENT}" == "production" ]; then
    echo ""
    echo -e "${RED}⚠️  WARNING: You are about to deploy to PRODUCTION!${NC}"
    read -p "Are you sure you want to continue? (yes/no): " confirm
    
    if [ "${confirm}" != "yes" ]; then
        echo -e "${YELLOW}Deployment cancelled${NC}"
        exit 0
    fi
fi

# Pull latest images
echo ""
echo -e "${BLUE}Pulling Docker images...${NC}"
export IMAGE_TAG="${IMAGE_TAG}"

if docker-compose -f docker-compose.prod.yml pull; then
    echo -e "${GREEN}✓ Images pulled successfully${NC}"
else
    echo -e "${RED}✗ Failed to pull images${NC}"
    exit 1
fi

# Run database migrations if requested
if [ "${RUN_MIGRATIONS}" == "true" ]; then
    echo ""
    echo -e "${BLUE}Running database migrations...${NC}"
    
    # Start only the database if not already running
    docker-compose -f docker-compose.prod.yml up -d postgres
    sleep 5
    
    # Run migrations
    if docker-compose -f docker-compose.prod.yml run --rm backend alembic upgrade head; then
        echo -e "${GREEN}✓ Migrations completed successfully${NC}"
    else
        echo -e "${RED}✗ Migration failed${NC}"
        exit 1
    fi
fi

# Deploy services
echo ""
echo -e "${BLUE}Deploying services...${NC}"

if docker-compose -f docker-compose.prod.yml up -d; then
    echo -e "${GREEN}✓ Services deployed successfully${NC}"
else
    echo -e "${RED}✗ Deployment failed${NC}"
    exit 1
fi

# Wait for services to be healthy
echo ""
echo -e "${BLUE}Waiting for services to be healthy...${NC}"
sleep 10

# Run health checks
echo ""
if ./scripts/health_check.sh; then
    echo -e "${GREEN}✓ Health checks passed${NC}"
else
    echo -e "${RED}✗ Health checks failed${NC}"
    echo ""
    echo -e "${YELLOW}Rolling back deployment...${NC}"
    docker-compose -f docker-compose.prod.yml down
    exit 1
fi

# Success
echo ""
echo -e "${BLUE}============================================${NC}"
echo -e "${GREEN}✓ Deployment completed successfully!${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""
echo "Environment: ${ENVIRONMENT}"
echo "Image Tag: ${IMAGE_TAG}"
echo ""
echo "View logs with: docker-compose -f docker-compose.prod.yml logs -f"
echo "Check status with: docker-compose -f docker-compose.prod.yml ps"
