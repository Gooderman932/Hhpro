# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Using Docker with Makefile (Recommended)

1. **Clone and navigate to the project:**
   ```bash
   git clone https://github.com/Gooderman932/market-data.git
   cd market-data
   ```

2. **Initial setup (creates .env if needed):**
   ```bash
   make setup
   ```

3. **Start all services:**
   ```bash
   make dev
   ```
   This automatically starts PostgreSQL, Redis, backend, and frontend with hot-reload enabled.

4. **Initialize the database** (in a new terminal):
   ```bash
   docker-compose exec backend python ../scripts/setup_db.py
   docker-compose exec backend python ../scripts/seed_data.py
   ```

5. **Access the application:**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

6. **Login with demo credentials:**
   - Email: `demo@example.com`
   - Password: `demo123`

### Alternative: Traditional Docker Commands

If you prefer not to use Make:
```bash
docker-compose up -d
docker-compose exec backend python ../scripts/setup_db.py
docker-compose exec backend python ../scripts/seed_data.py
```

### Manual Setup (Without Docker)

#### Backend

```bash
# Install Python dependencies
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up PostgreSQL database
createdb construction_intel

# Configure environment
export DATABASE_URL="postgresql://user:password@localhost:5432/construction_intel"
export SECRET_KEY="your-secret-key-here"

# Initialize database
python ../scripts/setup_db.py
python ../scripts/seed_data.py

# Start the backend
uvicorn app.main:app --reload
```

#### Frontend

```bash
# Install Node.js dependencies
cd frontend
npm install

# Start the development server
npm run dev
```

## 🎯 What to Try First

1. **Dashboard**: View project metrics and recent opportunities
2. **Opportunities**: Browse and filter construction projects
3. **Analytics**: Explore sector distribution and regional analysis
4. **Competitors**: Analyze competitor activity and win rates
5. **Forecasting**: View demand predictions and scenario analysis

## 📱 Main Features

### Project Management
- Create, update, and track construction projects
- Filter by sector, status, location, and value
- Import data from various sources

### Analytics & Intelligence
- Real-time market insights
- Competitor tracking and analysis
- Regional distribution and trends
- Win rate calculations

### AI/ML Capabilities
- Opportunity scoring
- Win probability predictions
- Demand forecasting
- Entity extraction from text

## 🔧 API Usage

### Authentication
```bash
# Get access token
curl -X POST http://localhost:8000/api/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=demo@example.com&password=demo123"

# Use token in subsequent requests
curl -X GET http://localhost:8000/api/projects/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Creating a Project
```bash
curl -X POST http://localhost:8000/api/projects/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Office Building",
    "project_type": "opportunity",
    "sector": "Commercial",
    "value": 5000000,
    "city": "San Francisco",
    "state": "CA",
    "status": "active"
  }'
```

## 🛠️ Development

### Using Makefile Commands (Recommended)

The project includes a comprehensive Makefile with 40+ commands. Run `make help` to see all available commands.

**Common commands:**
```bash
# Development environment
make dev            # Start development environment
make dev-logs       # View logs from all services
make dev-stop       # Stop development environment
make dev-restart    # Restart all services

# Testing
make test           # Run all tests (backend + frontend)
make test-backend   # Run backend tests with pytest
make test-frontend  # Run frontend build test
make test-coverage  # Generate test coverage report

# Code quality
make lint           # Run all linters (Python + TypeScript)
make format         # Auto-format all code
make ci             # Run full CI checks locally

# Database
make migrate        # Run database migrations
make db-reset       # Reset database (destroys all data!)

# Docker
make build          # Build Docker images
make logs           # Show logs from all services
make ps             # Show running containers
```

### Running Tests Manually
```bash
# Backend tests
cd backend
pytest tests/ -v --cov=app

# Frontend tests
cd frontend
npm run build  # Build test
npm run lint   # ESLint check
```

### Code Quality
```bash
# Backend linting (or use: make lint-backend)
cd backend
flake8 app/
black --check app/
mypy app/ --ignore-missing-imports

# Frontend linting (or use: make lint-frontend)
cd frontend
npm run lint
```

## 📚 Next Steps

- Review the [full README](README.md) for detailed documentation
- Check [CI/CD Documentation](docs/CICD.md) for automated workflows
- See [Developer Guide](docs/DEVELOPER.md) for local development setup
- Read [Deployment Guide](docs/DEPLOYMENT.md) for production deployment
- Explore API endpoints at http://localhost:8000/docs
- Check out the [data schemas](data/schemas/) for data format reference
- Review [sample data](data/seeds/) for examples

## 🔄 CI/CD Pipeline

The project includes automated GitHub Actions workflows for:
- **Continuous Integration**: Automated testing and linting on every push
- **Security Scanning**: Weekly vulnerability scans with CodeQL and Trivy
- **Docker Builds**: Automated image builds and publishing to GHCR
- **Deployments**: Multi-environment deployment workflows
- **Automation**: Daily scheduled platform management tasks

See [docs/CICD.md](docs/CICD.md) for complete workflow documentation.

## 🆘 Troubleshooting

### Using Helper Scripts

The project includes helper scripts for common tasks:
```bash
# Check service health
./scripts/health_check.sh

# Create database backup
./scripts/backup_database.sh

# Deploy to environment
./scripts/deploy.sh staging
```

### Port Already in Use
```bash
# Change ports in docker-compose.yml or stop conflicting services
lsof -i :8000  # Check what's using port 8000
lsof -i :5173  # Check what's using port 5173

# Or use Make to stop services
make dev-stop
```

### Database Connection Issues
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# View logs
make logs-db
# Or: docker-compose logs postgres

# Reset database if needed
make db-reset  # WARNING: Destroys all data!
```

### Frontend Build Issues
```bash
# Using Make
make clean  # Cleans all caches

# Or manually
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### View All Available Commands
```bash
make help  # Shows all 40+ Makefile commands
```

## 💡 Tips

- Use the API documentation at `/docs` to explore all endpoints
- The demo account has full access to all features
- Sample data includes 30 projects across multiple sectors
- All endpoints support pagination with `skip` and `limit` parameters
- Use filters to narrow down results by sector, status, location, etc.

---

Happy building! 🏗️
