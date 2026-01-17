#!/bin/bash
# Quick Deploy Script for Construction Intelligence Platform
# This script helps automate the deployment process

set -e  # Exit on error

echo "=========================================="
echo "Construction Intelligence Platform"
echo "Quick Deploy Helper"
echo "=========================================="
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo -e "${RED}This script is designed for Linux (Xubuntu). Current OS: $OSTYPE${NC}"
    exit 1
fi

echo "Step 1: Checking prerequisites..."
echo ""

# Check Git
if command -v git &> /dev/null; then
    echo -e "${GREEN}✓${NC} Git installed: $(git --version)"
else
    echo -e "${RED}✗${NC} Git not found. Installing..."
    sudo apt-get update && sudo apt-get install -y git
fi

# Check Docker
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✓${NC} Docker installed: $(docker --version)"
else
    echo -e "${YELLOW}!${NC} Docker not found. Would you like to install it? (y/n)"
    read -r install_docker
    if [[ "$install_docker" == "y" ]]; then
        sudo apt-get update
        sudo apt-get install -y docker.io docker-compose
        sudo usermod -aG docker $USER
        echo -e "${GREEN}Docker installed. Please log out and back in for group changes to take effect.${NC}"
    fi
fi

# Check Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓${NC} Node.js installed: $NODE_VERSION"
    
    # Check if version is 18+
    MAJOR_VERSION=$(echo $NODE_VERSION | cut -d'.' -f1 | sed 's/v//')
    if [ "$MAJOR_VERSION" -lt 18 ]; then
        echo -e "${YELLOW}! Node.js version is < 18. Recommended: 20+${NC}"
    fi
else
    echo -e "${YELLOW}!${NC} Node.js not found. Installing Node.js 20..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓${NC} Python installed: $PYTHON_VERSION"
else
    echo -e "${YELLOW}!${NC} Python not found. Installing Python 3.11..."
    sudo apt-get install -y python3.11 python3.11-venv python3-pip
fi

echo ""
echo "=========================================="
echo "Step 2: Cloud Services Setup"
echo "=========================================="
echo ""
echo "You'll need to create accounts on these services:"
echo ""
echo "1. Railway (Backend hosting): https://railway.app"
echo "   - Sign up with GitHub"
echo "   - Get $5/month free credit"
echo ""
echo "2. Vercel (Frontend hosting): https://vercel.com"
echo "   - Sign up with GitHub"
echo "   - 100% free for personal projects"
echo ""
echo "3. Supabase (PostgreSQL): https://supabase.com"
echo "   - Sign up (email or GitHub)"
echo "   - Free tier: 500MB database"
echo ""
echo "4. Upstash (Redis): https://upstash.com"
echo "   - Sign up (email or GitHub)"
echo "   - Free tier: 10K commands/day"
echo ""
echo "Have you created these accounts? (y/n)"
read -r accounts_created

if [[ "$accounts_created" != "y" ]]; then
    echo -e "${YELLOW}Please create accounts first, then run this script again.${NC}"
    exit 0
fi

echo ""
echo "=========================================="
echo "Step 3: Environment Configuration"
echo "=========================================="
echo ""
echo "Let's configure your environment variables..."
echo ""

# Backend configuration
echo "--- Backend Configuration ---"
echo ""
echo "Enter your Supabase PostgreSQL connection URL:"
echo "(Format: postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres)"
read -r database_url

echo ""
echo "Enter your Upstash Redis connection URL:"
echo "(Format: redis://default:[PASSWORD]@[HOST]:[PORT])"
read -r redis_url

echo ""
echo "Generate a random SECRET_KEY (32+ characters)? (y/n)"
read -r gen_secret
if [[ "$gen_secret" == "y" ]]; then
    secret_key=$(openssl rand -base64 32)
    echo "Generated SECRET_KEY: $secret_key"
else
    echo "Enter your SECRET_KEY:"
    read -r secret_key
fi

echo ""
echo "Enter your frontend domain (or leave blank for now):"
echo "(e.g., https://your-app.vercel.app)"
read -r frontend_url

if [[ -z "$frontend_url" ]]; then
    cors_origins="http://localhost:3000,http://localhost:5173"
else
    cors_origins="http://localhost:3000,http://localhost:5173,$frontend_url"
fi

# Create backend .env
cat > backend/.env << EOF
# Database
DATABASE_URL=$database_url

# Redis
REDIS_URL=$redis_url

# Application
SECRET_KEY=$secret_key
ENVIRONMENT=production
DEBUG=False

# CORS
CORS_ORIGINS=$cors_origins

# Optional: OpenAI (leave blank if not using)
OPENAI_API_KEY=

# Application Settings
APP_NAME=BuildIntel Pro
APP_VERSION=1.0.0
API_V1_PREFIX=/api/v1
EOF

echo -e "${GREEN}✓${NC} Created backend/.env"

# Frontend configuration
echo ""
echo "--- Frontend Configuration ---"
echo ""
echo "Enter your backend API URL (or leave blank for now):"
echo "(e.g., https://your-backend.up.railway.app)"
read -r backend_url

if [[ -z "$backend_url" ]]; then
    backend_url="http://localhost:8001"
fi

cat > frontend/.env << EOF
VITE_API_URL=$backend_url
EOF

echo -e "${GREEN}✓${NC} Created frontend/.env"

echo ""
echo "=========================================="
echo "Step 4: Local Testing"
echo "=========================================="
echo ""
echo "Would you like to test the application locally with Docker? (y/n)"
read -r test_local

if [[ "$test_local" == "y" ]]; then
    echo "Starting Docker Compose..."
    
    # Create docker-compose.yml if it doesn't exist
    if [ ! -f docker-compose.yml ]; then
        cat > docker-compose.yml << 'EOFCOMPOSE'
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: buildintel_user
      POSTGRES_PASSWORD: buildintel_pass
      POSTGRES_DB: buildintel_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  backend:
    build: ./backend
    ports:
      - "8001:8001"
    environment:
      - DATABASE_URL=postgresql://buildintel_user:buildintel_pass@postgres:5432/buildintel_db
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis
    command: uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - VITE_API_URL=http://localhost:8001
    command: yarn dev --host 0.0.0.0 --port 3000

volumes:
  postgres_data:
EOFCOMPOSE
        echo -e "${GREEN}✓${NC} Created docker-compose.yml"
    fi
    
    docker-compose up -d
    
    echo ""
    echo "Waiting for services to start..."
    sleep 10
    
    echo ""
    echo "Initializing database..."
    docker-compose exec backend python ../scripts/setup_db.py
    docker-compose exec backend python ../scripts/seed_data.py
    
    echo ""
    echo -e "${GREEN}✓${NC} Local test environment is running!"
    echo ""
    echo "Access your application at:"
    echo "  Frontend: http://localhost:3000"
    echo "  Backend: http://localhost:8001"
    echo "  API Docs: http://localhost:8001/api/docs"
    echo ""
    echo "To stop: docker-compose down"
fi

echo ""
echo "=========================================="
echo "Step 5: Git Repository Setup"
echo "=========================================="
echo ""
echo "Is your code already pushed to GitHub? (y/n)"
read -r git_ready

if [[ "$git_ready" != "y" ]]; then
    echo ""
    echo "Let's set up your Git repository..."
    echo ""
    echo "Enter your GitHub username:"
    read -r github_user
    
    echo "Enter your repository name (e.g., construction-intelligence):"
    read -r repo_name
    
    # Initialize git if not already
    if [ ! -d .git ]; then
        git init
        echo -e "${GREEN}✓${NC} Initialized Git repository"
    fi
    
    # Add gitignore
    cat > .gitignore << 'EOFIGNORE'
# Environment files
.env
.env.*
!.env.example

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
ENV/
.venv

# Node
node_modules/
dist/
build/
.cache/

# Database
*.db
*.sqlite
*.sqlite3

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/
EOFIGNORE
    
    git add .
    git commit -m "Initial commit: Construction Intelligence Platform"
    
    echo ""
    echo "Create a repository on GitHub:"
    echo "  Go to: https://github.com/new"
    echo "  Name: $repo_name"
    echo "  Make it PRIVATE (recommended)"
    echo ""
    echo "Press Enter after you've created the repository..."
    read -r

    git remote add origin "https://github.com/$github_user/$repo_name.git"
    git branch -M main
    git push -u origin main
    
    echo -e "${GREEN}✓${NC} Code pushed to GitHub"
fi

echo ""
echo "=========================================="
echo "Step 6: Railway Deployment"
echo "=========================================="
echo ""
echo "To deploy your backend to Railway:"
echo ""
echo "1. Go to: https://railway.app/new"
echo "2. Click 'Deploy from GitHub repo'"
echo "3. Select your repository"
echo "4. Select 'backend' as root directory"
echo "5. Add these environment variables:"
echo "   - DATABASE_URL (from Supabase)"
echo "   - REDIS_URL (from Upstash)"
echo "   - SECRET_KEY"
echo "   - ENVIRONMENT=production"
echo "   - DEBUG=False"
echo "   - CORS_ORIGINS (include your frontend domain)"
echo ""
echo "6. After deployment, copy your Railway URL"
echo ""
echo "Have you deployed to Railway? (y/n)"
read -r railway_deployed

if [[ "$railway_deployed" == "y" ]]; then
    echo "Enter your Railway backend URL:"
    read -r railway_url
    
    # Update frontend .env
    sed -i "s|VITE_API_URL=.*|VITE_API_URL=$railway_url|" frontend/.env
    echo -e "${GREEN}✓${NC} Updated frontend/.env with Railway URL"
fi

echo ""
echo "=========================================="
echo "Step 7: Vercel Deployment"
echo "=========================================="
echo ""
echo "To deploy your frontend to Vercel:"
echo ""
echo "1. Install Vercel CLI:"
echo "   npm install -g vercel"
echo ""
echo "2. Deploy:"
echo "   cd frontend"
echo "   vercel login"
echo "   vercel --prod"
echo ""
echo "3. Set environment variable in Vercel dashboard:"
echo "   VITE_API_URL=$railway_url"
echo ""
echo "Would you like to install Vercel CLI now? (y/n)"
read -r install_vercel

if [[ "$install_vercel" == "y" ]]; then
    sudo npm install -g vercel
    echo -e "${GREEN}✓${NC} Vercel CLI installed"
    echo ""
    echo "Run these commands to deploy:"
    echo "  cd frontend"
    echo "  vercel login"
    echo "  vercel --prod"
fi

echo ""
echo "=========================================="
echo "Step 8: Database Initialization"
echo "=========================================="
echo ""
echo "Initialize your production database? (y/n)"
read -r init_db

if [[ "$init_db" == "y" ]]; then
    echo "Initializing database..."
    
    # Export DATABASE_URL for scripts
    export DATABASE_URL="$database_url"
    
    python3 scripts/setup_db.py
    python3 scripts/seed_data.py
    
    echo -e "${GREEN}✓${NC} Database initialized with sample data"
fi

echo ""
echo "=========================================="
echo "🎉 DEPLOYMENT COMPLETE!"
echo "=========================================="
echo ""
echo "Your application is now deployed!"
echo ""
echo "Next steps:"
echo ""
echo "1. Test your production app:"
if [[ -n "$railway_url" ]]; then
    echo "   Backend: $railway_url/health"
    echo "   API Docs: $railway_url/api/docs"
fi
echo ""
echo "2. Set up monitoring:"
echo "   - UptimeRobot: https://uptimerobot.com"
echo "   - Add your /health endpoint"
echo ""
echo "3. Configure custom domain (optional):"
echo "   - Buy domain from Namecheap/Google"
echo "   - Configure DNS in Railway/Vercel"
echo ""
echo "4. Future deployments:"
echo "   Just run: git push"
echo "   Auto-deploys to production!"
echo ""
echo "Login credentials:"
echo "  Email: demo@example.com"
echo "  Password: demo123"
echo ""
echo "Documentation:"
echo "  - Full guide: /app/DEPLOYMENT_GUIDE_SOLO_OPERATOR.md"
echo "  - App docs: /app/README.md"
echo ""
echo "Need help? Check the deployment guide for troubleshooting."
echo ""
