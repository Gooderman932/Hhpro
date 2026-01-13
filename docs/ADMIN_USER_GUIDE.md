# Administrator & Developer User Guide

**BuildIntel Pro - Complete Administrator Guide**

Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.

Version: 1.0.0  
Last Updated: January 2025

---

## Table of Contents

- [System Overview](#system-overview)
- [Initial Setup](#initial-setup)
- [Running the Application](#running-the-application)
- [Configuration](#configuration)
- [Database Management](#database-management)
- [API Documentation](#api-documentation)
- [Monitoring & Logs](#monitoring--logs)
- [Troubleshooting](#troubleshooting)
- [Deployment](#deployment)

---

## System Overview

### What is BuildIntel Pro?

BuildIntel Pro is an enterprise SaaS platform for construction market intelligence, providing:
- **Project Discovery**: Track construction opportunities, permits, and tenders
- **Competitive Intelligence**: Analyze competitor activity and market share
- **Predictive Analytics**: Win probability models and demand forecasting
- **Market Insights**: Regional analysis and trend visualization

### Architecture

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│                 │         │                  │         │                 │
│  React Frontend │ ◄─────► │  FastAPI Backend │ ◄─────► │   PostgreSQL    │
│  (Port 3000)    │         │   (Port 8000)    │         │   Database      │
│                 │         │                  │         │                 │
└─────────────────┘         └──────────────────┘         └─────────────────┘
                                    │
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
            ┌──────────────┐ ┌──────────┐ ┌──────────────┐
            │    Redis     │ │ OpenAI   │ │  External    │
            │    Cache     │ │   API    │ │   APIs       │
            └──────────────┘ └──────────┘ └──────────────┘
```

### Key Components

**Backend (FastAPI + Python)**
- RESTful API with automatic OpenAPI documentation
- JWT-based authentication
- Multi-tenant architecture
- ML/AI integration for predictions
- Real-time data processing

**Frontend (React + TypeScript)**
- Modern, responsive UI with Tailwind CSS
- Real-time data visualization with Recharts
- Type-safe development with TypeScript
- Fast build times with Vite

**Database (PostgreSQL)**
- Relational data storage
- Multi-tenant data isolation
- Optimized for complex queries
- Full-text search capabilities

---

## Initial Setup

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11+**: [Download Python](https://www.python.org/downloads/)
- **Node.js 18+** and **npm**: [Download Node.js](https://nodejs.org/)
- **PostgreSQL 16+**: [Download PostgreSQL](https://www.postgresql.org/download/)
- **Git**: [Download Git](https://git-scm.com/downloads)
- **Redis** (optional but recommended): [Download Redis](https://redis.io/download)

**Verify installations:**
```bash
python --version   # Should be 3.11 or higher
node --version     # Should be 18 or higher
npm --version      # Should be 9 or higher
psql --version     # Should be 16 or higher
git --version      # Any recent version
```

### Clone Repository

```bash
# Clone the repository
git clone https://github.com/your-org/market-data.git
cd market-data

# Or if you already have it cloned
cd /path/to/market-data
```

### Backend Setup

#### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

#### 2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3. Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your settings
nano .env  # or use your preferred editor
```

**Critical settings to update:**
```ini
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/buildintel

# Security (IMPORTANT: Change in production!)
SECRET_KEY=your-super-secret-key-change-this-in-production

# OpenAI (if using AI features)
OPENAI_API_KEY=sk-your-openai-api-key

# Redis (if using caching)
REDIS_URL=redis://localhost:6379/0
```

### Database Setup

#### 1. Create PostgreSQL Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database and user
CREATE DATABASE buildintel;
CREATE USER buildintel_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE buildintel TO buildintel_user;

# Exit psql
\q
```

#### 2. Run Migrations

```bash
cd backend

# Run Alembic migrations
alembic upgrade head

# Verify database setup
python scripts/verify_database.py
```

#### 3. Seed Initial Data (Optional)

```bash
cd scripts
python seed_data.py
```

### Frontend Setup

#### 1. Install Dependencies

```bash
cd frontend
npm install
```

#### 2. Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env.local

# Edit .env.local
nano .env.local
```

**Update these settings:**
```ini
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=BuildIntel Pro
```

---

## Running the Application

### Development Mode (Recommended for Development)

You'll need **three terminal windows** open:

#### Terminal 1: Backend Server

```bash
cd backend
source venv/bin/activate  # Activate virtual environment
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at: **http://localhost:8000**

#### Terminal 2: Frontend Development Server

```bash
cd frontend
npm run dev
```

The frontend will be available at: **http://localhost:3000** (or port shown in terminal)

#### Terminal 3: Redis (Optional)

```bash
# On macOS/Linux:
redis-server

# On Windows (if Redis is installed):
redis-server.exe
```

### Production Mode (Docker)

For production-like environment, use Docker Compose:

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Services:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/api/docs

### Quick Test Connection

After starting the services, test the connection:

```bash
# Make the script executable (first time only)
chmod +x test-frontend-backend.sh

# Run connection test
./test-frontend-backend.sh
```

---

## Configuration

### Environment Variables

#### Backend Configuration (`backend/.env`)

**Application Settings**
```ini
APP_NAME=BuildIntel Pro
APP_VERSION=1.0.0
ENVIRONMENT=development  # or staging, production
DEBUG=true
LOG_LEVEL=INFO
```

**Security Configuration**
```ini
SECRET_KEY=your-secret-key-minimum-32-characters-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

**Database Configuration**
```ini
DATABASE_URL=postgresql://user:password@localhost:5432/buildintel
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=40
DATABASE_ECHO=false
```

**Redis Configuration**
```ini
REDIS_URL=redis://localhost:6379/0
CACHE_TTL=3600
```

**OpenAI Configuration**
```ini
OPENAI_API_KEY=sk-your-api-key
OPENAI_MODEL=gpt-4o
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

**CORS Configuration**
```ini
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173","https://yourdomain.com"]
```

**Multi-tenancy Settings**
```ini
ENABLE_MULTI_TENANT=true
MAX_USERS_PER_TENANT=50
MAX_PROJECTS_PER_TENANT_PRO=1000
```

#### Frontend Configuration (`frontend/.env.local`)

```ini
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=BuildIntel Pro
VITE_ENVIRONMENT=development
```

### Security Configuration

#### Generate Strong SECRET_KEY

```python
# Generate a secure random key
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### Configure HTTPS (Production)

Update Nginx configuration:
```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;

    # Frontend
    location / {
        root /var/www/buildintel/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## Database Management

### Running Migrations

#### Create New Migration

```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
```

#### Apply Migrations

```bash
# Upgrade to latest
alembic upgrade head

# Upgrade one version
alembic upgrade +1

# Downgrade one version
alembic downgrade -1

# View migration history
alembic history
```

### Database Backups

#### Create Backup

```bash
# Full database backup
pg_dump -U buildintel_user -h localhost buildintel > backup_$(date +%Y%m%d_%H%M%S).sql

# Compressed backup
pg_dump -U buildintel_user -h localhost buildintel | gzip > backup_$(date +%Y%m%d_%H%M%S).sql.gz
```

#### Restore Backup

```bash
# Restore from backup
psql -U buildintel_user -h localhost buildintel < backup_20250109.sql

# Restore from compressed backup
gunzip -c backup_20250109.sql.gz | psql -U buildintel_user -h localhost buildintel
```

#### Automated Backup Script

Create `backup_db.sh`:
```bash
#!/bin/bash
BACKUP_DIR="/var/backups/buildintel"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

pg_dump -U buildintel_user buildintel | gzip > $BACKUP_DIR/backup_$DATE.sql.gz

# Keep only last 30 days
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +30 -delete

echo "Backup completed: backup_$DATE.sql.gz"
```

Add to crontab for daily backups:
```bash
# Edit crontab
crontab -e

# Add line for daily backup at 2 AM
0 2 * * * /path/to/backup_db.sh
```

### Database Queries

#### Common Queries

```sql
-- Get total users
SELECT COUNT(*) FROM users;

-- Get projects by tenant
SELECT t.name, COUNT(p.id) as project_count
FROM tenants t
LEFT JOIN projects p ON t.id = p.tenant_id
GROUP BY t.id, t.name;

-- Get recent activity
SELECT * FROM projects
ORDER BY created_at DESC
LIMIT 10;

-- Database size
SELECT pg_size_pretty(pg_database_size('buildintel'));

-- Table sizes
SELECT
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename))
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

---

## API Documentation

### Authentication Flow

#### 1. Obtain Access Token

```bash
curl -X POST "http://localhost:8000/api/v1/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=yourpassword"
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### 2. Use Token in Requests

```bash
curl -X GET "http://localhost:8000/api/v1/projects" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Key Endpoints

#### System Endpoints

- `GET /health` - Health check
- `GET /` - API information
- `GET /api/docs` - Interactive API documentation (Swagger UI)
- `GET /api/redoc` - API documentation (ReDoc)

#### Authentication

- `POST /api/v1/auth/token` - Get access token
- `POST /api/v1/auth/register` - Register new user

#### Projects

- `GET /api/v1/projects` - List projects
- `GET /api/v1/projects/{id}` - Get project details
- `POST /api/v1/projects` - Create project
- `PUT /api/v1/projects/{id}` - Update project
- `DELETE /api/v1/projects/{id}` - Delete project

#### Analytics

- `GET /api/v1/analytics/summary` - Market summary
- `GET /api/v1/analytics/trends` - Trend analysis
- `GET /api/v1/analytics/regional` - Regional analysis

#### Intelligence

- `GET /api/v1/intelligence/competitors` - Competitor analysis
- `GET /api/v1/intelligence/market-share` - Market share data
- `GET /api/v1/intelligence/relationships` - Relationship mapping

### Example API Calls

#### Get Projects with Filters

```bash
curl -X GET "http://localhost:8000/api/v1/projects?sector=commercial&status=active&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### Create New Project

```bash
curl -X POST "http://localhost:8000/api/v1/projects" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Commercial Building",
    "description": "50,000 sq ft office space",
    "project_type": "opportunity",
    "sector": "commercial",
    "value": 5000000,
    "city": "New York",
    "state": "NY"
  }'
```

---

## Monitoring & Logs

### Log Locations

#### Development Mode

**Backend Logs:**
- Console output: Terminal where `uvicorn` is running
- File logs: `backend/logs/`
  - `info.log` - General application logs
  - `error.log` - Errors and exceptions
  - `debug.log` - Detailed debugging (dev only)
  - `access.log` - API access logs

**Frontend Logs:**
- Console output: Browser developer console
- Build logs: Terminal where `npm run dev` is running

#### Production Mode (Docker)

```bash
# View all logs
docker-compose logs

# View backend logs
docker-compose logs backend

# View frontend logs
docker-compose logs frontend

# Follow logs in real-time
docker-compose logs -f backend

# View last 100 lines
docker-compose logs --tail=100 backend
```

### Log Levels

Configure via `LOG_LEVEL` environment variable:

- **DEBUG**: Detailed information for debugging
- **INFO**: General informational messages (default)
- **WARNING**: Warning messages
- **ERROR**: Error messages
- **CRITICAL**: Critical issues

### Performance Monitoring

#### Monitor API Response Times

Check the `X-Process-Time` header in API responses:

```bash
curl -I http://localhost:8000/api/v1/projects
# Look for: X-Process-Time: 0.045
```

#### Monitor Database Performance

```sql
-- Slow queries
SELECT
    query,
    calls,
    total_time,
    mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Active connections
SELECT count(*) FROM pg_stat_activity;

-- Database cache hit ratio (should be > 95%)
SELECT
    sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) * 100 as cache_hit_ratio
FROM pg_statio_user_tables;
```

---

## Troubleshooting

### Common Issues

#### 1. Port Already in Use

**Problem:** Cannot start backend because port 8000 is in use

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows

# Or use a different port
uvicorn app.main:app --port 8001
```

#### 2. Database Connection Errors

**Problem:** `sqlalchemy.exc.OperationalError: could not connect to server`

**Solution:**
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql  # Linux
brew services list  # macOS

# Start PostgreSQL
sudo systemctl start postgresql  # Linux
brew services start postgresql  # macOS

# Verify connection
psql -U buildintel_user -h localhost -d buildintel

# Check DATABASE_URL in .env
echo $DATABASE_URL
```

#### 3. Frontend Cannot Connect to Backend

**Problem:** API calls fail with CORS errors

**Solution:**
1. Verify backend is running: `curl http://localhost:8000/health`
2. Check `CORS_ORIGINS` in backend `.env`:
   ```ini
   CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
   ```
3. Verify `VITE_API_URL` in frontend `.env.local`:
   ```ini
   VITE_API_URL=http://localhost:8000
   ```
4. Run connection test:
   ```bash
   ./test-frontend-backend.sh
   ```

#### 4. Migration Errors

**Problem:** `alembic upgrade head` fails

**Solution:**
```bash
# Check current migration status
alembic current

# View migration history
alembic history

# Reset to specific version
alembic downgrade <revision>

# If all else fails, drop and recreate
dropdb buildintel
createdb buildintel
alembic upgrade head
```

#### 5. Module Not Found Errors

**Problem:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep fastapi
```

#### 6. Permission Errors

**Problem:** Permission denied errors when running scripts

**Solution:**
```bash
# Make scripts executable
chmod +x test-frontend-backend.sh
chmod +x scripts/quick-start.sh

# Fix file ownership
sudo chown -R $USER:$USER /path/to/market-data
```

### Getting Help

If issues persist:

1. **Check logs**: Review backend logs in `backend/logs/error.log`
2. **Run diagnostics**:
   ```bash
   python backend/tests/test_backend.py
   python backend/scripts/verify_database.py
   ./test-frontend-backend.sh
   ```
3. **Contact support**:
   - Email: dev@poorduceholdings.com
   - Include: Error messages, log files, and steps to reproduce

---

## Deployment

### Pre-Deployment Checklist

Before deploying to production:

- [ ] Review [Production Checklist](PRODUCTION_CHECKLIST.md)
- [ ] Update all environment variables
- [ ] Change SECRET_KEY to production value
- [ ] Set DEBUG=false
- [ ] Configure PostgreSQL with production credentials
- [ ] Set up Redis for production
- [ ] Configure HTTPS/SSL certificates
- [ ] Set up monitoring and alerting
- [ ] Test backup and restore procedures

### Nginx Configuration

Create `/etc/nginx/sites-available/buildintel`:

```nginx
upstream backend {
    server localhost:8000;
}

server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Frontend
    location / {
        root /var/www/buildintel/frontend/dist;
        try_files $uri $uri/ /index.html;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Backend API
    location /api {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Health check
    location /health {
        proxy_pass http://backend;
        access_log off;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/buildintel /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Gunicorn Setup

Create `gunicorn_config.py`:

```python
bind = "127.0.0.1:8000"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
timeout = 30
keepalive = 2
errorlog = "/var/log/buildintel/gunicorn-error.log"
accesslog = "/var/log/buildintel/gunicorn-access.log"
loglevel = "info"
```

Start with Gunicorn:
```bash
gunicorn app.main:app -c gunicorn_config.py
```

### Systemd Service

Create `/etc/systemd/system/buildintel.service`:

```ini
[Unit]
Description=BuildIntel Pro Backend
After=network.target postgresql.service redis.service

[Service]
Type=notify
User=buildintel
Group=buildintel
WorkingDirectory=/var/www/buildintel/backend
Environment="PATH=/var/www/buildintel/backend/venv/bin"
ExecStart=/var/www/buildintel/backend/venv/bin/gunicorn app.main:app -c gunicorn_config.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable buildintel
sudo systemctl start buildintel
sudo systemctl status buildintel
```

---

## Additional Resources

- **API Documentation**: http://localhost:8000/api/docs
- **Production Checklist**: [PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md)
- **API Integration Guide**: [API_INTEGRATION_GUIDE.md](API_INTEGRATION_GUIDE.md)
- **Customer Guide**: [CUSTOMER_USER_GUIDE.md](CUSTOMER_USER_GUIDE.md)

---

**Document Version**: 1.0.0  
**Last Updated**: January 2025  
**Support**: dev@poorduceholdings.com
