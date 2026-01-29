# HHDrywall Repair Pro Platform
## Complete Implementation, Administration & Maintenance Guide

**Professional contractor/subcontractor job matching platform with e-commerce for hhdrywallrepair.com**

**Integrated with:** [Construction Intelligence Platform](https://github.com/Gooderman932/market-data) by Poor Dude Holdings LLC

---

## 🌐 Live URLs

| Environment | URL |
|-------------|-----|
| **HhDrywall Pro Platform** | https://pro.hhdrywallrepair.com |
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

Add to HhDrywall backend (`/app/backend/server.py`):

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

### Option C: Embed in Hhdrywall Platform

Create iframe integration on market data page:

```html
<iframe 
    src="https://intel.hhdrywallrepair.com/dashboard" 
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
| HhDrywall Platform | https://pro.hhdrywallrepair.com |
| Market Data Platform | https://intel.hhdrywallrepair.com |
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
HHDrywall Repair Pro Platform
Complete Implementation, Administration & Maintenance Guide
Professional contractor/subcontractor job matching platform with e-commerce for hdrywallrepair.com
Integrated with: Construction Intelligence Platform by Poor Dude Holdings LLC
🌐 Live URLs
Environment
URL
HDrywall Pro Platform
https://pro.hhdrywallrepair.com
Preview URL
https://job-trade-match.preview.emergentagent.com
Market Data Repo
https://github.com/Gooderman932/market-data
Construction Intel Platform
https://intel.hhdrywallrepair.com
📑 TABLE OF CONTENTS
Platform Overview
Frontend Assets & Branding
Domain Implementation
HTML Integration
Market Data Repository Integration
Product Administration
Market Data Tier Administration
User Management
Job Listings Management
Worker Profiles Management
Orders & Payments
Stripe Configuration
System Maintenance
Database Operations
Troubleshooting
Quick Reference
🏗️ PLATFORM OVERVIEW
HhDrywall Pro Features
For Contractors
✅ Post jobs with trade codes (09-Drywall, 03-Concrete, etc.)
✅ Browse skilled worker profiles
✅ Purchase professional tools
✅ Access market data analytics
For Subcontractors
✅ Create professional profiles with skills & experience
✅ Browse available job opportunities
✅ Purchase tools and supplies
✅ Track availability status
E-Commerce (Pro Shop)
✅ Contractor tools and supplies
✅ Category filtering
✅ Shopping cart with Stripe checkout
✅ Real-time inventory management
Market Data Analytics (3 Tiers)
Tier
Price
Projects Limit
Features
Basic
$299/mo
100 projects
Regional trends, basic analytics, monthly reports
Professional
$799/mo
1,000 projects
National data, real-time tracking, competitor analysis
Enterprise
$1,999/mo
Unlimited
API access, custom integrations, predictive analytics, dedicated support
🎨 FRONTEND ASSETS & BRANDING
Brand Colors
The platform uses a consistent blue color scheme:
/* Primary Colors */
--primary: hsl(221 83% 53%);          /* Blue #3b82f6 */
--primary-foreground: hsl(210 40% 98%); /* Off-white */

/* Secondary Colors */
--secondary: hsl(210 40% 96.1%);      /* Light blue-gray */
--accent: hsl(221 83% 53%);           /* Blue accent */

/* Orange Accent (CTAs) */
--orange: #f97316;                     /* Tailwind orange-500 */
Typography
/* Sans-serif (UI) */
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;

/* Monospace (Code) */
font-family: 'JetBrains Mono', 'Courier New', monospace;
Favicon & Icons
Location: /public/favicon.svg
The favicon features:
Construction building with windows
Crane illustration
Data analytics overlay
Blue brand color (#3b82f6)
Open Graph Image
Location: /public/og-image.jpg
Generate from template:
Open og-image-template.html in browser
Set viewport to 1200x630px
Take screenshot
Save as og-image.jpg in /public/
Specifications:
Dimensions: 1200x630px
Format: JPEG
Max size: 300KB
Quality: 85-90%
Meta Tags
<!-- SEO -->
<meta name="description" content="HHDrywall Pro Platform - Professional contractor/subcontractor job matching with e-commerce and market analytics" />
<meta name="keywords" content="drywall, contractor jobs, construction, subcontractor, market data, construction analytics" />

<!-- Theme Colors -->
<meta name="theme-color" content="#3b82f6" media="(prefers-color-scheme: light)" />
<meta name="theme-color" content="#2563eb" media="(prefers-color-scheme: dark)" />

<!-- Open Graph -->
<meta property="og:title" content="HHDrywall Repair Pro Platform" />
<meta property="og:description" content="Professional contractor/subcontractor job matching with e-commerce and market analytics" />
<meta property="og:image" content="https://pro.hhdrywallrepair.com/og-image.jpg" />
<meta property="og:url" content="https://pro.hhdrywallrepair.com" />

<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:image" content="https://pro.hhdrywallrepair.com/og-image.jpg" />
🌐 DOMAIN IMPLEMENTATION
Subdomain Setup (pro.hhdrywallrepair.com)
Step 1: Add DNS Record
Go to your domain provider (GoDaddy, Namecheap, Cloudflare):
Type:   CNAME
Name:   pro
Value:  job-trade-match.preview.emergentagent.com
TTL:    Auto (or 3600)
Step 2: Connect in Emergent Dashboard
Go to Home in Emergent
Click HhDrywall Repair project
Click "Link domain"
Enter: pro.hhdrywallrepair.com
Click "Entri" → follow prompts
Wait 5-15 minutes for SSL
Step 3: Verify
Visit: https://pro.hhdrywallrepair.com
DNS Propagation Check:
https://dnschecker.org
https://www.whatsmydns.net
🔗 HTML INTEGRATION
Navigation Links
<!-- Main Navigation -->
<nav>
  <a href="https://pro.hhdrywallrepair.com">Home</a>
  <a href="https://pro.hhdrywallrepair.com/jobs">Find Jobs</a>
  <a href="https://pro.hhdrywallrepair.com/workers">Find Workers</a>
  <a href="https://pro.hhdrywallrepair.com/shop">Pro Shop</a>
  <a href="https://pro.hhdrywallrepair.com/market-data">Market Data</a>
  <a href="https://pro.hhdrywallrepair.com/dashboard">Dashboard</a>
</nav>
Call-to-Action Buttons
<!-- Primary CTA (Orange) -->
<a href="https://pro.hhdrywallrepair.com/register" 
   style="display:inline-block; background:#f97316; color:white; 
          padding:14px 28px; text-decoration:none; font-weight:600; 
          text-transform:uppercase; border-radius:2px; 
          transition:background 0.3s ease;">
   Get Started
</a>

<!-- Secondary CTA (Dark) -->
<a href="https://pro.hhdrywallrepair.com/jobs" 
   style="display:inline-block; background:#0f172a; color:white; 
          padding:14px 28px; text-decoration:none; font-weight:600; 
          text-transform:uppercase; border-radius:2px;
          transition:background 0.3s ease;">
   Browse Jobs
</a>

<!-- Tertiary CTA (Blue) -->
<a href="https://pro.hhdrywallrepair.com/market-data" 
   style="display:inline-block; background:#3b82f6; color:white; 
          padding:14px 28px; text-decoration:none; font-weight:600; 
          text-transform:uppercase; border-radius:2px;
          transition:background 0.3s ease;">
   Market Analytics
</a>
Complete Feature Section
<section style="padding:60px 20px; background:#f8fafc;">
  <div style="max-width:1200px; margin:0 auto; text-align:center;">
    <h2 style="font-size:32px; color:#0f172a; margin-bottom:40px; font-weight:700;">
      Professional Services for Construction Pros
    </h2>
    
    <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(250px,1fr)); gap:20px;">
      
      <!-- Job Board Card -->
      <a href="https://pro.hhdrywallrepair.com/jobs" 
         style="display:block; background:white; border:1px solid #e2e8f0; 
                padding:30px; text-decoration:none; text-align:center;
                border-radius:8px; transition:all 0.3s ease;">
        <div style="width:60px; height:60px; background:#eff6ff; border-radius:50%; 
                    margin:0 auto 20px; display:flex; align-items:center; justify-content:center;">
          <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <line x1="9" y1="9" x2="15" y2="9"></line>
            <line x1="9" y1="15" x2="15" y2="15"></line>
          </svg>
        </div>
        <h3 style="color:#0f172a; margin-bottom:10px; font-weight:600;">Job Board</h3>
        <p style="color:#64748b; font-size:14px; margin-bottom:15px; line-height:1.6;">
          Find or post jobs by trade code and location
        </p>
        <span style="color:#f97316; font-weight:500;">Browse Jobs →</span>
      </a>
      
      <!-- Find Workers Card -->
      <a href="https://pro.hhdrywallrepair.com/workers" 
         style="display:block; background:white; border:1px solid #e2e8f0; 
                padding:30px; text-decoration:none; text-align:center;
                border-radius:8px; transition:all 0.3s ease;">
        <div style="width:60px; height:60px; background:#eff6ff; border-radius:50%; 
                    margin:0 auto 20px; display:flex; align-items:center; justify-content:center;">
          <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
            <circle cx="9" cy="7" r="4"></circle>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
          </svg>
        </div>
        <h3 style="color:#0f172a; margin-bottom:10px; font-weight:600;">Find Workers</h3>
        <p style="color:#64748b; font-size:14px; margin-bottom:15px; line-height:1.6;">
          Browse skilled subcontractors by trade
        </p>
        <span style="color:#f97316; font-weight:500;">View Profiles →</span>
      </a>
      
      <!-- Pro Shop Card -->
      <a href="https://pro.hhdrywallrepair.com/shop" 
         style="display:block; background:white; border:1px solid #e2e8f0; 
                padding:30px; text-decoration:none; text-align:center;
                border-radius:8px; transition:all 0.3s ease;">
        <div style="width:60px; height:60px; background:#eff6ff; border-radius:50%; 
                    margin:0 auto 20px; display:flex; align-items:center; justify-content:center;">
          <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2">
            <circle cx="9" cy="21" r="1"></circle>
            <circle cx="20" cy="21" r="1"></circle>
            <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
          </svg>
        </div>
        <h3 style="color:#0f172a; margin-bottom:10px; font-weight:600;">Pro Shop</h3>
        <p style="color:#64748b; font-size:14px; margin-bottom:15px; line-height:1.6;">
          Professional tools and supplies
        </p>
        <span style="color:#f97316; font-weight:500;">Shop Now →</span>
      </a>
      
      <!-- Market Data Card -->
      <a href="https://pro.hhdrywallrepair.com/market-data" 
         style="display:block; background:white; border:1px solid #e2e8f0; 
                padding:30px; text-decoration:none; text-align:center;
                border-radius:8px; transition:all 0.3s ease;">
        <div style="width:60px; height:60px; background:#eff6ff; border-radius:50%; 
                    margin:0 auto 20px; display:flex; align-items:center; justify-content:center;">
          <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2">
            <line x1="18" y1="20" x2="18" y2="10"></line>
            <line x1="12" y1="20" x2="12" y2="4"></line>
            <line x1="6" y1="20" x2="6" y2="14"></line>
          </svg>
        </div>
        <h3 style="color:#0f172a; margin-bottom:10px; font-weight:600;">Market Data</h3>
        <p style="color:#64748b; font-size:14px; margin-bottom:15px; line-height:1.6;">
          Construction industry analytics
        </p>
        <span style="color:#f97316; font-weight:500;">View Plans →</span>
      </a>
      
    </div>
  </div>
</section>
Hover Effects CSS
Add to your stylesheet:
/* Button Hover Effects */
a[href*="hhdrywallrepair.com"]:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
}

/* Card Hover Effects */
.feature-card:hover {
  border-color: #3b82f6;
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.12);
}
🔌 MARKET DATA REPOSITORY INTEGRATION
Repository Overview
Repository: https://github.com/Gooderman932/market-data
Copyright: Poor Dude Holdings LLC
Description: Enterprise SaaS platform for construction market intelligence
Features from Market Data Platform
Feature
Description
Project Discovery
Track opportunities, permits, and tenders
Competitive Intelligence
Analyze competitor activity and market share
Predictive Analytics
Win probability models and demand forecasting
Market Insights
Regional analysis and trend visualization
Tech Stack
Backend: Python 3.11+ with FastAPI, PostgreSQL 16, SQLAlchemy 2.0
Frontend: React 18 with TypeScript, Vite, Tailwind CSS, Recharts
ML/AI: scikit-learn, OpenAI API
Infrastructure: Docker, Redis 7, Nginx
Step 1: Clone the Repository
# Clone to your server
git clone https://github.com/Gooderman932/market-data.git
cd market-data

# Or clone to specific directory
git clone https://github.com/Gooderman932/market-data.git /opt/market-data
Step 2: Environment Configuration
# Copy example environment file
cp .env.example .env

# Edit with your configuration
nano .env
Required Environment Variables:
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
Step 3: Docker Deployment (Recommended)
# Development
make quickstart
# or
docker compose up --build

# Production
docker-compose -f docker-compose.prod.yml up -d
Access Points:
Frontend: http://localhost:5173
Backend API: http://localhost:8000
API Docs: http://localhost:8000/docs
Step 4: Manual Installation (Alternative)
Backend Setup
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
Frontend Setup
cd frontend
npm install
npm run dev
Step 5: Database Initialization
# Initialize database schema
make db-init

# Seed sample data (optional)
make db-seed

# Run migrations
cd backend
alembic upgrade head
Step 6: Default Login Credentials
After seeding:
Email: demo@example.com
Password: demo123
Market Data API Endpoints
Authentication
POST /api/auth/token        → Login
POST /api/auth/register     → Register new user
GET  /api/auth/me           → Get current user
Projects
GET    /api/projects/       → List projects (with filters)
GET    /api/projects/{id}   → Get project details
POST   /api/projects/       → Create project
PUT    /api/projects/{id}   → Update project
DELETE /api/projects/{id}   → Delete project
Analytics
GET /api/analytics/summary  → Dashboard summary
GET /api/analytics/trends   → Project trends
GET /api/analytics/regions  → Regional analysis
Intelligence
GET /api/intelligence/competitors    → Competitor data
GET /api/intelligence/market-share   → Market share analysis
GET /api/intelligence/relationships  → Relationship graph
Linking Market Data to HDrywall Platform
Option A: API Integration
Add to HDrywall backend (/app/backend/server.py):
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
Option B: Subdomain Setup
Deploy market-data platform to a subdomain:
1. Add DNS record:
Type: A or CNAME
Name: intel
Value: your-server-ip or target
2. Configure Nginx:
server {
    listen 80;
    server_name intel.hdrywallrepair.com;
    
    location / {
        proxy_pass http://localhost:5173;  # Market data frontend
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /api {
        proxy_pass http://localhost:8000;  # Market data backend
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
Access at: https://intel.hdrywallrepair.com
Option C: Embed in HDrywall Platform
Create iframe integration on market data page:
<div style="width:100%; height:800px; border:none;">
  <iframe 
      src="https://intel.hdrywallrepair.com/dashboard" 
      width="100%" 
      height="100%" 
      frameborder="0"
      allow="fullscreen"
      style="border:1px solid #e2e8f0; border-radius:8px;">
  </iframe>
</div>
Market Data Maintenance
Daily Tasks
# Update market data
cd /opt/market-data
git pull origin main
docker-compose restart

# Check health
./scripts/deployment/health-check.sh
Weekly Tasks
# Run platform automation
make run-automation

# Security scan
make security-scan

# Backup database
make backup
Database Migrations
# Create new migration
cd backend
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
Update Dependencies
# Backend
cd backend
pip install -r requirements.txt --upgrade

# Frontend
cd frontend
npm update
📦 PRODUCT ADMINISTRATION
View All Products
mongosh
use test_database
db.products.find().pretty()
Add New Product
db.products.insertOne({
  "product_id": "prod_" + Math.random().toString(36).substr(2, 12),
  "name": "Product Name",
  "description": "Product description goes here",
  "category": "Drywall Tools",
  "price": 29.99,
  "compare_price": 39.99,
  "image_url": "https://example.com/image.jpg",
  "stock": 100,
  "sku": "SKU-001",
  "active": true,
  "created_at": new Date().toISOString()
})
Available Categories:
Drywall Tools
Materials
Power Tools
Safety Gear
Blades & Accessories
Storage & Organization
Update Product Price
db.products.updateOne(
  { "name": "Product Name" },
  { $set: { "price": 49.99, "compare_price": 69.99 } }
)
Update Stock
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
Deactivate/Delete Product
// Deactivate (hide from shop)
db.products.updateOne(
  { "name": "Product Name" },
  { $set: { "active": false } }
)

// Reactivate
db.products.updateOne(
  { "product_id": "prod_abc123" },
  { $set: { "active": true } }
)

// Delete permanently
db.products.deleteOne({ "product_id": "prod_abc123" })
Bulk Price Update
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

// Update specific category
db.products.updateMany(
  { "category": "Power Tools" },
  [{ $set: { "price": { $multiply: ["$price", 1.05] } } }]
)
💰 MARKET DATA TIER ADMINISTRATION
Current Configuration
Located in /app/backend/server.py:
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
Change Tier Pricing
Edit /app/backend/server.py
Find MARKET_DATA_TIERS
Change price values:
"price": 349.00,  # Changed from 299.00
Restart backend:
sudo supervisorctl restart backend
Add/Remove Features
Edit the features array for each tier:
"features": [
    "Existing feature",
    "NEW: Added feature",  # Add new feature
    # Remove by deleting the line
]
Add New Tier
{
    "tier_id": "startup",
    "name": "Startup Plan",
    "price": 99.00,
    "billing_period": "monthly",
    "description": "Perfect for new construction businesses",
    "features": [
        "Limited regional data",
        "Basic analytics",
        "Email support",
        "Up to 25 projects"
    ]
}
👥 USER MANAGEMENT
View Users
// All users
db.users.find().pretty()

// By type
db.users.find({ "user_type": "contractor" }).pretty()
db.users.find({ "user_type": "subcontractor" }).pretty()

// By email
db.users.findOne({ "email": "user@example.com" })

// Recent registrations
db.users.find().sort({ "created_at": -1 }).limit(10).pretty()
User Statistics
// Count by type
db.users.aggregate([
  { $group: { _id: "$user_type", count: { $sum: 1 } } }
])

// Active users (with sessions)
db.user_sessions.distinct("user_id").length
Change User Type
db.users.updateOne(
  { "email": "user@example.com" },
  { $set: { "user_type": "contractor" } }
)
Update User Profile
db.users.updateOne(
  { "email": "user@example.com" },
  { 
    $set: { 
      "first_name": "John",
      "last_name": "Doe",
      "company": "ABC Construction",
      "phone": "+1-555-123-4567"
    } 
  }
)
Delete User
// Delete user
db.users.deleteOne({ "email": "user@example.com" })

// Delete associated data
db.user_sessions.deleteMany({ "user_id": "user_abc123" })
db.jobs.deleteMany({ "created_by": "user_abc123" })
db.worker_profiles.deleteMany({ "user_id": "user_abc123" })
db.orders.deleteMany({ "user_id": "user_abc123" })
💼 JOB LISTINGS MANAGEMENT
View/Search Jobs
// All jobs
db.jobs.find().pretty()

// Active jobs only
db.jobs.find({ "status": "active" }).pretty()

// By trade code
db.jobs.find({ "trade_codes": "09" }).pretty()

// By location
db.jobs.find({ "location": /Dallas/i }).pretty()

// Recent jobs
db.jobs.find().sort({ "created_at": -1 }).limit(10).pretty()
Job Statistics
// Count by status
db.jobs.aggregate([
  { $group: { _id: "$status", count: { $sum: 1 } } }
])

// Count by trade
db.jobs.aggregate([
  { $unwind: "$trade_codes" },
  { $group: { _id: "$trade_codes", count: { $sum: 1 } } }
])
Close/Reopen Job
// Close job
db.jobs.updateOne(
  { "job_id": "job_abc123" },
  { $set: { "status": "closed", "closed_at": new Date().toISOString() } }
)

// Reopen job
db.jobs.updateOne(
  { "job_id": "job_abc123" },
  { $set: { "status": "active" }, $unset: { "closed_at": "" } }
)
Delete Job
db.jobs.deleteOne({ "job_id": "job_abc123" })
👷 WORKER PROFILES MANAGEMENT
View/Search Profiles
// All profiles
db.worker_profiles.find().pretty()

// By trade code
db.worker_profiles.find({ "trade_codes": "09" }).pretty()

// By availability
db.worker_profiles.find({ "availability": "immediate" }).pretty()

// By location
db.worker_profiles.find({ "location": /Texas/i }).pretty()
Profile Statistics
// Count by availability
db.worker_profiles.aggregate([
  { $group: { _id: "$availability", count: { $sum: 1 } } }
])

// Count by trade
db.worker_profiles.aggregate([
  { $unwind: "$trade_codes" },
  { $group: { _id: "$trade_codes", count: { $sum: 1 } } }
])
Deactivate/Delete Profile
// Deactivate
db.worker_profiles.updateOne(
  { "profile_id": "profile_abc123" },
  { $set: { "status": "inactive" } }
)

// Reactivate
db.worker_profiles.updateOne(
  { "profile_id": "profile_abc123" },
  { $set: { "status": "active" } }
)

// Delete permanently
db.worker_profiles.deleteOne({ "profile_id": "profile_abc123" })
💳 ORDERS & PAYMENTS
View Transactions
// All orders
db.orders.find().pretty()

// All payment transactions
db.payment_transactions.find().pretty()

// Paid transactions only
db.payment_transactions.find({ "payment_status": "paid" }).pretty()

// Failed payments
db.payment_transactions.find({ "payment_status": "failed" }).pretty()

// Recent transactions
db.payment_transactions.find().sort({ "created_at": -1 }).limit(10).pretty()
Revenue Statistics
// Total revenue
db.payment_transactions.aggregate([
  { $match: { "payment_status": "paid" } },
  { $group: { _id: null, total: { $sum: "$amount" } } }
])

// Revenue by month
db.payment_transactions.aggregate([
  { $match: { "payment_status": "paid" } },
  { 
    $group: { 
      _id: { $substr: ["$created_at", 0, 7] },
      total: { $sum: "$amount" },
      count: { $sum: 1 }
    } 
  },
  { $sort: { _id: -1 } }
])

// Revenue by product category
db.orders.aggregate([
  { $lookup: {
      from: "products",
      localField: "product_id",
      foreignField: "product_id",
      as: "product"
  }},
  { $unwind: "$product" },
  { $group: {
      _id: "$product.category",
      total: { $sum: "$total" },
      count: { $sum: 1 }
  }}
])
💰 STRIPE CONFIGURATION
Test Mode (Default)
STRIPE_API_KEY=sk_test_emergent
Switch to Live Mode
Get your live keys from https://dashboard.stripe.com/apikeys
Update /app/backend/.env:
STRIPE_API_KEY=sk_live_your_actual_live_key
STRIPE_PUBLISHABLE_KEY=pk_live_your_actual_live_key
Restart backend:
sudo supervisorctl restart backend
Webhook Setup
Go to https://dashboard.stripe.com/webhooks
Add endpoint: https://pro.hhdrywallrepair.com/api/stripe/webhook
Select events:
payment_intent.succeeded
payment_intent.failed
charge.succeeded
charge.failed
Copy webhook secret
Update .env:
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
🔧 SYSTEM MAINTENANCE
Service Commands
# Check status
sudo supervisorctl status

# Restart services
sudo supervisorctl restart backend
sudo supervisorctl restart frontend
sudo supervisorctl restart all

# Stop services
sudo supervisorctl stop backend
sudo supervisorctl stop frontend

# Start services
sudo supervisorctl start backend
sudo supervisorctl start frontend

# Reload configuration
sudo supervisorctl reread
sudo supervisorctl update
View Logs
# Backend logs
tail -f /var/log/supervisor/backend.err.log
tail -f /var/log/supervisor/backend.out.log

# Frontend logs
tail -f /var/log/supervisor/frontend.err.log
tail -f /var/log/supervisor/frontend.out.log

# Last 50 lines
tail -n 50 /var/log/supervisor/backend.err.log

# Follow with grep filter
tail -f /var/log/supervisor/backend.err.log | grep ERROR
Environment Variables
Backend (/app/backend/.env):
# Database
MONGO_URL="mongodb://localhost:27017"
DB_NAME="test_database"

# Authentication
JWT_SECRET="your-secret-key-change-this-in-production"
JWT_ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Stripe
STRIPE_API_KEY=sk_test_emergent
STRIPE_PUBLISHABLE_KEY=pk_test_emergent
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# Market Data Integration
MARKET_DATA_API_URL="http://localhost:8000"
MARKET_DATA_API_KEY="your-api-key"

# CORS
CORS_ORIGINS="https://pro.hhdrywallrepair.com,http://localhost:3000"
Frontend (/app/frontend/.env):
VITE_API_URL=https://pro.hhdrywallrepair.com/api
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_emergent
🗄️ DATABASE OPERATIONS
Backup Database
# Full backup
mongodump --db test_database --out /app/backup/$(date +%Y%m%d)

# Specific collections
mongodump --db test_database --collection products --out /app/backup/products_$(date +%Y%m%d)

# Compressed backup
mongodump --db test_database --gzip --archive=/app/backup/db_$(date +%Y%m%d).gz
Restore Database
# Full restore
mongorestore --db test_database /app/backup/20250128/test_database/

# Specific collection
mongorestore --db test_database --collection products /app/backup/products_20250128/test_database/products.bson

# From compressed archive
mongorestore --gzip --archive=/app/backup/db_20250128.gz
Create Indexes
// User email (unique)
db.users.createIndex({ "email": 1 }, { unique: true })

// Job trade codes
db.jobs.createIndex({ "trade_codes": 1 })
db.jobs.createIndex({ "status": 1 })
db.jobs.createIndex({ "created_at": -1 })

// Products
db.products.createIndex({ "category": 1 })
db.products.createIndex({ "active": 1 })
db.products.createIndex({ "sku": 1 }, { unique: true })

// Worker profiles
db.worker_profiles.createIndex({ "trade_codes": 1 })
db.worker_profiles.createIndex({ "availability": 1 })

// Payments
db.payment_transactions.createIndex({ "payment_status": 1 })
db.payment_transactions.createIndex({ "created_at": -1 })
Database Statistics
// Database stats
db.stats()

// Collection stats
db.users.stats()
db.products.stats()
db.jobs.stats()

// Index usage
db.users.aggregate([{ $indexStats: {} }])
🔍 TROUBLESHOOTING
Common Issues & Solutions
Issue
Solution
Backend not starting
Check logs: tail -n 50 /var/log/supervisor/backend.err.log
Frontend not loading
Check logs: tail -n 50 /var/log/supervisor/frontend.err.log
Database connection failed
Run: sudo systemctl restart mongod
API returns 500
Check backend logs for Python errors
DNS not working
Wait 24-48 hours, check https://dnschecker.org
Stripe payment fails
Verify API keys in .env, check Stripe dashboard
CORS errors
Check CORS_ORIGINS in backend .env
Session expired
Clear browser cookies, login again
Images not loading
Verify image_url paths in database
Market data not showing
Check API connection and subscription status
Debug Mode
Enable debug logging:
# In /app/backend/.env
DEBUG=True
LOG_LEVEL=DEBUG
Restart backend:
sudo supervisorctl restart backend
Health Checks
# API health
curl https://pro.hhdrywallrepair.com/api/health

# Database connection
mongosh --eval "db.adminCommand('ping')"

# Service status
sudo supervisorctl status
📚 QUICK REFERENCE
URLs
Resource
URL
HhDrywall Platform
https://pro.hhdrywallrepair.com
Market Data Platform
https://intel.hhdrywallrepair.com
API Docs
https://pro.hhdrywallrepair.com/api/docs
API Health
https://pro.hhdrywallrepair.com/api/health
Platform Pages
Page
Path
Home
/
Jobs
/jobs
Workers
/workers
Shop
/shop
Market Data
/market-data
Dashboard
/dashboard
Register
/register
Login
/login
Trade Codes
Code
Trade
03
Concrete
04
Masonry
05
Metals
06
Wood, Plastics & Composites
07
Thermal & Moisture Protection
08
Openings (Doors & Windows)
09
Finishes (Drywall/Paint)
22
Plumbing
23
HVAC
26
Electrical
Quick Commands
Task
Command
Restart Backend
sudo supervisorctl restart backend
Restart Frontend
sudo supervisorctl restart frontend
View Backend Logs
tail -f /var/log/supervisor/backend.err.log
View Frontend Logs
tail -f /var/log/supervisor/frontend.err.log
MongoDB Shell
mongosh → use test_database
Backup Database
mongodump --db test_database --out /app/backup/
Check Services
sudo supervisorctl status
Update Code
cd /app && git pull && sudo supervisorctl restart all
Demo Credentials
Account Type
Email
Password
Contractor
demo@example.com
demo123
Market Data
demo@example.com
demo123
📞 CONTACT & SUPPORT
HDrywall Repair
Email: info@hdrywallrepair.com
Phone: (555) 123-4567
Website: https://hdrywallrepair.com
Platform: https://pro.hhdrywallrepair.com
Market Data Platform
Copyright: © 2025 Poor Dude Holdings LLC
Email: legal@poorduceholdings.com
Repository: https://github.com/Gooderman932/market-data
🏆 Built With
Backend: FastAPI + Python + MongoDB
Frontend: React + TypeScript + Vite + Tailwind CSS
Payments: Stripe
Hosting: Emergent Platform
Analytics: Construction Intelligence Platform
Database: MongoDB Atlas
Last Updated: January 28, 2025
Version: 2.0.0
Status: ✅ Production Ready
