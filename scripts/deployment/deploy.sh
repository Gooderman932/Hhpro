#!/bin/bash
# Production Deployment Script for Construction Intelligence Platform
#
# Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.
# PROPRIETARY AND CONFIDENTIAL - Unauthorized use prohibited.

set -e

echo "=================================="
echo "Production Deployment Script"
echo "=================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}Error: .env file not found!${NC}"
    echo "Please copy .env.production to .env and configure it:"
    echo "  cp .env.production .env"
    echo "  nano .env"
    exit 1
fi

# Check if required environment variables are set
echo -e "${YELLOW}Checking environment configuration...${NC}"
source .env

if [ "$SECRET_KEY" = "CHANGE_THIS_TO_A_RANDOM_SECRET_KEY_AT_LEAST_32_CHARS" ]; then
    echo -e "${RED}Error: SECRET_KEY not configured!${NC}"
    echo "Please set a secure SECRET_KEY in .env file"
    exit 1
fi

if [ "$POSTGRES_PASSWORD" = "CHANGE_THIS_TO_A_STRONG_PASSWORD" ]; then
    echo -e "${RED}Error: POSTGRES_PASSWORD not configured!${NC}"
    echo "Please set a secure POSTGRES_PASSWORD in .env file"
    exit 1
fi

echo -e "${GREEN}✓ Environment configuration validated${NC}"

# Pull latest code
echo -e "${YELLOW}Pulling latest code...${NC}"
git pull origin main || {
    echo -e "${RED}Error: Failed to pull latest code${NC}"
    exit 1
}
echo -e "${GREEN}✓ Code updated${NC}"

# Build Docker images
echo -e "${YELLOW}Building Docker images...${NC}"
docker-compose -f docker-compose.prod.yml build || {
    echo -e "${RED}Error: Failed to build Docker images${NC}"
    exit 1
}
echo -e "${GREEN}✓ Docker images built${NC}"

# Stop old containers
echo -e "${YELLOW}Stopping old containers...${NC}"
docker-compose -f docker-compose.prod.yml down
echo -e "${GREEN}✓ Old containers stopped${NC}"

# Start new containers
echo -e "${YELLOW}Starting new containers...${NC}"
docker-compose -f docker-compose.prod.yml up -d || {
    echo -e "${RED}Error: Failed to start containers${NC}"
    exit 1
}
echo -e "${GREEN}✓ Containers started${NC}"

# Wait for services to be healthy
echo -e "${YELLOW}Waiting for services to be healthy...${NC}"
sleep 10

# Check if backend is healthy
echo -e "${YELLOW}Checking backend health...${NC}"
for i in {1..30}; do
    if curl -f http://localhost/health > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Backend is healthy${NC}"
        break
    fi
    if [ $i -eq 30 ]; then
        echo -e "${RED}Error: Backend failed to become healthy${NC}"
        docker-compose -f docker-compose.prod.yml logs backend
        exit 1
    fi
    sleep 2
done

# Run database migrations
echo -e "${YELLOW}Running database migrations...${NC}"
docker-compose -f docker-compose.prod.yml exec -T backend alembic upgrade head || {
    echo -e "${YELLOW}Warning: Migration failed or not needed${NC}"
}
echo -e "${GREEN}✓ Database migrations completed${NC}"

# Show running containers
echo ""
echo -e "${GREEN}Deployment completed successfully!${NC}"
echo ""
echo "Running containers:"
docker-compose -f docker-compose.prod.yml ps

echo ""
echo "Application URLs:"
echo "  Frontend: http://localhost (or your domain)"
echo "  Backend API: http://localhost/api/v1"
echo "  Health Check: http://localhost/health"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Configure SSL/TLS certificates for HTTPS"
echo "2. Set up database backups"
echo "3. Configure monitoring and alerts"
echo "4. Review logs: docker-compose -f docker-compose.prod.yml logs -f"
