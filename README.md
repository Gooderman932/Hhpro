# HHDrywall Repair Pro Platform
## Complete Implementation, Administration & Maintenance Guide

**Professional contractor/subcontractor job matching platform with e-commerce for hdrywallrepair.com**

**Integrated with:** [Construction Intelligence Platform](https://github.com/Gooderman932/market-data) by Poor Dude Holdings LLC

---

## 🌐 Live URLs

| Environment | URL |
|-------------|-----|
| **HDrywall Pro Platform** | https://pro.hhdrywallrepair.com |
| **Preview URL** | https://job-trade-match.preview.emergentagent.com |
| **Market Data Repo** | https://github.com/Gooderman932/market-data |

---

# TABLE OF CONTENTS

1. [Platform Overview](#platform-overview)
2. [Domain Implementation](#domain-implementation)
3. [HTML Integration](#html-integration)
4. [Market Data Repository Integration](#market-data-repository-integration)
5. [Product Administration](#product-administration)
6. [Market Data Tier Administration](#market-data-tier-administration)
7. [User Management](#user-management)
8. [Job Listings Management](#job-listings-management)
9. [Worker Profiles Management](#worker-profiles-management)
10. [Orders & Payments](#orders--payments)
11. [Stripe Configuration](#stripe-configuration)
12. [System Maintenance](#system-maintenance)
13. [Database Operations](#database-operations)
14. [Troubleshooting](#troubleshooting)
15. [Quick Reference](#quick-reference)

---

# PLATFORM OVERVIEW

## HhDrywall Pro Features

### For Contractors
- Post jobs with trade codes (09-Drywall, 03-Concrete, etc.)
- Browse skilled worker profiles
- Purchase professional tools
- Access market data analytics

### For Subcontractors
- Create professional profiles with skills & experience
- Browse available job opportunities
- Purchase tools and supplies
- Track availability status

### E-Commerce (Pro Shop)
- Contractor tools and supplies
- Category filtering
- Shopping cart with Stripe checkout

### Market Data Analytics (3 Tiers)

| Tier | Price | Projects Limit | Features |
|------|-------|----------------|----------|
| **Basic** | $299/mo | 100 projects | Regional trends, basic analytics, monthly reports |
| **Professional** | $799/mo | 1,000 projects | National data, real-time tracking, competitor analysis |
| **Enterprise** | $1,999/mo | Unlimited | API access, custom integrations, predictive analytics, dedicated support |

---

# DOMAIN IMPLEMENTATION

## Subdomain Setup (pro.hhdrywallrepair.com)

### Step 1: Add DNS Record

Go to your domain provider (GoDaddy, Namecheap, Cloudflare):

```
Type:   CNAME
Name:   pro
Value:  job-trade-match.preview.emergentagent.com
TTL:    Auto (or 3600)
```

### Step 2: Connect in Emergent Dashboard

1. Go to **Home** in Emergent
2. Click **HhDrywall Repair** project
3. Click **"Link domain"**
4. Enter: `pro.hhdrywallrepair.com`
5. Click **"Entri"** → follow prompts
6. Wait 5-15 minutes for SSL

### Step 3: Verify

Visit `https://pro.hhdrywallrepair.com`

---

# HTML INTEGRATION

## Navigation Links

```html
<a href="https://pro.hhdrywallrepair.com/jobs">Find Jobs</a>
<a href="https://pro.hhdrywallrepair.com/workers">Find Workers</a>
<a href="https://pro.hhdrywallrepair.com/shop">Pro Shop</a>
<a href="https://pro.hhdrywallrepair.com/market-data">Market Data</a>
```

## Call-to-Action Buttons

```html
<!-- Orange "Get Started" Button -->
<a href="https://pro.hhdrywallrepair.com/register" 
   style="display:inline-block; background:#f97316; color:white; 
          padding:14px 28px; text-decoration:none; font-weight:600; 
          text-transform:uppercase; border-radius:2px;">
   Get Started
</a>

<!-- Dark "Browse Jobs" Button -->
<a href="https://pro.hhdrywallrepair.com/jobs" 
   style="display:inline-block; background:#0f172a; color:white; 
          padding:14px 28px; text-decoration:none; font-weight:600; 
          text-transform:uppercase; border-radius:2px;">
   Browse Jobs
</a>

<!-- Market Data Button -->
<a href="https://pro.hhdrywallrepair.com/market-data" 
   style="display:inline-block; background:#0f172a; color:white; 
          padding:14px 28px; text-decoration:none; font-weight:600; 
          text-transform:uppercase; border-radius:2px;">
   Market Analytics
</a>
```

## Complete Feature Section

```html
<section style="padding:60px 20px; background:#f8fafc;">
  <div style="max-width:1200px; margin:0 auto; text-align:center;">
    <h2 style="font-size:32px; color:#0f172a; margin-bottom:40px;">
      Our Professional Services
    </h2>
    <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(250px,1fr)); gap:20px;">
      
      <a href="https://pro.hhdrywallrepair.com/jobs" 
         style="display:block; background:white; border:1px solid #e2e8f0; 
                padding:30px; text-decoration:none; text-align:center;">
        <h3 style="color:#0f172a; margin-bottom:10px;">Job Board</h3>
        <p style="color:#64748b; font-size:14px; margin-bottom:15px;">
          Find or post jobs by trade code and location
        </p>
        <span style="color:#f97316; font-weight:500;">Browse Jobs →</span>
      </a>
      
      <a href="https://pro.hhdrywallrepair.com/workers" 
         style="display:block; background:white; border:1px solid #e2e8f0; 
                padding:30px; text-decoration:none; text-align:center;">
        <h3 style="color:#0f172a; margin-bottom:10px;">Find Workers</h3>
        <p style="color:#64748b; font-size:14px; margin-bottom:15px;">
          Browse skilled subcontractors by trade
        </p>
        <span style="color:#f97316; font-weight:500;">View Profiles →</span>
      </a>
      
      <a href="https://pro.hhdrywallrepair.com/shop" 
         style="display:block; background:white; border:1px solid #e2e8f0; 
                padding:30px; text-decoration:none; text-align:center;">
        <h3 style="color:#0f172a; margin-bottom:10px;">Pro Shop</h3>
        <p style="color:#64748b; font-size:14px; margin-bottom:15px;">
          Professional tools and supplies
        </p>
        <span style="color:#f97316; font-weight:500;">Shop Now →</span>
      </a>
      
      <a href="https://pro.hhdrywallrepair.com/market-data" 
         style="display:block; background:white; border:1px solid #e2e8f0; 
                padding:30px; text-decoration:none; text-align:center;">
        <h3 style="color:#0f172a; margin-bottom:10px;">Market Data</h3>
        <p style="color:#64748b; font-size:14px; margin-bottom:15px;">
          Construction industry analytics
        </p>
        <span style="color:#f97316; font-weight:500;">View Plans →</span>
      </a>
      
    </div>
  </div>
</section>
```

---

# MARKET DATA REPOSITORY INTEGRATION

## Repository Overview

**Repository:** https://github.com/Gooderman932/market-data  
**Copyright:** Poor Dude Holdings LLC  
**Description:** Enterprise SaaS platform for construction market intelligence

### Features from Market Data Platform

| Feature | Description |
|---------|-------------|
| **Project Discovery** | Track opportunities, permits, and tenders |
| **Competitive Intelligence** | Analyze competitor activity and market share |
| **Predictive Analytics** | Win probability models and demand forecasting |
| **Market Insights** | Regional analysis and trend visualization |

### Tech Stack

- **Backend:** Python 3.11+ with FastAPI, PostgreSQL 16, SQLAlchemy 2.0
- **Frontend:** React 18 with TypeScript, Vite, Tailwind CSS, Recharts
- **ML/AI:** scikit-learn, OpenAI API
- **Infrastructure:** Docker, Redis 7, Nginx

---

## Step 1: Clone the Repository

```bash
# Clone to your server
git clone https://github.com/Gooderman932/market-data.git
cd market-data

# Or clone to specific directory
git clone https://github.com/Gooderman932/market-data.git /opt/market-data
```

## Step 2: Environment Configuration

```bash
# Copy example environment file
cp .env.example .env

# Edit with your configuration
nano .env
```

**Required Environment Variables:**

```env
# Application
APP_NAME="BuildIntel Pro"
ENVIRONMENT=production
DEBUG=False

# Database (PostgreSQL)
DATABASE_URL="postgresql://user:password@localhost:5432/construction_intel"

# Authentication
SECRET_KEY="your-secure-secret-key-change-this"
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Redis Cache
REDIS_URL="redis://localhost:6379/0"

# OpenAI (for AI features)
OPENAI_API_KEY="sk-your-openai-key"
OPENAI_MODEL="gpt-4o"

# Multi-tenancy Limits
MAX_PROJECTS_PER_TENANT_FREE=100
MAX_PROJECTS_PER_TENANT_PRO=1000
MAX_PROJECTS_PER_TENANT_ENTERPRISE=0  # 0 = unlimited
```

## Step 3: Docker Deployment (Recommended)

```bash
# Development
make quickstart
# or
docker compose up --build

# Production
docker-compose -f docker-compose.prod.yml up -d
```

**Access Points:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Step 4: Manual Installation (Alternative)

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql://user:password@localhost:5432/construction_intel"
export SECRET_KEY="your-secret-key"

# Setup database
python ../scripts/setup_db.py
python ../scripts/seed_data.py

# Run backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Step 5: Database Initialization

```bash
# Initialize database schema
make db-init

# Seed sample data (optional)
make db-seed

# Run migrations
cd backend
alembic upgrade head
```

## Step 6: Default Login Credentials

After seeding:
- **Email:** demo@example.com
- **Password:** demo123

---

## Market Data API Endpoints

### Authentication
```
POST /api/auth/token        → Login
POST /api/auth/register     → Register new user
GET  /api/auth/me           → Get current user
```

### Projects
```
GET    /api/projects/       → List projects (with filters)
GET    /api/projects/{id}   → Get project details
POST   /api/projects/       → Create project
PUT    /api/projects/{id}   → Update project
DELETE /api/projects/{id}   → Delete project
```

### Analytics
```
GET /api/analytics/summary  → Dashboard summary
GET /api/analytics/trends   → Project trends
GET /api/analytics/regions  → Regional analysis
```

### Intelligence
```
GET /api/intelligence/competitors    → Competitor data
GET /api/intelligence/market-share   → Market share analysis
GET /api/intelligence/relationships  → Relationship graph
```

---

## Linking Market Data to HDrywall Platform

### Option A: API Integration

Add to HDrywall backend (`/app/backend/server.py`):

```python
import httpx

MARKET_DATA_API_URL = os.environ.get("MARKET_DATA_API_URL", "http://localhost:8000")
MARKET_DATA_API_KEY = os.environ.get("MARKET_DATA_API_KEY")

@api_router.get("/market-data/analytics/{tier_id}")
async def get_market_analytics(tier_id: str, request: Request):
    """Proxy to market data analytics API"""
    user = await require_user(request)
    
    # Verify subscription
    subscription = await db.subscriptions.find_one({
        "user_id": user["user_id"],
        "tier_id": tier_id,
        "status": "active"
    }, {"_id": 0})
    
    if not subscription:
        raise HTTPException(status_code=403, detail="Active subscription required")
    
    # Call market data API
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{MARKET_DATA_API_URL}/api/analytics/summary",
            headers={"Authorization": f"Bearer {MARKET_DATA_API_KEY}"}
        )
        return response.json()
```

### Option B: Subdomain Setup

Deploy market-data platform to a subdomain:

1. Add DNS record:
```
Type: A or CNAME
Name: intel
Value: your-server-ip or target
```

2. Configure Nginx:
```nginx
server {
    listen 80;
    server_name intel.hdrywallrepair.com;
    
    location / {
        proxy_pass http://localhost:5173;  # Market data frontend
    }
    
    location /api {
        proxy_pass http://localhost:8000;  # Market data backend
    }
}
```

3. Access at: `https://intel.hdrywallrepair.com`

### Option C: Embed in HDrywall Platform

Create iframe integration on market data page:

```html
<iframe 
    src="https://intel.hdrywallrepair.com/dashboard" 
    width="100%" 
    height="800px" 
    frameborder="0">
</iframe>
```

---

## Market Data Maintenance

### Daily Tasks

```bash
# Update market data
cd /opt/market-data
git pull origin main
docker-compose restart

# Check health
./scripts/deployment/health-check.sh
```

### Weekly Tasks

```bash
# Run platform automation
make run-automation

# Security scan
make security-scan

# Backup database
make backup
```

### Database Migrations

```bash
# Create new migration
cd backend
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Update Dependencies

```bash
# Backend
cd backend
pip install -r requirements.txt --upgrade

# Frontend
cd frontend
npm update
```

---

# PRODUCT ADMINISTRATION

## View All Products

```javascript
mongosh
use test_database
db.products.find().pretty()
```

## Add New Product

```javascript
db.products.insertOne({
  "product_id": "prod_" + Math.random().toString(36).substr(2, 12),
  "name": "Product Name",
  "description": "Description",
  "category": "Drywall Tools",
  "price": 29.99,
  "compare_price": 39.99,
  "image_url": "https://example.com/image.jpg",
  "stock": 100,
  "sku": "SKU-001",
  "active": true,
  "created_at": new Date().toISOString()
})
```

**Categories:** Drywall Tools, Materials, Power Tools, Safety Gear, Blades & Accessories, Storage & Organization

## Update Product Price

```javascript
db.products.updateOne(
  { "name": "Product Name" },
  { $set: { "price": 49.99, "compare_price": 69.99 } }
)
```

## Update Stock

```javascript
// Set specific level
db.products.updateOne(
  { "product_id": "prod_abc123" },
  { $set: { "stock": 100 } }
)

// Decrease after sale
db.products.updateOne(
  { "product_id": "prod_abc123" },
  { $inc: { "stock": -5 } }
)

// Increase after restock
db.products.updateOne(
  { "product_id": "prod_abc123" },
  { $inc: { "stock": 50 } }
)
```

## Deactivate/Delete Product

```javascript
// Deactivate (hide from shop)
db.products.updateOne(
  { "name": "Product Name" },
  { $set: { "active": false } }
)

// Delete permanently
db.products.deleteOne({ "product_id": "prod_abc123" })
```

## Bulk Price Update

```javascript
// Increase all by 10%
db.products.updateMany(
  {},
  [{ $set: { "price": { $multiply: ["$price", 1.10] } } }]
)

// Decrease all by 15%
db.products.updateMany(
  {},
  [{ $set: { "price": { $multiply: ["$price", 0.85] } } }]
)
```

---

# MARKET DATA TIER ADMINISTRATION

## Current Configuration

Located in `/app/backend/server.py`:

```python
MARKET_DATA_TIERS = [
    {
        "tier_id": "basic",
        "name": "Basic Analytics",
        "price": 299.00,
        "billing_period": "monthly",
        "description": "Essential market insights for growing businesses",
        "features": [
            "Regional labor market trends",
            "Basic wage analytics",
            "Monthly industry reports",
            "Email support",
            "Up to 100 projects"
        ]
    },
    {
        "tier_id": "professional",
        "name": "Professional Suite",
        "price": 799.00,
        "billing_period": "monthly",
        "description": "Comprehensive analytics for established contractors",
        "features": [
            "All Basic features",
            "National market data",
            "Real-time wage tracking",
            "Competitor analysis",
            "Custom report generation",
            "Priority support",
            "Up to 1,000 projects"
        ]
    },
    {
        "tier_id": "enterprise",
        "name": "Enterprise Platform",
        "price": 1999.00,
        "billing_period": "monthly",
        "description": "Full-scale intelligence for large construction firms",
        "features": [
            "All Professional features",
            "API access",
            "Custom data integrations",
            "Predictive analytics",
            "Win probability models",
            "Demand forecasting",
            "Dedicated account manager",
            "White-label reports",
            "24/7 phone support",
            "Unlimited projects"
        ]
    }
]
```

## Change Tier Pricing

1. Edit `/app/backend/server.py`
2. Find `MARKET_DATA_TIERS`
3. Change price values:
```python
"price": 349.00,  # Changed from 299.00
```
4. Restart backend:
```bash
sudo supervisorctl restart backend
```

## Add/Remove Features

Edit the `features` array for each tier:

```python
"features": [
    "Existing feature",
    "NEW: Added feature",  # Add
    # Remove by deleting the line
]
```

---

# USER MANAGEMENT

## View Users

```javascript
db.users.find().pretty()
db.users.find({ "user_type": "contractor" }).pretty()
db.users.find({ "user_type": "subcontractor" }).pretty()
```

## Change User Type

```javascript
db.users.updateOne(
  { "email": "user@example.com" },
  { $set: { "user_type": "contractor" } }
)
```

## Delete User

```javascript
db.users.deleteOne({ "email": "user@example.com" })
db.user_sessions.deleteMany({ "user_id": "user_abc123" })
```

---

# JOB LISTINGS MANAGEMENT

## View/Search Jobs

```javascript
db.jobs.find().pretty()
db.jobs.find({ "status": "active" }).pretty()
db.jobs.find({ "trade_codes": "09" }).pretty()
```

## Close/Reopen Job

```javascript
// Close
db.jobs.updateOne(
  { "job_id": "job_abc123" },
  { $set: { "status": "closed" } }
)

// Reopen
db.jobs.updateOne(
  { "job_id": "job_abc123" },
  { $set: { "status": "active" } }
)
```

---

# WORKER PROFILES MANAGEMENT

## View/Search Profiles

```javascript
db.worker_profiles.find().pretty()
db.worker_profiles.find({ "trade_codes": "09" }).pretty()
db.worker_profiles.find({ "availability": "immediate" }).pretty()
```

## Deactivate/Delete Profile

```javascript
db.worker_profiles.updateOne(
  { "profile_id": "profile_abc123" },
  { $set: { "status": "inactive" } }
)

db.worker_profiles.deleteOne({ "profile_id": "profile_abc123" })
```

---

# ORDERS & PAYMENTS

## View Transactions

```javascript
db.orders.find().pretty()
db.payment_transactions.find().pretty()
db.payment_transactions.find({ "payment_status": "paid" }).pretty()
```

## Revenue Statistics

```javascript
// Total revenue
db.payment_transactions.aggregate([
  { $match: { "payment_status": "paid" } },
  { $group: { _id: null, total: { $sum: "$amount" } } }
])
```

---

# STRIPE CONFIGURATION

## Switch to Live Mode

1. Get keys from https://dashboard.stripe.com/apikeys
2. Update `/app/backend/.env`:
```env
STRIPE_API_KEY=sk_live_your_live_key
```
3. Restart: `sudo supervisorctl restart backend`

---

# SYSTEM MAINTENANCE

## Service Commands

```bash
sudo supervisorctl status
sudo supervisorctl restart backend
sudo supervisorctl restart frontend
sudo supervisorctl restart all
```

## View Logs

```bash
tail -f /var/log/supervisor/backend.err.log
tail -f /var/log/supervisor/frontend.err.log
```

## Environment Variables

**Backend** (`/app/backend/.env`):
```env
MONGO_URL="mongodb://localhost:27017"
DB_NAME="test_database"
JWT_SECRET="your-secret-key"
STRIPE_API_KEY=sk_test_emergent
MARKET_DATA_API_URL="http://localhost:8000"
```

---

# DATABASE OPERATIONS

## Backup

```bash
mongodump --db test_database --out /app/backup/$(date +%Y%m%d)
```

## Restore

```bash
mongorestore --db test_database /app/backup/20250117/test_database/
```

## Create Indexes

```javascript
db.users.createIndex({ "email": 1 }, { unique: true })
db.jobs.createIndex({ "trade_codes": 1 })
db.products.createIndex({ "category": 1 })
```

---

# TROUBLESHOOTING

| Issue | Solution |
|-------|----------|
| Backend not starting | Check logs: `tail -n 50 /var/log/supervisor/backend.err.log` |
| Frontend not loading | Check logs: `tail -n 50 /var/log/supervisor/frontend.err.log` |
| Database connection failed | `sudo systemctl restart mongod` |
| API returns 500 | Check backend logs for Python errors |
| DNS not working | Wait 24-48 hours, check dnschecker.org |

---

# QUICK REFERENCE

## URLs

| Resource | URL |
|----------|-----|
| HDrywall Platform | https://pro.hdrywallrepair.com |
| Market Data Platform | https://intel.hdrywallrepair.com |
| API Health | /api/health |
| API Docs (Market Data) | /api/docs |

## Platform Pages

| Page | Path |
|------|------|
| Home | `/` |
| Jobs | `/jobs` |
| Workers | `/workers` |
| Shop | `/shop` |
| Market Data | `/market-data` |
| Dashboard | `/dashboard` |

## Trade Codes

| Code | Trade |
|------|-------|
| 03 | Concrete |
| 04 | Masonry |
| 05 | Metals |
| 06 | Wood, Plastics |
| 07 | Thermal/Moisture |
| 08 | Openings |
| 09 | Finishes (Drywall/Paint) |
| 22 | Plumbing |
| 23 | HVAC |
| 26 | Electrical |

## Quick Commands

| Task | Command |
|------|---------|
| Restart Backend | `sudo supervisorctl restart backend` |
| Restart Frontend | `sudo supervisorctl restart frontend` |
| View Logs | `tail -f /var/log/supervisor/backend.err.log` |
| MongoDB Shell | `mongosh` → `use test_database` |
| Backup DB | `mongodump --db test_database --out /app/backup/` |

---

## Contact

**HDrywall Repair**  
Email: info@hdrywallrepair.com  
Phone: (555) 123-4567

**Market Data Platform**  
Copyright © 2025 Poor Dude Holdings LLC  
Email: legal@poorduceholdings.com

---

*Built with FastAPI + React + MongoDB on Emergent Platform*  
*Market Data powered by Construction Intelligence Platform*  
*Last Updated: January 2025*
