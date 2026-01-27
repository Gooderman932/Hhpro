#!/bin/bash
# Quick Setup Script for Construction Intelligence Platform

echo "==================================="
echo "Construction Intelligence Platform"
echo "Quick Setup Script"
echo "==================================="

# Install system dependencies if needed
echo "Step 1: Installing system dependencies..."
apt-get update -qq
apt-get install -y -qq postgresql-15 postgresql-contrib-15 redis-server > /dev/null 2>&1

# Start services
echo "Step 2: Starting PostgreSQL and Redis..."
service postgresql start
service redis-server start

# Wait for services to be ready
sleep 3

# Create database and user
echo "Step 3: Setting up database..."
sudo -u postgres psql -c "CREATE USER buildintel_user WITH PASSWORD 'buildintel_pass';" 2>/dev/null || echo "User already exists"
sudo -u postgres psql -c "CREATE DATABASE buildintel_db OWNER buildintel_user;" 2>/dev/null || echo "Database already exists"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE buildintel_db TO buildintel_user;"

# Install Python dependencies
echo "Step 4: Installing Python dependencies..."
cd /app/backend
pip install -q -r requirements.txt

# Install Node dependencies
echo "Step 5: Installing Node dependencies..."
cd /app/frontend
yarn install --silent

# Initialize database
echo "Step 6: Initializing database schema..."
cd /app
python scripts/setup_db.py

# Seed database
echo "Step 7: Seeding database with sample data..."
python scripts/seed_data.py

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "Login Credentials:"
echo "  Email: demo@example.com"
echo "  Password: demo123"
echo ""
echo "To start the application:"
echo "  sudo supervisorctl restart all"
echo ""
echo "Access the application at:"
echo "  https://market-data-migrate.preview.emergentagent.com"
echo "=========================================="
