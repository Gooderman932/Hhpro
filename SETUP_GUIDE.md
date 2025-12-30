# BuildIntel Pro - Setup Guide

Complete guide to set up and configure your Construction Intelligence Platform.

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Python 3.10+
- PostgreSQL 14+
- Redis 6+
- Node.js 18+ (for frontend)
- OpenAI API key (for ML features)

### Step 1: Clone and Setup Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model for entity extraction
python -m spacy download en_core_web_lg
```

### Step 2: Configure Environment

```bash
# Copy example environment file
cp ../.env.example ../.env

# Edit .env with your settings
nano ../.env  # or use your preferred editor
```

**Minimum Required Settings:**
```bash
# In .env file:
APP_NAME="BuildIntel Pro"
DATABASE_URL="postgresql://user:password@localhost:5432/buildintel_db"
REDIS_URL="redis://localhost:6379/0"
OPENAI_API_KEY="sk-proj-your-key-here"
SECRET_KEY="generate-a-random-string-here"
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

**Quick Start Everything:**

```bash
# Create docker-compose.yml in root directory
# (I'll provide this file next)

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

---

## 🧪 Testing the Setup

### 1. Backend Health Check
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy","version":"1.0.0"}
```

### 2. Database Connection
```bash
python -c "
from app.database import engine
from sqlalchemy import text
with engine.connect() as conn:
    result = conn.execute(text('SELECT 1'))
    print('Database connected:', result.fetchone())
"
```

### 3. Redis Connection
```bash
python -c "
import redis
r = redis.from_url('redis://localhost:6379/0')
r.set('test', 'hello')
print('Redis connected:', r.get('test'))
"
```

### 4. OpenAI API
```bash
python -c "
import openai
from app.config import settings
client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[{'role': 'user', 'content': 'Say hello'}],
    max_tokens=10
)
print('OpenAI connected:', response.choices[0].message.content)
"
```

### 5. ML Services
```bash
python -c "
from app.ml.project_classifier import classify_project
result = classify_project(
    'New 100,000 SF Office Building',
    'Proposed commercial office development...'
)
print('Classification:', result['project_type'], result['confidence'])
"
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

### Create New Migration

```bash
# After modifying models, create migration
alembic revision --autogenerate -m "Add new field to projects"

# Review the generated migration file
# Edit if needed: alembic/versions/xxx_add_new_field.py

# Apply migration
alembic upgrade head
```

### Rollback Migration

```bash
# Rollback one version
alembic downgrade -1

# Rollback to specific version
alembic downgrade abc123

# Rollback all
alembic downgrade base
```

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

### Database Connection Errors

```bash
# Check PostgreSQL is running
pg_isready -h localhost -p 5432

# Test connection
psql -U buildintel_user -d buildintel_db -h localhost

# Check DATABASE_URL format
echo $DATABASE_URL
```

### Redis Connection Errors

```bash
# Check Redis is running
redis-cli ping
# Should return: PONG

# Test connection
redis-cli -h localhost -p 6379
```

### OpenAI API Errors

```bash
# Test API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# Check usage/billing at: https://platform.openai.com/usage
```

### Import Errors

```bash
# Ensure virtual environment is activated
which python  # Should show venv path

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

---

## 📞 Support

- **Documentation**: http://localhost:8000/api/docs
- **GitHub Issues**: [your-repo]/issues
- **Email**: support@yourcompany.com

---

## ✅ Next Steps

After setup is complete:

1. **Create First Tenant**: Use admin panel or API
2. **Import Sample Data**: Run seed script
3. **Test ML Features**: Classify projects, score opportunities
4. **Set Up Frontend**: Follow frontend/README.md
5. **Configure Monitoring**: Set up Sentry, logging
6. **Schedule Background Jobs**: Cron for model retraining
7. **Deploy to Production**: Follow deployment guide

---

## 🎉 Success!

Your BuildIntel Pro platform is now running. Visit:

- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs
- **Health Check**: http://localhost:8000/health

**Default Admin Account** (if seeded):
- Email: admin@buildintel.com
- Password: Change this in production!
