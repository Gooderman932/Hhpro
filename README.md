# HDrywall Repair Pro Platform
## Complete Implementation, Administration & Maintenance Guide

Professional contractor/subcontractor job matching platform with e-commerce for hdrywallrepair.com

---

## 🌐 Live URLs

| Environment | URL |
|-------------|-----|
| **Preview** | https://job-trade-match.preview.emergentagent.com |
| **Production** | https://pro.hdrywallrepair.com (after subdomain setup) |
| **Market Data Repo** | https://github.com/Gooderman932/market-data.git |

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

## Features Summary

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
| Tier | Price | Target |
|------|-------|--------|
| Basic | $299/mo | Small contractors |
| Professional | $799/mo | Established businesses |
| Enterprise | $1999/mo | Large construction firms |

---

# DOMAIN IMPLEMENTATION

## Option A: Subdomain Setup (Recommended)

### Step 1: Add DNS Record

Go to your domain provider (GoDaddy, Namecheap, Cloudflare, etc.):

```
Type:   CNAME
Name:   pro
Value:  job-trade-match.preview.emergentagent.com
TTL:    Auto (or 3600)
```

**Provider-Specific:**

| Provider | Path |
|----------|------|
| GoDaddy | My Products → DNS → Add Record → CNAME |
| Namecheap | Domain List → Manage → Advanced DNS → Add New Record |
| Cloudflare | DNS → Add Record (Proxy: OFF initially) |

### Step 2: Connect in Emergent

1. Go to **Home** in Emergent
2. Click **HDrywall Repair** project
3. Click **"Link domain"**
4. Enter: `pro.hdrywallrepair.com`
5. Click **"Entri"** → follow prompts
6. Wait 5-15 minutes for SSL

### Step 3: Verify

Visit `https://pro.hdrywallrepair.com`

**Troubleshooting:**
- Check: https://dnschecker.org
- Remove conflicting A records
- Re-link domain if needed

---

## Option B: Path-Based Redirects

Add to your server config on hdrywallrepair.com:

**Apache (.htaccess):**
```apache
RewriteEngine On
RewriteRule ^jobs/?$ https://pro.hdrywallrepair.com/jobs [R=301,L]
RewriteRule ^workers/?$ https://pro.hdrywallrepair.com/workers [R=301,L]
RewriteRule ^shop/?$ https://pro.hdrywallrepair.com/shop [R=301,L]
RewriteRule ^market-data/?$ https://pro.hdrywallrepair.com/market-data [R=301,L]
```

**Nginx:**
```nginx
location /jobs { return 301 https://pro.hdrywallrepair.com/jobs; }
location /workers { return 301 https://pro.hdrywallrepair.com/workers; }
location /shop { return 301 https://pro.hdrywallrepair.com/shop; }
location /market-data { return 301 https://pro.hdrywallrepair.com/market-data; }
```

---

# HTML INTEGRATION

## Navigation Links

```html
<a href="https://pro.hdrywallrepair.com/jobs">Find Jobs</a>
<a href="https://pro.hdrywallrepair.com/workers">Find Workers</a>
<a href="https://pro.hdrywallrepair.com/shop">Pro Shop</a>
<a href="https://pro.hdrywallrepair.com/market-data">Market Data</a>
```

## Call-to-Action Buttons

```html
<!-- Orange "Get Started" Button -->
<a href="https://pro.hdrywallrepair.com/register" 
   style="display:inline-block; background:#f97316; color:white; 
          padding:14px 28px; text-decoration:none; font-weight:600; 
          text-transform:uppercase; border-radius:2px;">
   Get Started
</a>

<!-- Dark "Browse Jobs" Button -->
<a href="https://pro.hdrywallrepair.com/jobs" 
   style="display:inline-block; background:#0f172a; color:white; 
          padding:14px 28px; text-decoration:none; font-weight:600; 
          text-transform:uppercase; border-radius:2px;">
   Browse Jobs
</a>

<!-- Dark "Find Workers" Button -->
<a href="https://pro.hdrywallrepair.com/workers" 
   style="display:inline-block; background:#0f172a; color:white; 
          padding:14px 28px; text-decoration:none; font-weight:600; 
          text-transform:uppercase; border-radius:2px;">
   Find Workers
</a>

<!-- Orange "Shop Tools" Button -->
<a href="https://pro.hdrywallrepair.com/shop" 
   style="display:inline-block; background:#f97316; color:white; 
          padding:14px 28px; text-decoration:none; font-weight:600; 
          text-transform:uppercase; border-radius:2px;">
   Shop Tools
</a>

<!-- Market Data Button -->
<a href="https://pro.hdrywallrepair.com/market-data" 
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
      
      <a href="https://pro.hdrywallrepair.com/jobs" 
         style="display:block; background:white; border:1px solid #e2e8f0; 
                padding:30px; text-decoration:none; text-align:center;">
        <h3 style="color:#0f172a; margin-bottom:10px;">Job Board</h3>
        <p style="color:#64748b; font-size:14px; margin-bottom:15px;">
          Find or post jobs by trade code and location
        </p>
        <span style="color:#f97316; font-weight:500;">Browse Jobs →</span>
      </a>
      
      <a href="https://pro.hdrywallrepair.com/workers" 
         style="display:block; background:white; border:1px solid #e2e8f0; 
                padding:30px; text-decoration:none; text-align:center;">
        <h3 style="color:#0f172a; margin-bottom:10px;">Find Workers</h3>
        <p style="color:#64748b; font-size:14px; margin-bottom:15px;">
          Browse skilled subcontractors by trade
        </p>
        <span style="color:#f97316; font-weight:500;">View Profiles →</span>
      </a>
      
      <a href="https://pro.hdrywallrepair.com/shop" 
         style="display:block; background:white; border:1px solid #e2e8f0; 
                padding:30px; text-decoration:none; text-align:center;">
        <h3 style="color:#0f172a; margin-bottom:10px;">Pro Shop</h3>
        <p style="color:#64748b; font-size:14px; margin-bottom:15px;">
          Professional tools and supplies
        </p>
        <span style="color:#f97316; font-weight:500;">Shop Now →</span>
      </a>
      
      <a href="https://pro.hdrywallrepair.com/market-data" 
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

## Hero Banner

```html
<section style="background:linear-gradient(to bottom right,#0f172a,#1e293b); 
                color:white; padding:80px 20px; text-align:center;">
  <div style="max-width:800px; margin:0 auto;">
    <span style="display:inline-block; background:rgba(249,115,22,0.2); 
                 color:#fb923c; padding:6px 16px; font-size:12px; 
                 text-transform:uppercase; letter-spacing:1px; 
                 border-radius:2px; margin-bottom:20px;">
      The Pro's Network
    </span>
    <h1 style="font-size:48px; text-transform:uppercase; margin-bottom:20px; line-height:1.1;">
      Connect With Skilled <span style="color:#f97316;">Tradespeople</span>
    </h1>
    <p style="font-size:18px; color:#94a3b8; margin-bottom:32px;">
      The premier platform for contractors seeking subcontractors and skilled workers.
    </p>
    <div style="display:flex; gap:16px; justify-content:center; flex-wrap:wrap;">
      <a href="https://pro.hdrywallrepair.com/register" 
         style="display:inline-block; background:#f97316; color:white; 
                padding:16px 32px; text-decoration:none; font-weight:600; 
                text-transform:uppercase; border-radius:2px;">
        Get Started →
      </a>
      <a href="https://pro.hdrywallrepair.com/jobs" 
         style="display:inline-block; background:transparent; border:2px solid white; 
                color:white; padding:16px 32px; text-decoration:none; font-weight:600; 
                text-transform:uppercase; border-radius:2px;">
        Browse Jobs
      </a>
    </div>
  </div>
</section>
```

## Footer Links

```html
<div style="display:flex; gap:24px; flex-wrap:wrap;">
  <a href="https://pro.hdrywallrepair.com/jobs" style="color:#94a3b8; text-decoration:none;">Job Board</a>
  <a href="https://pro.hdrywallrepair.com/workers" style="color:#94a3b8; text-decoration:none;">Find Workers</a>
  <a href="https://pro.hdrywallrepair.com/shop" style="color:#94a3b8; text-decoration:none;">Pro Shop</a>
  <a href="https://pro.hdrywallrepair.com/market-data" style="color:#94a3b8; text-decoration:none;">Market Data</a>
</div>
```

---

# MARKET DATA REPOSITORY INTEGRATION

## Repository: Gooderman932/market-data

### Step 1: Clone the Repository

```bash
# Clone to your local machine or server
git clone https://github.com/Gooderman932/market-data.git

# Or if private, use SSH
git clone git@github.com:Gooderman932/market-data.git

# Or with token
git clone https://<your-token>@github.com/Gooderman932/market-data.git
```

### Step 2: If Repository is Private

**Generate Personal Access Token:**
1. Go to GitHub → Settings → Developer Settings → Personal Access Tokens
2. Generate new token with `repo` scope
3. Use token in clone URL:
```bash
git clone https://YOUR_TOKEN@github.com/Gooderman932/market-data.git
```

### Step 3: Link to Platform

**Option A: Submodule Integration**
```bash
cd /app
git submodule add https://github.com/Gooderman932/market-data.git market-data
git commit -m "Add market-data submodule"
```

**Option B: Direct Integration**
```bash
# Copy market data files into platform
cp -r /path/to/market-data/src/* /app/backend/market_data/
```

### Step 4: Update Backend to Use Market Data

Edit `/app/backend/server.py` to import market data:

```python
# Add at top of file
from market_data import analytics, reports, trends

# Add new endpoints
@api_router.get("/market-data/analytics/{tier_id}")
async def get_market_analytics(tier_id: str, request: Request):
    """Get analytics data based on subscription tier"""
    user = await require_user(request)
    
    # Verify user has subscription
    subscription = await db.subscriptions.find_one({
        "user_id": user["user_id"],
        "tier_id": tier_id,
        "status": "active"
    }, {"_id": 0})
    
    if not subscription:
        raise HTTPException(status_code=403, detail="Subscription required")
    
    # Return data based on tier
    if tier_id == "basic":
        return analytics.get_basic_data()
    elif tier_id == "professional":
        return analytics.get_professional_data()
    elif tier_id == "enterprise":
        return analytics.get_enterprise_data()
```

### Step 5: Update Market Data from Repository

```bash
# If using submodule
cd /app
git submodule update --remote market-data

# If direct integration
cd /path/to/market-data
git pull origin main
cp -r src/* /app/backend/market_data/
```

### Step 6: Configure Market Data Environment

Add to `/app/backend/.env`:
```env
MARKET_DATA_API_KEY=your_api_key_if_needed
MARKET_DATA_UPDATE_INTERVAL=3600
MARKET_DATA_CACHE_TTL=300
```

### Market Data Maintenance Schedule

| Task | Frequency | Command |
|------|-----------|---------|
| Update data | Daily | `git submodule update --remote` |
| Clear cache | Weekly | `db.market_cache.drop()` |
| Verify data | Monthly | Run validation scripts |
| Full refresh | Quarterly | Re-clone and rebuild |

---

# PRODUCT ADMINISTRATION

## View All Products

```javascript
mongosh
use test_database
db.products.find().pretty()
```

**API:**
```bash
curl https://pro.hdrywallrepair.com/api/products
```

## Add New Product

```javascript
mongosh
use test_database

db.products.insertOne({
  "product_id": "prod_" + Math.random().toString(36).substr(2, 12),
  "name": "Product Name Here",
  "description": "Product description",
  "category": "Drywall Tools",
  "price": 29.99,
  "compare_price": 39.99,
  "image_url": "https://your-image-url.com/image.jpg",
  "stock": 100,
  "sku": "SKU-001",
  "active": true,
  "created_at": new Date().toISOString()
})
```

**Categories Available:**
- Drywall Tools
- Materials
- Power Tools
- Safety Gear
- Blades & Accessories
- Storage & Organization

## Update Product Price

```javascript
// By name
db.products.updateOne(
  { "name": "Product Name" },
  { $set: { "price": 49.99, "compare_price": 69.99 } }
)

// By ID
db.products.updateOne(
  { "product_id": "prod_abc123" },
  { $set: { "price": 49.99 } }
)
```

## Update Stock

```javascript
// Set specific level
db.products.updateOne(
  { "product_id": "prod_abc123" },
  { $set: { "stock": 100 } }
)

// Decrease (after sale)
db.products.updateOne(
  { "product_id": "prod_abc123" },
  { $inc: { "stock": -5 } }
)

// Increase (after restock)
db.products.updateOne(
  { "product_id": "prod_abc123" },
  { $inc: { "stock": 50 } }
)
```

## Deactivate/Activate Product

```javascript
// Hide from shop
db.products.updateOne(
  { "name": "Product Name" },
  { $set: { "active": false } }
)

// Show again
db.products.updateOne(
  { "name": "Product Name" },
  { $set: { "active": true } }
)
```

## Delete Product

```javascript
db.products.deleteOne({ "product_id": "prod_abc123" })
```

## Change Category

```javascript
db.products.updateOne(
  { "name": "Product Name" },
  { $set: { "category": "Power Tools" } }
)
```

## Add New Category

Use any new category name - it appears automatically:
```javascript
db.products.insertOne({
  ...
  "category": "New Category Name",
  ...
})
```

## Bulk Price Update

```javascript
// Increase all prices by 10%
db.products.updateMany(
  {},
  [{ $set: { "price": { $multiply: ["$price", 1.10] } } }]
)

// Decrease all prices by 15%
db.products.updateMany(
  {},
  [{ $set: { "price": { $multiply: ["$price", 0.85] } } }]
)

// Update specific category
db.products.updateMany(
  { "category": "Drywall Tools" },
  [{ $set: { "price": { $multiply: ["$price", 1.05] } } }]
)
```

## Bulk Stock Update

```javascript
// Set all products to specific stock
db.products.updateMany(
  {},
  { $set: { "stock": 100 } }
)

// Mark low stock items
db.products.find({ "stock": { $lt: 10 } }).pretty()
```

## Import Products from CSV/JSON

```bash
# JSON import
mongoimport --db test_database --collection products --file products.json --jsonArray

# CSV import
mongoimport --db test_database --collection products --type csv --headerline --file products.csv
```

**JSON format:**
```json
[
  {
    "product_id": "prod_001",
    "name": "Product 1",
    "description": "Description",
    "category": "Drywall Tools",
    "price": 29.99,
    "compare_price": null,
    "image_url": "https://example.com/img.jpg",
    "stock": 100,
    "sku": "SKU-001",
    "active": true
  }
]
```

---

# MARKET DATA TIER ADMINISTRATION

## Current Tier Configuration

Located in `/app/backend/server.py` (search for `MARKET_DATA_TIERS`):

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
            "Email support"
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
            "Priority support"
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
            "Dedicated account manager",
            "White-label reports",
            "24/7 phone support"
        ]
    }
]
```

## Change Tier Pricing

**Step 1:** Edit `/app/backend/server.py`

```python
# Change Basic from $299 to $349
"price": 349.00,

# Change Professional from $799 to $899
"price": 899.00,

# Change Enterprise from $1999 to $2499
"price": 2499.00,
```

**Step 2:** Restart backend
```bash
sudo supervisorctl restart backend
```

## Add Tier Features

```python
{
    "tier_id": "professional",
    "features": [
        "All Basic features",
        "National market data",
        "Real-time wage tracking",
        "Competitor analysis",
        "Custom report generation",
        "Priority support",
        "NEW: Quarterly business reviews",  # Add new feature
        "NEW: Market forecasting"           # Add another
    ]
}
```

## Remove Tier Features

Simply delete the line from the features array.

## Change Tier Name/Description

```python
{
    "tier_id": "basic",
    "name": "Starter Plan",  # Changed
    "description": "Perfect for small contractors getting started",  # Changed
    ...
}
```

## Add New Tier

```python
MARKET_DATA_TIERS = [
    # ... existing tiers ...
    {
        "tier_id": "premium",
        "name": "Premium Plus",
        "price": 1299.00,
        "billing_period": "monthly",
        "description": "Enhanced features for mid-size firms",
        "features": [
            "All Professional features",
            "Quarterly strategy sessions",
            "Custom dashboards",
            "Phone support"
        ]
    }
]
```

## Change Billing Period

```python
{
    "tier_id": "basic",
    "price": 2999.00,
    "billing_period": "yearly",  # Changed from monthly
    ...
}
```

## Tier Pricing History (Track Changes)

Create `/app/backend/tier_pricing_history.md`:
```markdown
# Tier Pricing History

| Date | Tier | Old Price | New Price | Reason |
|------|------|-----------|-----------|--------|
| 2025-01-17 | Basic | $299 | $299 | Initial |
| 2025-01-17 | Professional | $799 | $799 | Initial |
| 2025-01-17 | Enterprise | $1999 | $1999 | Initial |
```

---

# USER MANAGEMENT

## View All Users

```javascript
mongosh
use test_database

db.users.find().pretty()
```

## View by Type

```javascript
// Contractors only
db.users.find({ "user_type": "contractor" }).pretty()

// Subcontractors only
db.users.find({ "user_type": "subcontractor" }).pretty()
```

## Search Users

```javascript
// By email
db.users.findOne({ "email": "user@example.com" })

// By name (partial match)
db.users.find({ "name": { $regex: "John", $options: "i" } }).pretty()
```

## Change User Type

```javascript
db.users.updateOne(
  { "email": "user@example.com" },
  { $set: { "user_type": "contractor" } }
)
```

## Update User Info

```javascript
db.users.updateOne(
  { "email": "user@example.com" },
  { $set: { "name": "New Name", "picture": "https://new-picture.jpg" } }
)
```

## Delete User

```javascript
// Delete user
db.users.deleteOne({ "email": "user@example.com" })

// Also delete their sessions
db.user_sessions.deleteMany({ "user_id": "user_abc123" })

// Delete their profile if subcontractor
db.worker_profiles.deleteOne({ "user_id": "user_abc123" })

// Delete their jobs if contractor
db.jobs.deleteMany({ "contractor_id": "user_abc123" })
```

## User Statistics

```javascript
// Total users
db.users.countDocuments()

// By type
db.users.countDocuments({ "user_type": "contractor" })
db.users.countDocuments({ "user_type": "subcontractor" })

// Recent signups (last 7 days)
db.users.countDocuments({
  "created_at": { $gte: new Date(Date.now() - 7*24*60*60*1000).toISOString() }
})
```

---

# JOB LISTINGS MANAGEMENT

## View All Jobs

```javascript
db.jobs.find().pretty()
```

## View Active Jobs

```javascript
db.jobs.find({ "status": "active" }).pretty()
```

## Search Jobs

```javascript
// By trade code
db.jobs.find({ "trade_codes": "09" }).pretty()

// By location
db.jobs.find({ "state": "TX" }).pretty()

// By contractor
db.jobs.find({ "contractor_id": "user_abc123" }).pretty()
```

## Close a Job

```javascript
db.jobs.updateOne(
  { "job_id": "job_abc123" },
  { $set: { "status": "closed" } }
)
```

## Reopen a Job

```javascript
db.jobs.updateOne(
  { "job_id": "job_abc123" },
  { $set: { "status": "active" } }
)
```

## Update Job Details

```javascript
db.jobs.updateOne(
  { "job_id": "job_abc123" },
  { $set: { 
    "pay_rate": "30",
    "duration": "3 weeks"
  }}
)
```

## Delete a Job

```javascript
db.jobs.deleteOne({ "job_id": "job_abc123" })
```

## Job Statistics

```javascript
// Total jobs
db.jobs.countDocuments()

// Active jobs
db.jobs.countDocuments({ "status": "active" })

// Jobs by trade code
db.jobs.aggregate([
  { $unwind: "$trade_codes" },
  { $group: { _id: "$trade_codes", count: { $sum: 1 } } },
  { $sort: { count: -1 } }
])

// Jobs by state
db.jobs.aggregate([
  { $group: { _id: "$state", count: { $sum: 1 } } },
  { $sort: { count: -1 } }
])
```

---

# WORKER PROFILES MANAGEMENT

## View All Profiles

```javascript
db.worker_profiles.find().pretty()
```

## View Active Profiles

```javascript
db.worker_profiles.find({ "status": "active" }).pretty()
```

## Search Profiles

```javascript
// By trade code
db.worker_profiles.find({ "trade_codes": "09" }).pretty()

// By location
db.worker_profiles.find({ "state": "TX" }).pretty()

// By availability
db.worker_profiles.find({ "availability": "immediate" }).pretty()

// By experience (5+ years)
db.worker_profiles.find({ "experience_years": { $gte: 5 } }).pretty()
```

## Deactivate Profile

```javascript
db.worker_profiles.updateOne(
  { "profile_id": "profile_abc123" },
  { $set: { "status": "inactive" } }
)
```

## Reactivate Profile

```javascript
db.worker_profiles.updateOne(
  { "profile_id": "profile_abc123" },
  { $set: { "status": "active" } }
)
```

## Delete Profile

```javascript
db.worker_profiles.deleteOne({ "profile_id": "profile_abc123" })
```

## Profile Statistics

```javascript
// Total profiles
db.worker_profiles.countDocuments()

// Active profiles
db.worker_profiles.countDocuments({ "status": "active" })

// By trade code
db.worker_profiles.aggregate([
  { $unwind: "$trade_codes" },
  { $group: { _id: "$trade_codes", count: { $sum: 1 } } },
  { $sort: { count: -1 } }
])

// Average experience
db.worker_profiles.aggregate([
  { $group: { _id: null, avgExp: { $avg: "$experience_years" } } }
])
```

---

# ORDERS & PAYMENTS

## View All Orders

```javascript
db.orders.find().pretty()
```

## View Payment Transactions

```javascript
db.payment_transactions.find().pretty()
```

## View Paid Only

```javascript
db.payment_transactions.find({ "payment_status": "paid" }).pretty()
```

## View Market Data Subscriptions

```javascript
db.payment_transactions.find({ "type": "market_data_subscription" }).pretty()
```

## Revenue Statistics

```javascript
// Total revenue
db.payment_transactions.aggregate([
  { $match: { "payment_status": "paid" } },
  { $group: { _id: null, total: { $sum: "$amount" } } }
])

// Revenue by type
db.payment_transactions.aggregate([
  { $match: { "payment_status": "paid" } },
  { $group: { _id: "$type", total: { $sum: "$amount" } } }
])

// Revenue by month
db.payment_transactions.aggregate([
  { $match: { "payment_status": "paid" } },
  { $group: { 
    _id: { $substr: ["$created_at", 0, 7] },
    total: { $sum: "$amount" },
    count: { $sum: 1 }
  }},
  { $sort: { _id: -1 } }
])
```

## Refund a Transaction

```javascript
db.payment_transactions.updateOne(
  { "transaction_id": "txn_abc123" },
  { $set: { "status": "refunded", "payment_status": "refunded" } }
)
```

---

# STRIPE CONFIGURATION

## Current Setup (Test Mode)

Located in `/app/backend/.env`:
```env
STRIPE_API_KEY=sk_test_emergent
```

## Switch to Live Mode

**Step 1:** Get live keys from https://dashboard.stripe.com/apikeys

**Step 2:** Update `/app/backend/.env`:
```env
STRIPE_API_KEY=sk_live_your_live_key_here
```

**Step 3:** Restart backend:
```bash
sudo supervisorctl restart backend
```

## Stripe Dashboard Links

| Task | URL |
|------|-----|
| View Payments | https://dashboard.stripe.com/payments |
| View Customers | https://dashboard.stripe.com/customers |
| API Keys | https://dashboard.stripe.com/apikeys |
| Webhooks | https://dashboard.stripe.com/webhooks |
| Test Mode | https://dashboard.stripe.com/test/payments |

## Configure Webhooks (Optional)

1. Go to https://dashboard.stripe.com/webhooks
2. Add endpoint: `https://pro.hdrywallrepair.com/api/webhook/stripe`
3. Select events: `checkout.session.completed`, `payment_intent.succeeded`

---

# SYSTEM MAINTENANCE

## Service Commands

```bash
# Check status
sudo supervisorctl status

# Restart backend
sudo supervisorctl restart backend

# Restart frontend
sudo supervisorctl restart frontend

# Restart both
sudo supervisorctl restart all

# Stop service
sudo supervisorctl stop backend

# Start service
sudo supervisorctl start backend
```

## View Logs

```bash
# Backend errors
tail -f /var/log/supervisor/backend.err.log

# Backend output
tail -f /var/log/supervisor/backend.out.log

# Frontend errors
tail -f /var/log/supervisor/frontend.err.log

# Last 100 lines
tail -n 100 /var/log/supervisor/backend.err.log
```

## Clear Logs

```bash
# Truncate logs
> /var/log/supervisor/backend.err.log
> /var/log/supervisor/backend.out.log
> /var/log/supervisor/frontend.err.log
> /var/log/supervisor/frontend.out.log
```

## Update Dependencies

**Backend:**
```bash
cd /app/backend
pip install -r requirements.txt
sudo supervisorctl restart backend
```

**Frontend:**
```bash
cd /app/frontend
yarn install
sudo supervisorctl restart frontend
```

## Environment Variables

**Backend** (`/app/backend/.env`):
```env
MONGO_URL="mongodb://localhost:27017"
DB_NAME="test_database"
CORS_ORIGINS="*"
JWT_SECRET="your-secret-key"
STRIPE_API_KEY=sk_test_emergent
```

**Frontend** (`/app/frontend/.env`):
```env
REACT_APP_BACKEND_URL=https://pro.hdrywallrepair.com
```

After changing `.env`, restart the service:
```bash
sudo supervisorctl restart backend
sudo supervisorctl restart frontend
```

---

# DATABASE OPERATIONS

## Connect to MongoDB

```bash
mongosh
use test_database
```

## Backup Database

```bash
# Full backup
mongodump --db test_database --out /app/backup/$(date +%Y%m%d)

# Specific collection
mongodump --db test_database --collection products --out /app/backup/

# Compressed
mongodump --db test_database --archive=/app/backup/db_$(date +%Y%m%d).gz --gzip
```

## Restore Database

```bash
# Full restore
mongorestore --db test_database /app/backup/20250117/test_database/

# Specific collection
mongorestore --db test_database --collection products /app/backup/test_database/products.bson

# From compressed
mongorestore --archive=/app/backup/db_20250117.gz --gzip
```

## Export to JSON

```bash
mongoexport --db test_database --collection products --out products.json
mongoexport --db test_database --collection users --out users.json
mongoexport --db test_database --collection jobs --out jobs.json
```

## Import from JSON

```bash
mongoimport --db test_database --collection products --file products.json
```

## Database Statistics

```javascript
mongosh
use test_database

// Collection stats
db.stats()

// Collection sizes
db.products.countDocuments()
db.users.countDocuments()
db.jobs.countDocuments()
db.worker_profiles.countDocuments()
db.orders.countDocuments()
db.payment_transactions.countDocuments()
```

## Create Indexes (Performance)

```javascript
// Users
db.users.createIndex({ "email": 1 }, { unique: true })
db.users.createIndex({ "user_id": 1 }, { unique: true })

// Jobs
db.jobs.createIndex({ "job_id": 1 }, { unique: true })
db.jobs.createIndex({ "trade_codes": 1 })
db.jobs.createIndex({ "state": 1 })
db.jobs.createIndex({ "status": 1 })

// Profiles
db.worker_profiles.createIndex({ "profile_id": 1 }, { unique: true })
db.worker_profiles.createIndex({ "trade_codes": 1 })
db.worker_profiles.createIndex({ "status": 1 })

// Products
db.products.createIndex({ "product_id": 1 }, { unique: true })
db.products.createIndex({ "category": 1 })
db.products.createIndex({ "active": 1 })
```

---

# TROUBLESHOOTING

## Common Issues

### Backend Not Starting

```bash
# Check logs
tail -n 50 /var/log/supervisor/backend.err.log

# Common fixes
cd /app/backend
pip install -r requirements.txt
sudo supervisorctl restart backend
```

### Frontend Not Loading

```bash
# Check logs
tail -n 50 /var/log/supervisor/frontend.err.log

# Common fixes
cd /app/frontend
yarn install
sudo supervisorctl restart frontend
```

### Database Connection Failed

```bash
# Check MongoDB status
sudo systemctl status mongod

# Restart MongoDB
sudo systemctl restart mongod

# Verify connection
mongosh --eval "db.adminCommand('ping')"
```

### API Returns 500 Error

```bash
# Check backend logs
tail -n 100 /var/log/supervisor/backend.err.log

# Look for Python errors
grep -i "error\|exception" /var/log/supervisor/backend.err.log
```

### Stripe Checkout Not Working

1. Verify API key in `/app/backend/.env`
2. Check Stripe dashboard for errors
3. Ensure webhook URL is correct

### DNS/Domain Not Working

1. Check propagation: https://dnschecker.org
2. Remove conflicting A records
3. Re-link in Emergent dashboard
4. Wait up to 48 hours for full propagation

---

# QUICK REFERENCE

## URLs

| Resource | URL |
|----------|-----|
| Platform | https://pro.hdrywallrepair.com |
| API Health | https://pro.hdrywallrepair.com/api/health |
| Products API | https://pro.hdrywallrepair.com/api/products |
| Jobs API | https://pro.hdrywallrepair.com/api/jobs |
| Profiles API | https://pro.hdrywallrepair.com/api/profiles |
| Tiers API | https://pro.hdrywallrepair.com/api/market-data/tiers |

## Platform Pages

| Page | Path |
|------|------|
| Home | `/` |
| Jobs | `/jobs` |
| Post Job | `/post-job` |
| Workers | `/workers` |
| Create Profile | `/create-profile` |
| Shop | `/shop` |
| Cart | `/cart` |
| Market Data | `/market-data` |
| Login | `/login` |
| Register | `/register` |
| Dashboard | `/dashboard` |

## Trade Codes

| Code | Trade |
|------|-------|
| 03 | Concrete |
| 04 | Masonry |
| 05 | Metals |
| 06 | Wood, Plastics, Composites |
| 07 | Thermal & Moisture Protection |
| 08 | Openings (Doors/Windows) |
| 09 | Finishes (Drywall/Paint) |
| 10 | Specialties |
| 22 | Plumbing |
| 23 | HVAC |
| 26 | Electrical |
| 31 | Earthwork |
| 32 | Exterior Improvements |

## Quick Commands

| Task | Command |
|------|---------|
| Restart Backend | `sudo supervisorctl restart backend` |
| Restart Frontend | `sudo supervisorctl restart frontend` |
| View Backend Logs | `tail -f /var/log/supervisor/backend.err.log` |
| Access MongoDB | `mongosh` → `use test_database` |
| Check Services | `sudo supervisorctl status` |
| Backup Database | `mongodump --db test_database --out /app/backup/` |

## File Locations

| File | Path |
|------|------|
| Backend Code | `/app/backend/server.py` |
| Backend Env | `/app/backend/.env` |
| Frontend App | `/app/frontend/src/App.js` |
| Frontend Env | `/app/frontend/.env` |
| This README | `/app/README.md` |

---

## Contact

**Email:** info@hdrywallrepair.com  
**Phone:** (555) 123-4567

---

*Built with FastAPI + React + MongoDB on Emergent Platform*
*Last Updated: January 2025*
