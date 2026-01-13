# Construction Intelligence Platform - Setup Guide

Complete guide to set up and configure your Construction Intelligence Platform.

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- **Docker & Docker Compose** (recommended) OR
- **Python 3.11+** and **Node.js 20+** (for local development)
- **PostgreSQL 16+** (if running without Docker)
- **Redis 7+** (for caching)
- **OpenAI API key** (optional, for ML features)

### Quickest Setup (Using Make + Docker)

```bash
# Clone the repository
git clone https://github.com/Gooderman932/market-data.git
cd market-data

# Setup environment (creates .env if needed)
make setup

# Start all services (PostgreSQL, Redis, Backend, Frontend)
make dev

# Initialize database (in a new terminal)
docker-compose exec backend python ../scripts/setup_db.py
docker-compose exec backend python ../scripts/seed_data.py

# Access the application
# Frontend: http://localhost:5173
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

**Login credentials:**
- Email: `demo@example.com`
- Password: `demo123`

### All Available Commands

Run `make help` to see all 40+ available commands. Key commands:

```bash
# Development
make dev              # Start development environment
make dev-logs         # View logs
make dev-stop         # Stop environment
make dev-restart      # Restart environment

# Testing
make test             # Run all tests
make test-coverage    # Generate coverage report
make ci               # Run CI checks locally

# Code Quality
make lint             # Run all linters
make format           # Auto-format code

# Database
make migrate          # Run migrations
make migrate-create   # Create new migration
make db-reset         # Reset database

# Deployment
make deploy-staging   # Deploy to staging
make deploy-prod      # Deploy to production
```

**Generate SECRET_KEY:**
```python
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 3: Setup Database

```bash
# Create PostgreSQL database
createdb buildintel_db

# Or using psql:
psql -U postgres
CREATE DATABASE buildintel_db;
\q

# Run database migrations
alembic upgrade head

# Optional: Seed with sample data
python scripts/seed_data.py
```

### Step 4: Start Backend

```bash
# Development mode (with auto-reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

**Test it works:**
- Open http://localhost:8000 - Should see API info
- Open http://localhost:8000/health - Should return `{"status": "healthy"}`
- Open http://localhost:8000/api/docs - Swagger UI

---

## 🔧 Detailed Configuration

### Database Setup (PostgreSQL)

**Option 1: Local PostgreSQL**
```bash
# Install PostgreSQL
# macOS:
brew install postgresql@14
brew services start postgresql@14

# Ubuntu/Debian:
sudo apt-get install postgresql-14

# Create user and database
sudo -u postgres psql
CREATE USER buildintel_user WITH PASSWORD 'your_secure_password';
CREATE DATABASE buildintel_db OWNER buildintel_user;
GRANT ALL PRIVILEGES ON DATABASE buildintel_db TO buildintel_user;
\q
```

**Option 2: Docker PostgreSQL**
```bash
docker run --name buildintel-postgres \
  -e POSTGRES_DB=buildintel_db \
  -e POSTGRES_USER=buildintel_user \
  -e POSTGRES_PASSWORD=your_password \
  -p 5432:5432 \
  -d postgres:14
```

**Option 3: Cloud Database**
- AWS RDS: Use connection string from RDS console
- Google Cloud SQL: Use cloud-sql-proxy
- Heroku Postgres: Use DATABASE_URL from config vars
- Supabase: Use connection string from project settings

### Redis Setup

**Option 1: Local Redis**
```bash
# macOS:
brew install redis
brew services start redis

# Ubuntu/Debian:
sudo apt-get install redis-server
sudo systemctl start redis
```

**Option 2: Docker Redis**
```bash
docker run --name buildintel-redis \
  -p 6379:6379 \
  -d redis:7
```

**Option 3: Cloud Redis**
- Redis Labs (free tier available)
- AWS ElastiCache
- Google Cloud Memorystore
- Heroku Redis

### OpenAI API Setup

1. **Get API Key:**
   - Go to https://platform.openai.com/api-keys
   - Create new secret key
   - Copy to `.env` as `OPENAI_API_KEY`

2. **Set Usage Limits:**
   - Set monthly budget limit in OpenAI dashboard
   - Monitor usage at https://platform.openai.com/usage

3. **Cost Optimization:**
   ```bash
   # Use GPT-4o-mini for cheaper operations
   OPENAI_MODEL="gpt-4o-mini"
   
   # Disable LLM by default, use on-demand
   ML_USE_LLM_BY_DEFAULT=false
   ```

**Estimated Costs:**
- Entity extraction (LLM): ~$0.01-0.03 per document
- Classification (LLM): ~$0.01 per project
- Embeddings: ~$0.0001 per project
- Monthly for 10,000 projects: ~$50-100

---

## 📊 Running with Docker Compose

**Using Make (Recommended):**

```bash
# Start all services (PostgreSQL, Redis, Backend, Frontend)
make dev

# View logs from all services
make dev-logs

# View logs from specific service
make logs-backend
make logs-frontend
make logs-db

# Stop all services
make dev-stop

# Restart services
make dev-restart

# Check running containers
make ps
```

**Without Make (Traditional Method):**

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

### Production Docker Configuration

For production deployments, use the production docker-compose:

```bash
# Build production images
make build-prod
# Or: docker-compose -f docker-compose.prod.yml build

# Start production services
docker-compose -f docker-compose.prod.yml up -d

# Production images use:
# - Multi-stage builds for optimization
# - Non-root users for security
# - Health checks for monitoring
# - Resource limits
# - Nginx with security headers (frontend)
```

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for complete production deployment guide.

---

## 🧪 Testing the Setup

### Using Helper Scripts

```bash
# Comprehensive health check of all services
./scripts/health_check.sh

# Create database backup
./scripts/backup_database.sh
```

### Using Makefile

```bash
# Check service health
make health

# Run all tests
make test

# Run tests with coverage
make test-coverage
```

### Manual Health Checks

#### 1. Backend Health Check
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy","version":"0.1.0","environment":"development"}
```

#### 2. Database Connection
```bash
python -c "
from app.database import engine
from sqlalchemy import text
with engine.connect() as conn:
    result = conn.execute(text('SELECT 1'))
    print('Database connected:', result.fetchone())
"
```

#### 3. Redis Connection
```bash
python -c "
import redis
r = redis.from_url('redis://localhost:6379/0')
r.set('test', 'hello')
print('Redis connected:', r.get('test'))
"
```

#### 4. Docker Services Status
```bash
# Using Make
make ps

# Or directly
docker-compose ps
```

---

## 🔐 Security Configuration

### Production Checklist

**Required for Production:**

1. **Change SECRET_KEY:**
   ```bash
   # Generate strong secret
   python -c "import secrets; print(secrets.token_urlsafe(64))"
   ```

2. **Enable HTTPS:**
   ```bash
   SESSION_COOKIE_SECURE=true
   CORS_ORIGINS="https://app.yourcompany.com"
   ```

3. **Secure Database:**
   ```bash
   DATABASE_URL="postgresql://user:password@host:5432/db?sslmode=require"
   ```

4. **Disable Debug Mode:**
   ```bash
   DEBUG=false
   ENVIRONMENT="production"
   ```

5. **Set Up Monitoring:**
   ```bash
   # Get Sentry DSN from sentry.io
   SENTRY_DSN="https://your-dsn@sentry.io/project-id"
   ```

---

## 🎯 Feature Configuration

### Enable/Disable ML Features

Control which ML services are active:

```bash
# Enable all ML features (costs API credits)
ENABLE_WIN_PROBABILITY=true
ENABLE_DEMAND_FORECAST=true
ENABLE_ENTITY_EXTRACTION=true
ENABLE_PROJECT_CLASSIFICATION=true
ENABLE_SEMANTIC_SEARCH=true

# Cost optimization: disable expensive features
ENABLE_ENTITY_EXTRACTION=false  # If not using document processing
ML_USE_LLM_BY_DEFAULT=false     # Use ML models instead of LLM
```

### Subscription Tier Limits

Configure limits per tier:

```bash
# Free tier
MAX_PROJECTS_PER_TENANT_FREE=100

# Professional tier ($499/mo)
MAX_PROJECTS_PER_TENANT_PRO=1000

# Enterprise tier (unlimited)
MAX_PROJECTS_PER_TENANT_ENTERPRISE=0
```

### API Credits Pricing

Configure credit costs:

```bash
# Lower costs for development
CREDIT_COST_CLASSIFICATION_LLM=5  # Instead of 10
CREDIT_COST_WIN_PROBABILITY=5     # Instead of 10

# Or make some features free
CREDIT_COST_CLASSIFICATION_RULE=0
CREDIT_COST_CLASSIFICATION_ML=0
```

---

## 📈 Performance Tuning

### Database Optimization

```bash
# Increase connection pool for high traffic
DATABASE_POOL_SIZE=50
DATABASE_MAX_OVERFLOW=100
```

**PostgreSQL Settings** (`postgresql.conf`):
```ini
max_connections = 200
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 16MB
```

### Redis Caching

```bash
# Increase cache TTL for stable data
CACHE_TTL=7200  # 2 hours instead of 1

# Use Redis for session storage (faster than database)
```

### ML Model Performance

```bash
# Batch processing for efficiency
ML_BATCH_SIZE=200  # Process 200 projects at once

# Pre-generate embeddings in background
# (Add to cron job)
python scripts/generate_embeddings.py --batch-size 1000
```

---

## 🐳 Docker Configuration

Create `docker-compose.yml` in root:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: buildintel_db
      POSTGRES_USER: buildintel_user
      POSTGRES_PASSWORD: your_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://buildintel_user:your_password@postgres:5432/buildintel_db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - postgres
      - redis
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

volumes:
  postgres_data:
  redis_data:
```

---

## 🔄 Migrations

### Using Makefile (Recommended)

```bash
# Run all pending migrations
make migrate

# Create a new migration
make migrate-create msg="add user preferences table"

# Rollback last migration
make migrate-rollback

# View migration history
make migrate-history

# Check current migration
make migrate-current
```

### Manual Migration Commands

```bash
# After modifying models, create migration
cd backend
alembic revision --autogenerate -m "Add new field to projects"

# Review the generated migration file
# Edit if needed: alembic/versions/xxx_add_new_field.py

# Apply migration
alembic upgrade head

# Rollback one version
alembic downgrade -1

# Rollback to specific version
alembic downgrade abc123

# Rollback all
alembic downgrade base
```

### CI/CD Migration Workflow

Migrations can also be run via GitHub Actions:

```bash
# Using GitHub CLI
gh workflow run migrations.yml \
  -f environment=staging \
  -f action=upgrade \
  -f dry_run=true  # Test first

# After verifying dry run
gh workflow run migrations.yml \
  -f environment=staging \
  -f action=upgrade \
  -f dry_run=false
```

See [docs/CICD.md](docs/CICD.md) for more on automated migrations.

---

## 🎓 Training ML Models

### Win Probability Model

```bash
# Prepare training data from historical bids
python scripts/train_win_probability.py

# Model saved to: ./models/win_probability_v1.joblib
```

**Requirements:**
- Minimum 500 historical bids with outcomes
- 2,000+ bids recommended for 80%+ accuracy

### Demand Forecast Model

```bash
# Train on historical project data
python scripts/train_demand_forecast.py --country USA --periods 12

# Model saved to: ./models/demand_forecast_v1.joblib
```

**Requirements:**
- 2+ years of historical data
- Data from multiple regions/sectors

---

## 🚨 Troubleshooting

### Using Helper Scripts

```bash
# Comprehensive health check
./scripts/health_check.sh

# Check specific service logs
make logs-backend
make logs-frontend
make logs-db
```

### Database Connection Errors

```bash
# Check PostgreSQL is running
pg_isready -h localhost -p 5432
# Or with Docker: docker-compose ps postgres

# Test connection
psql -U user -d construction_intel -h localhost
# Or with Make: make db-shell

# Check DATABASE_URL format
echo $DATABASE_URL

# Reset database if needed
make db-reset  # WARNING: Destroys all data!
```

### Redis Connection Errors

```bash
# Check Redis is running
redis-cli ping
# Should return: PONG

# Test connection
redis-cli -h localhost -p 6379

# View Redis logs
make logs  # Shows all service logs including Redis
```

### Docker Issues

```bash
# Clean up Docker resources
make clean

# Rebuild containers
make build

# View container status
make ps

# Restart all services
make dev-restart
```

### Import Errors

```bash
# Ensure virtual environment is activated
which python  # Should show venv path

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Or rebuild Docker containers
make build
```

### Pre-commit Hook Issues

```bash
# Install pre-commit hooks
make install-hooks

# Run hooks manually
pre-commit run --all-files

# Skip hooks temporarily (not recommended)
git commit --no-verify
```

---

## 📞 Support & Documentation

### Documentation
- **CI/CD Pipeline**: [docs/CICD.md](docs/CICD.md) - GitHub Actions workflows
- **Deployment Guide**: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) - Production deployment
- **Developer Guide**: [docs/DEVELOPER.md](docs/DEVELOPER.md) - Local development setup
- **API Documentation**: http://localhost:8000/docs - Interactive Swagger UI
- **Secrets Configuration**: [.github/SECRETS.md](.github/SECRETS.md) - Required secrets
- **Environment Template**: [.env.production.example](.env.production.example) - Production config

### Quick Help

```bash
# Show all available Make commands
make help

# Run health checks
make health
./scripts/health_check.sh

# View logs
make dev-logs
make logs-backend
make logs-frontend

# Get support
# - GitHub Issues: https://github.com/Gooderman932/market-data/issues
# - Email: support@yourcompany.com
```

---

## ✅ Next Steps

After setup is complete:

1. **Explore the Platform**
   - Access frontend at http://localhost:5173
   - Review API docs at http://localhost:8000/docs
   - Test the health endpoint: http://localhost:8000/health

2. **Developer Setup**
   - Install pre-commit hooks: `make install-hooks`
   - Run tests: `make test`
   - Run linters: `make lint`
   - Format code: `make format`

3. **Learn the Tools**
   - Run `make help` to see all 40+ commands
   - Read [docs/DEVELOPER.md](docs/DEVELOPER.md) for development workflow
   - Check [docs/CICD.md](docs/CICD.md) for CI/CD pipeline

4. **Database Management**
   - Create migrations: `make migrate-create msg="description"`
   - Run migrations: `make migrate`
   - Backup database: `make backup`

5. **Production Deployment**
   - Review [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
   - Configure GitHub secrets from [.github/SECRETS.md](.github/SECRETS.md)
   - Use production environment template: `.env.production.example`

6. **CI/CD Integration**
   - GitHub Actions run automatically on push
   - Security scans run weekly
   - Deployment workflows available for staging/production
   - Database migrations can be run via workflows

7. **Monitoring**
   - Configure Prometheus: see `monitoring/prometheus.yml`
   - Set up alerts: see `monitoring/alerts.yml`
   - Use health check script: `./scripts/health_check.sh`

---

## 🎉 Success!

Your Construction Intelligence Platform is now running. 

### Access Points
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Default Credentials
- **Email**: demo@example.com
- **Password**: demo123

### Quick Commands Reference
```bash
make help            # Show all available commands
make dev             # Start development environment
make test            # Run all tests
make lint            # Run all linters
make ci              # Run CI checks locally
./scripts/health_check.sh  # Check service health
```

### Next Steps
1. Review [docs/DEVELOPER.md](docs/DEVELOPER.md) for development workflow
2. Check [docs/CICD.md](docs/CICD.md) for CI/CD pipeline info
3. Read [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) before deploying to production

---

**Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.**
