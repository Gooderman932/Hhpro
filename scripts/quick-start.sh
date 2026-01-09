#!/bin/bash
#
# Quick Start Setup Script for BuildIntel Pro
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
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Print banner
echo ""
echo -e "${CYAN}============================================================${NC}"
echo -e "${CYAN}  🚀 BuildIntel Pro - Quick Start Setup${NC}"
echo -e "${CYAN}============================================================${NC}"
echo ""

# Functions for colored output
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

print_step() {
    echo ""
    echo -e "${CYAN}──────────────────────────────────────────────────────────────${NC}"
    echo -e "${CYAN}  $1${NC}"
    echo -e "${CYAN}──────────────────────────────────────────────────────────────${NC}"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Get project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

print_info "Project directory: $PROJECT_ROOT"
echo ""

# Step 1: Check prerequisites
print_step "Step 1: Checking Prerequisites"

PREREQUISITES_OK=true

# Check Python
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python 3 found: $PYTHON_VERSION"
else
    print_error "Python 3 not found"
    print_info "Install Python 3.11 or higher from https://www.python.org/downloads/"
    PREREQUISITES_OK=false
fi

# Check Node.js
if command_exists node; then
    NODE_VERSION=$(node --version)
    print_success "Node.js found: $NODE_VERSION"
else
    print_error "Node.js not found"
    print_info "Install Node.js 18 or higher from https://nodejs.org/"
    PREREQUISITES_OK=false
fi

# Check npm
if command_exists npm; then
    NPM_VERSION=$(npm --version)
    print_success "npm found: v$NPM_VERSION"
else
    print_error "npm not found"
    print_info "npm should be installed with Node.js"
    PREREQUISITES_OK=false
fi

# Check Git
if command_exists git; then
    GIT_VERSION=$(git --version | cut -d' ' -f3)
    print_success "Git found: $GIT_VERSION"
else
    print_error "Git not found"
    print_info "Install Git from https://git-scm.com/downloads"
    PREREQUISITES_OK=false
fi

# Check PostgreSQL (optional)
if command_exists psql; then
    PSQL_VERSION=$(psql --version | cut -d' ' -f3)
    print_success "PostgreSQL found: $PSQL_VERSION"
else
    print_warning "PostgreSQL not found (optional for production)"
    print_info "For production, install PostgreSQL from https://www.postgresql.org/download/"
fi

# Check Redis (optional)
if command_exists redis-server; then
    print_success "Redis found"
else
    print_warning "Redis not found (optional, improves performance)"
    print_info "Install Redis from https://redis.io/download"
fi

if [ "$PREREQUISITES_OK" = false ]; then
    echo ""
    print_error "Some prerequisites are missing. Please install them and run this script again."
    exit 1
fi

echo ""
print_success "All required prerequisites are installed!"

# Step 2: Backend setup
print_step "Step 2: Setting Up Backend"

cd "$PROJECT_ROOT/backend"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_info "Creating Python virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_success "Virtual environment already exists"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    print_success "Virtual environment activated"
elif [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
    print_success "Virtual environment activated"
else
    print_error "Could not find virtual environment activation script"
    exit 1
fi

# Install Python dependencies
print_info "Installing Python dependencies (this may take a few minutes)..."
if pip install --upgrade pip > /dev/null 2>&1; then
    print_success "pip upgraded"
fi

if pip install -r requirements.txt > /dev/null 2>&1; then
    print_success "Python dependencies installed"
else
    print_error "Failed to install Python dependencies"
    print_info "Try running: pip install -r backend/requirements.txt"
    exit 1
fi

# Setup environment variables
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        print_info "Creating .env file from .env.example..."
        cp .env.example .env
        print_success ".env file created"
        print_warning "IMPORTANT: Edit backend/.env and update the SECRET_KEY and other settings!"
    else
        print_warning ".env.example not found. You'll need to create .env manually"
    fi
else
    print_success ".env file already exists"
fi

cd "$PROJECT_ROOT"

# Step 3: Frontend setup
print_step "Step 3: Setting Up Frontend"

cd "$PROJECT_ROOT/frontend"

# Install Node.js dependencies
print_info "Installing Node.js dependencies (this may take a few minutes)..."
if npm install > /dev/null 2>&1; then
    print_success "Node.js dependencies installed"
else
    print_error "Failed to install Node.js dependencies"
    print_info "Try running: cd frontend && npm install"
    exit 1
fi

# Setup environment variables
if [ ! -f ".env.local" ]; then
    if [ -f ".env.example" ]; then
        print_info "Creating .env.local file from .env.example..."
        cp .env.example .env.local
        print_success ".env.local file created"
    else
        print_warning ".env.example not found. You'll need to create .env.local manually"
    fi
else
    print_success ".env.local file already exists"
fi

cd "$PROJECT_ROOT"

# Step 4: Database setup
print_step "Step 4: Database Setup"

print_info "For development, SQLite will be used by default."
print_info "For production, you should use PostgreSQL."
echo ""

if command_exists psql; then
    read -p "Do you want to set up PostgreSQL now? (y/N): " setup_postgres
    if [[ $setup_postgres =~ ^[Yy]$ ]]; then
        print_info "To set up PostgreSQL:"
        echo "  1. Create a database: createdb buildintel"
        echo "  2. Update DATABASE_URL in backend/.env"
        echo "  3. Run migrations: cd backend && alembic upgrade head"
        echo ""
        read -p "Press Enter to continue after setting up PostgreSQL..."
    fi
fi

# Run migrations
print_info "Running database migrations..."
cd "$PROJECT_ROOT/backend"

if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
fi

if command_exists alembic; then
    if alembic upgrade head > /dev/null 2>&1; then
        print_success "Database migrations completed"
    else
        print_warning "Database migrations failed (this is OK if database doesn't exist yet)"
        print_info "You can run migrations later with: cd backend && alembic upgrade head"
    fi
else
    print_warning "Alembic not found. Migrations not run."
fi

cd "$PROJECT_ROOT"

# Step 5: Verification
print_step "Step 5: Verifying Installation"

print_info "Running database verification..."
cd "$PROJECT_ROOT/backend"

if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
fi

if python scripts/verify_database.py > /dev/null 2>&1; then
    print_success "Database verification passed"
else
    print_warning "Database verification had issues (check database setup)"
fi

cd "$PROJECT_ROOT"

# Final summary
echo ""
echo -e "${CYAN}============================================================${NC}"
echo -e "${CYAN}  ✨ Setup Complete!${NC}"
echo -e "${CYAN}============================================================${NC}"
echo ""
print_success "BuildIntel Pro is ready to run!"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo ""
echo "1. ${CYAN}Configure Environment Variables${NC}"
echo "   Edit backend/.env and update:"
echo "   - SECRET_KEY (generate a secure random key)"
echo "   - DATABASE_URL (if using PostgreSQL)"
echo "   - OPENAI_API_KEY (if using AI features)"
echo ""
echo "2. ${CYAN}Start the Backend${NC}"
echo "   Open a terminal and run:"
echo "   ${GREEN}cd backend${NC}"
echo "   ${GREEN}source venv/bin/activate${NC}  # On Windows: venv\\Scripts\\activate"
echo "   ${GREEN}uvicorn app.main:app --reload${NC}"
echo ""
echo "3. ${CYAN}Start the Frontend${NC}"
echo "   Open another terminal and run:"
echo "   ${GREEN}cd frontend${NC}"
echo "   ${GREEN}npm run dev${NC}"
echo ""
echo "4. ${CYAN}Access the Application${NC}"
echo "   Frontend: ${GREEN}http://localhost:3000${NC}"
echo "   Backend API: ${GREEN}http://localhost:8000${NC}"
echo "   API Docs: ${GREEN}http://localhost:8000/api/docs${NC}"
echo ""
echo -e "${CYAN}──────────────────────────────────────────────────────────────${NC}"
echo ""
echo "📖 Documentation:"
echo "   - Admin Guide: docs/ADMIN_USER_GUIDE.md"
echo "   - Customer Guide: docs/CUSTOMER_USER_GUIDE.md"
echo "   - API Guide: docs/API_INTEGRATION_GUIDE.md"
echo "   - Production Checklist: docs/PRODUCTION_CHECKLIST.md"
echo ""
echo "🧪 Testing:"
echo "   - Backend tests: ${GREEN}python backend/tests/test_backend.py${NC}"
echo "   - Connection test: ${GREEN}./test-frontend-backend.sh${NC}"
echo "   - Database verification: ${GREEN}python backend/scripts/verify_database.py${NC}"
echo ""
echo "🆘 Need Help?"
echo "   - Email: dev@poorduceholdings.com"
echo "   - Documentation: See docs/ directory"
echo ""
echo -e "${CYAN}============================================================${NC}"
echo ""
print_success "Happy building with BuildIntel Pro! 🚀"
echo ""
