#!/bin/bash
#
# Frontend-Backend Connection Testing Script
#
# Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.
# PROPRIETARY AND CONFIDENTIAL - Unauthorized use prohibited.
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration (DEVELOPMENT DEFAULTS - Use HTTPS in production!)
BACKEND_URL="${BACKEND_URL:-http://localhost:8000}"
FRONTEND_URL="${FRONTEND_URL:-http://localhost:3000}"
TIMEOUT=5

echo "=============================================================="
echo "  🔗 BuildIntel Pro - Connection Testing"
echo "=============================================================="
echo ""

# Function to print colored output
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Test if backend is running
echo "──────────────────────────────────────────────────────────────"
echo "  Testing Backend Connection"
echo "──────────────────────────────────────────────────────────────"
echo "Backend URL: $BACKEND_URL"
echo ""

if command -v curl &> /dev/null; then
    # Test backend health endpoint
    if curl -s -f -m $TIMEOUT "${BACKEND_URL}/health" > /dev/null; then
        print_success "Backend is running and healthy"
        
        # Get backend info
        BACKEND_INFO=$(curl -s -m $TIMEOUT "${BACKEND_URL}/health")
        echo "Backend Status: $BACKEND_INFO"
    else
        print_error "Backend is not responding at $BACKEND_URL"
        print_info "Make sure the backend is running:"
        echo "  $ cd backend"
        echo "  $ uvicorn app.main:app --reload"
        exit 1
    fi
else
    print_warning "curl not found, skipping backend test"
fi

echo ""

# Test API documentation
echo "──────────────────────────────────────────────────────────────"
echo "  Testing API Documentation"
echo "──────────────────────────────────────────────────────────────"
echo ""

if command -v curl &> /dev/null; then
    if curl -s -f -m $TIMEOUT "${BACKEND_URL}/api/docs" > /dev/null 2>&1; then
        print_success "API documentation is accessible"
        echo "  📚 View docs at: ${BACKEND_URL}/api/docs"
    else
        print_warning "API documentation not accessible (may be disabled in production)"
    fi
else
    print_warning "curl not found, skipping API docs test"
fi

echo ""

# Test CORS configuration
echo "──────────────────────────────────────────────────────────────"
echo "  Testing CORS Configuration"
echo "──────────────────────────────────────────────────────────────"
echo ""

if command -v curl &> /dev/null; then
    CORS_RESPONSE=$(curl -s -I -X OPTIONS -m $TIMEOUT \
        -H "Origin: http://localhost:3000" \
        -H "Access-Control-Request-Method: GET" \
        "${BACKEND_URL}/health" 2>&1)
    
    if echo "$CORS_RESPONSE" | grep -i "access-control-allow-origin" > /dev/null; then
        print_success "CORS is properly configured"
        ALLOWED_ORIGIN=$(echo "$CORS_RESPONSE" | grep -i "access-control-allow-origin" | cut -d' ' -f2 | tr -d '\r')
        echo "  Allowed origin: $ALLOWED_ORIGIN"
    else
        print_warning "CORS headers not found in response"
        print_info "Check CORS_ORIGINS in backend configuration"
    fi
else
    print_warning "curl not found, skipping CORS test"
fi

echo ""

# Test frontend connection
echo "──────────────────────────────────────────────────────────────"
echo "  Testing Frontend Connection"
echo "──────────────────────────────────────────────────────────────"
echo "Frontend URL: $FRONTEND_URL"
echo ""

if command -v curl &> /dev/null; then
    if curl -s -f -m $TIMEOUT "$FRONTEND_URL" > /dev/null 2>&1; then
        print_success "Frontend is running"
        echo "  🌐 Access at: $FRONTEND_URL"
    else
        print_warning "Frontend is not responding at $FRONTEND_URL"
        print_info "Start the frontend with:"
        echo "  $ cd frontend"
        echo "  $ npm run dev"
    fi
else
    print_warning "curl not found, skipping frontend test"
fi

echo ""

# Test API endpoints
echo "──────────────────────────────────────────────────────────────"
echo "  Testing API Endpoints"
echo "──────────────────────────────────────────────────────────────"
echo ""

if command -v curl &> /dev/null; then
    # Test root endpoint
    if curl -s -f -m $TIMEOUT "${BACKEND_URL}/" > /dev/null; then
        print_success "Root endpoint (/) accessible"
    else
        print_error "Root endpoint (/) not accessible"
    fi
    
    # Test health endpoint
    if curl -s -f -m $TIMEOUT "${BACKEND_URL}/health" > /dev/null; then
        print_success "Health endpoint (/health) accessible"
    else
        print_error "Health endpoint (/health) not accessible"
    fi
    
    # Test protected endpoint (should return 401 or 403)
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" -m $TIMEOUT "${BACKEND_URL}/api/v1/projects")
    if [ "$STATUS" = "401" ] || [ "$STATUS" = "403" ]; then
        print_success "Protected endpoints require authentication (status: $STATUS)"
    elif [ "$STATUS" = "404" ]; then
        print_warning "Projects endpoint not found (status: 404)"
    else
        print_info "Projects endpoint returned status: $STATUS"
    fi
else
    print_warning "curl not found, skipping API endpoint tests"
fi

echo ""

# Summary and next steps
echo "=============================================================="
echo "  📝 Summary & Next Steps"
echo "=============================================================="
echo ""

if command -v curl &> /dev/null; then
    # Check if backend is healthy
    if curl -s -f -m $TIMEOUT "${BACKEND_URL}/health" > /dev/null 2>&1; then
        print_success "Backend is ready for connections"
        
        # Check if frontend is running
        if curl -s -f -m $TIMEOUT "$FRONTEND_URL" > /dev/null 2>&1; then
            print_success "Frontend is ready"
            echo ""
            echo "🚀 Your application is ready!"
            echo ""
            echo "Access the application:"
            echo "  Frontend: $FRONTEND_URL"
            echo "  Backend:  $BACKEND_URL"
            echo "  API Docs: ${BACKEND_URL}/api/docs"
        else
            echo ""
            print_info "Frontend is not running. Start it with:"
            echo "  $ cd frontend"
            echo "  $ npm install  # if dependencies not installed"
            echo "  $ npm run dev"
        fi
    else
        echo ""
        print_error "Backend is not running!"
        print_info "Start the backend with:"
        echo "  $ cd backend"
        echo "  $ pip install -r requirements.txt  # if dependencies not installed"
        echo "  $ uvicorn app.main:app --reload"
        echo ""
        print_info "Or use Docker:"
        echo "  $ docker-compose up"
    fi
else
    print_warning "Install curl to run connection tests"
    echo "  Ubuntu/Debian: sudo apt-get install curl"
    echo "  macOS: brew install curl"
    echo "  Windows: Download from https://curl.se/download.html"
fi

echo ""
echo "For more information, see:"
echo "  📖 Admin Guide: docs/ADMIN_USER_GUIDE.md"
echo "  📖 API Guide:   docs/API_INTEGRATION_GUIDE.md"
echo ""
echo "=============================================================="
