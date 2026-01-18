# HDrywall Repair Pro Platform

Professional contractor/subcontractor job matching platform with e-commerce for hdrywallrepair.com

## 🌐 Live URLs

| Environment | URL |
|-------------|-----|
| **Preview** | https://job-trade-match.preview.emergentagent.com |
| **Production** | https://pro.hdrywallrepair.com (after subdomain setup) |

---

## 📋 Platform Features

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
- Shopping cart
- Stripe checkout integration

### Market Data Analytics (3 Tiers)
| Tier | Price | Features |
|------|-------|----------|
| Basic | $299/mo | Regional trends, wage analytics, monthly reports |
| Professional | $799/mo | National data, real-time tracking, competitor analysis |
| Enterprise | $1999/mo | API access, custom integrations, predictive analytics |

---

# 🔧 IMPLEMENTATION GUIDE

## Part 1: Domain Integration with hdrywallrepair.com

### Option A: Subdomain Setup (Recommended)

**Step 1: Add DNS Record**

Go to your domain provider (GoDaddy, Namecheap, Cloudflare, etc.) and add:

```
Type:   CNAME
Name:   pro
Value:  job-trade-match.preview.emergentagent.com
TTL:    Auto (or 3600)
```

**Provider-Specific Instructions:**

| Provider | Navigation Path |
|----------|-----------------|
| GoDaddy | My Products → DNS → Add Record → CNAME |
| Namecheap | Domain List → Manage → Advanced DNS → Add New Record |
| Cloudflare | DNS → Add Record (Proxy: OFF initially) |

**Step 2: Connect in Emergent Dashboard**

1. Go to **Home** in Emergent interface
2. Click on **HDrywall Repair** project
3. Click **"Link domain"**
4. Enter: `pro.hdrywallrepair.com`
5. Click **"Entri"** and follow prompts
6. Wait 5-15 minutes for SSL certificate

**Step 3: Verify**

Visit `https://pro.hdrywallrepair.com` - should load the platform.

**Troubleshooting:**
- Check DNS propagation: https://dnschecker.org
- Remove conflicting A records for "pro" subdomain
- Re-link domain if needed

---

### Option B: Link from Main Site (No Subdomain)

If you prefer to keep the preview URL and just link from your main site:

**Add Navigation Links:**
```html
<a href="https://job-trade-match.preview.emergentagent.com/jobs">Find Jobs</a>
<a href="https://job-trade-match.preview.emergentagent.com/workers">Find Workers</a>
<a href="https://job-trade-match.preview.emergentagent.com/shop">Pro Shop</a>
<a href="https://job-trade-match.preview.emergentagent.com/market-data">Market Data</a>
```

---

## Part 2: HTML Code for hdrywallrepair.com

### Navigation Links (Add to Menu)

```html
<a href="https://pro.hdrywallrepair.com/jobs">Find Jobs</a>
<a href="https://pro.hdrywallrepair.com/workers">Find Workers</a>
<a href="https://pro.hdrywallrepair.com/shop">Pro Shop</a>
<a href="https://pro.hdrywallrepair.com/market-data">Market Data</a>
```

### Call-to-Action Buttons

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
```

### Complete Feature Section (For Homepage)

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

### Hero Banner Section

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

### Footer Links

```html
<div style="display:flex; gap:24px; flex-wrap:wrap;">
  <a href="https://pro.hdrywallrepair.com/jobs" style="color:#94a3b8; text-decoration:none; font-size:14px;">Job Board</a>
  <a href="https://pro.hdrywallrepair.com/workers" style="color:#94a3b8; text-decoration:none; font-size:14px;">Find Workers</a>
  <a href="https://pro.hdrywallrepair.com/shop" style="color:#94a3b8; text-decoration:none; font-size:14px;">Pro Shop</a>
  <a href="https://pro.hdrywallrepair.com/market-data" style="color:#94a3b8; text-decoration:none; font-size:14px;">Market Data</a>
</div>
```

---

# 🛠️ ADMINISTRATION GUIDE

## Product Management (Pro Shop)

### View All Products

**Using MongoDB Shell:**
```bash
mongosh
use test_database
db.products.find().pretty()
```

**Using API (curl):**
```bash
curl https://pro.hdrywallrepair.com/api/products
```

---

### Add New Product

**Using MongoDB Shell:**
```javascript
mongosh
use test_database

db.products.insertOne({
  "product_id": "prod_" + Math.random().toString(36).substr(2, 12),
  "name": "Your Product Name",
  "description": "Product description here",
  "category": "Drywall Tools",  // Options: Drywall Tools, Materials, Power Tools, Safety Gear, Blades & Accessories, Storage & Organization
  "price": 29.99,
  "compare_price": 39.99,  // Optional: shows "Sale" badge if higher than price
  "image_url": "https://your-image-url.com/image.jpg",
  "stock": 100,
  "sku": "YOUR-SKU-001",
  "active": true,
  "created_at": new Date().toISOString()
})
```

**Using API (curl):**
```bash
curl -X POST https://pro.hdrywallrepair.com/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Your Product Name",
    "description": "Product description",
    "category": "Drywall Tools",
    "price": 29.99,
    "compare_price": 39.99,
    "image_url": "https://your-image-url.com/image.jpg",
    "stock": 100,
    "sku": "YOUR-SKU-001"
  }'
```

---

### Update Product Price

**Using MongoDB Shell:**
```javascript
mongosh
use test_database

// Update by product name
db.products.updateOne(
  { "name": "Professional Drywall Taping Knife Set" },
  { $set: { "price": 49.99, "compare_price": 69.99 } }
)

// Update by product_id
db.products.updateOne(
  { "product_id": "prod_abc123xyz" },
  { $set: { "price": 49.99 } }
)
```

---

### Update Product Stock

```javascript
mongosh
use test_database

// Set specific stock level
db.products.updateOne(
  { "name": "Mesh Drywall Tape - 300ft Roll" },
  { $set: { "stock": 250 } }
)

// Decrease stock by amount (after sale)
db.products.updateOne(
  { "product_id": "prod_abc123xyz" },
  { $inc: { "stock": -5 } }
)

// Increase stock (after restock)
db.products.updateOne(
  { "product_id": "prod_abc123xyz" },
  { $inc: { "stock": 100 } }
)
```

---

### Deactivate/Activate Product

```javascript
mongosh
use test_database

// Hide product from shop (deactivate)
db.products.updateOne(
  { "name": "Product To Hide" },
  { $set: { "active": false } }
)

// Show product again (activate)
db.products.updateOne(
  { "name": "Product To Show" },
  { $set: { "active": true } }
)
```

---

### Delete Product

```javascript
mongosh
use test_database

// Delete by name
db.products.deleteOne({ "name": "Product To Delete" })

// Delete by product_id
db.products.deleteOne({ "product_id": "prod_abc123xyz" })
```

---

### Change Product Category

```javascript
mongosh
use test_database

db.products.updateOne(
  { "name": "Your Product" },
  { $set: { "category": "Power Tools" } }
)
```

**Available Categories:**
- Drywall Tools
- Materials
- Power Tools
- Safety Gear
- Blades & Accessories
- Storage & Organization

---

### Add New Category

Simply use a new category name when adding/updating products:

```javascript
db.products.updateOne(
  { "name": "Your Product" },
  { $set: { "category": "New Category Name" } }
)
```

The new category will automatically appear in the shop filter dropdown.

---

### Bulk Update All Prices (Percentage Increase)

```javascript
mongosh
use test_database

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
```

---

## Market Data Tier Pricing

### View Current Tier Pricing

The tier pricing is defined in `/app/backend/server.py`. Search for `MARKET_DATA_TIERS`:

```python
MARKET_DATA_TIERS = [
    {
        "tier_id": "basic",
        "name": "Basic Analytics",
        "price": 299.00,
        "billing_period": "monthly",
        ...
    },
    {
        "tier_id": "professional",
        "name": "Professional Suite",
        "price": 799.00,
        ...
    },
    {
        "tier_id": "enterprise",
        "name": "Enterprise Platform",
        "price": 1999.00,
        ...
    }
]
```

---

### Change Tier Pricing

**Step 1:** Edit `/app/backend/server.py`

Find the `MARKET_DATA_TIERS` section (around line 830) and update prices:

```python
MARKET_DATA_TIERS = [
    {
        "tier_id": "basic",
        "name": "Basic Analytics",
        "price": 349.00,  # Changed from 299.00
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
        "price": 899.00,  # Changed from 799.00
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
        "price": 2499.00,  # Changed from 1999.00
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

**Step 2:** Restart Backend

```bash
sudo supervisorctl restart backend
```

---

### Add/Remove Tier Features

Edit the `features` array for each tier in `MARKET_DATA_TIERS`:

```python
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
        "NEW FEATURE HERE"  # Add new feature
    ]
}
```

---

### Change Tier Name or Description

```python
{
    "tier_id": "basic",
    "name": "Starter Plan",  # Changed from "Basic Analytics"
    "price": 299.00,
    "billing_period": "monthly",
    "description": "Perfect for small contractors getting started",  # New description
    ...
}
```

---

## User Management

### View All Users

```javascript
mongosh
use test_database

db.users.find().pretty()
```

### View Contractors Only

```javascript
db.users.find({ "user_type": "contractor" }).pretty()
```

### View Subcontractors Only

```javascript
db.users.find({ "user_type": "subcontractor" }).pretty()
```

### Change User Type

```javascript
db.users.updateOne(
  { "email": "user@example.com" },
  { $set: { "user_type": "contractor" } }
)
```

### Delete User

```javascript
db.users.deleteOne({ "email": "user@example.com" })
```

---

## Job Listings Management

### View All Jobs

```javascript
mongosh
use test_database

db.jobs.find().pretty()
```

### Close a Job

```javascript
db.jobs.updateOne(
  { "job_id": "job_abc123xyz" },
  { $set: { "status": "closed" } }
)
```

### Reopen a Job

```javascript
db.jobs.updateOne(
  { "job_id": "job_abc123xyz" },
  { $set: { "status": "active" } }
)
```

### Delete a Job

```javascript
db.jobs.deleteOne({ "job_id": "job_abc123xyz" })
```

---

## Worker Profiles Management

### View All Profiles

```javascript
mongosh
use test_database

db.worker_profiles.find().pretty()
```

### Deactivate a Profile

```javascript
db.worker_profiles.updateOne(
  { "profile_id": "profile_abc123xyz" },
  { $set: { "status": "inactive" } }
)
```

### Delete a Profile

```javascript
db.worker_profiles.deleteOne({ "profile_id": "profile_abc123xyz" })
```

---

## Order & Payment Management

### View All Orders

```javascript
mongosh
use test_database

db.orders.find().pretty()
```

### View Payment Transactions

```javascript
db.payment_transactions.find().pretty()
```

### View Paid Transactions Only

```javascript
db.payment_transactions.find({ "payment_status": "paid" }).pretty()
```

---

## Stripe Configuration

### Switch to Live Payments

**Step 1:** Get live keys from https://dashboard.stripe.com/apikeys

**Step 2:** Update `/app/backend/.env`:

```env
STRIPE_API_KEY=sk_live_your_live_key_here
```

**Step 3:** Restart backend:

```bash
sudo supervisorctl restart backend
```

---

## Database Backup

### Export All Data

```bash
mongodump --db test_database --out /app/backup/$(date +%Y%m%d)
```

### Export Specific Collection

```bash
mongoexport --db test_database --collection products --out /app/backup/products.json
```

### Import Data

```bash
mongoimport --db test_database --collection products --file /app/backup/products.json
```

---

# 📱 Platform Pages Reference

| Page | URL | Description |
|------|-----|-------------|
| Home | `/` | Landing page with hero and service overview |
| Jobs | `/jobs` | Browse job listings with filters |
| Post Job | `/post-job` | Contractor job posting form |
| Workers | `/workers` | Browse subcontractor profiles |
| Create Profile | `/create-profile` | Subcontractor profile form |
| Shop | `/shop` | E-commerce product catalog |
| Cart | `/cart` | Shopping cart |
| Market Data | `/market-data` | Analytics subscription tiers |
| Login | `/login` | User login (email + Google) |
| Register | `/register` | User registration |
| Dashboard | `/dashboard` | User dashboard |

---

# 🏗️ Trade Codes Reference

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

---

# 📁 Project Structure

```
/app
├── backend/
│   ├── server.py          # FastAPI application (tier pricing here)
│   ├── seed_products.py   # Product seeding script
│   └── .env               # Backend environment variables
├── frontend/
│   ├── src/
│   │   ├── App.js         # Main React app
│   │   ├── pages/         # Page components
│   │   └── components/    # Shared components
│   └── .env               # Frontend environment variables
├── memory/
│   └── PRD.md             # Product requirements document
└── README.md              # This file
```

---

# 🚀 Quick Command Reference

| Task | Command |
|------|---------|
| Restart Backend | `sudo supervisorctl restart backend` |
| Restart Frontend | `sudo supervisorctl restart frontend` |
| View Backend Logs | `tail -f /var/log/supervisor/backend.err.log` |
| View Frontend Logs | `tail -f /var/log/supervisor/frontend.err.log` |
| Access MongoDB | `mongosh` then `use test_database` |
| Check Services | `sudo supervisorctl status` |

---

# 📞 Contact

For connection requests between contractors and subcontractors:
- **Email**: info@hdrywallrepair.com
- **Phone**: (555) 123-4567

---

*Built with FastAPI + React + MongoDB on Emergent Platform*
