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
- 12+ contractor tools and supplies
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

## 🔧 Subdomain Setup (pro.hdrywallrepair.com)

### Step 1: Add DNS Record

Go to your domain provider (GoDaddy, Namecheap, Cloudflare, etc.) and add:

```
Type:   CNAME
Name:   pro
Value:  job-trade-match.preview.emergentagent.com
TTL:    Auto (or 3600)
```

### Step 2: Connect in Emergent Dashboard

1. Go to **Home** in Emergent
2. Click on **HDrywall Repair** project
3. Click **"Link domain"**
4. Enter: `pro.hdrywallrepair.com`
5. Click **"Entri"** and follow prompts

### Step 3: Wait & Verify

- DNS propagation: 5-30 minutes
- SSL certificate: 5-15 minutes
- Test: Visit `https://pro.hdrywallrepair.com`

### Troubleshooting

If not working after 15 minutes:
1. Check DNS at https://dnschecker.org
2. Remove any conflicting A records for "pro"
3. Re-link domain in Emergent

---

## 🔗 HTML Integration for hdrywallrepair.com

### Navigation Links

Add to your existing menu:

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

### Complete Feature Section (Homepage)

```html
<section style="padding:60px 20px; background:#f8fafc;">
  <div style="max-width:1200px; margin:0 auto; text-align:center;">
    <h2 style="font-size:32px; color:#0f172a; margin-bottom:40px;">
      Our Professional Services
    </h2>
    
    <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(250px,1fr)); gap:20px;">
      
      <!-- Job Board -->
      <a href="https://pro.hdrywallrepair.com/jobs" 
         style="display:block; background:white; border:1px solid #e2e8f0; 
                padding:30px; text-decoration:none; text-align:center;">
        <h3 style="color:#0f172a; margin-bottom:10px;">Job Board</h3>
        <p style="color:#64748b; font-size:14px; margin-bottom:15px;">
          Find or post jobs by trade code and location
        </p>
        <span style="color:#f97316; font-weight:500;">Browse Jobs →</span>
      </a>
      
      <!-- Find Workers -->
      <a href="https://pro.hdrywallrepair.com/workers" 
         style="display:block; background:white; border:1px solid #e2e8f0; 
                padding:30px; text-decoration:none; text-align:center;">
        <h3 style="color:#0f172a; margin-bottom:10px;">Find Workers</h3>
        <p style="color:#64748b; font-size:14px; margin-bottom:15px;">
          Browse skilled subcontractors by trade
        </p>
        <span style="color:#f97316; font-weight:500;">View Profiles →</span>
      </a>
      
      <!-- Pro Shop -->
      <a href="https://pro.hdrywallrepair.com/shop" 
         style="display:block; background:white; border:1px solid #e2e8f0; 
                padding:30px; text-decoration:none; text-align:center;">
        <h3 style="color:#0f172a; margin-bottom:10px;">Pro Shop</h3>
        <p style="color:#64748b; font-size:14px; margin-bottom:15px;">
          Professional tools and supplies
        </p>
        <span style="color:#f97316; font-weight:500;">Shop Now →</span>
      </a>
      
      <!-- Market Data -->
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

## 📱 Platform Pages

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

## 🏗️ Trade Codes Supported

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

## 🔐 Authentication

- **Email/Password**: JWT-based authentication
- **Google Login**: Emergent OAuth integration
- **User Types**: Contractor or Subcontractor (switchable)

---

## 💳 Payments

- **Provider**: Stripe
- **Supported**: Credit cards
- **Test Mode**: Currently using test keys

To switch to production:
1. Get Stripe live keys from https://dashboard.stripe.com
2. Update `STRIPE_API_KEY` in `/app/backend/.env`
3. Restart backend

---

## 📁 Project Structure

```
/app
├── backend/
│   ├── server.py          # FastAPI application
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

## 🚀 Deployment Checklist

- [x] Backend API working
- [x] Frontend pages working
- [x] Stripe integration working
- [x] Google OAuth working
- [x] Products seeded (12 items)
- [x] Database queries optimized
- [x] Deployment blockers fixed
- [ ] Add CNAME record for subdomain
- [ ] Link domain in Emergent
- [ ] Add HTML links to main site
- [ ] Switch to Stripe live keys (when ready)

---

## 📞 Contact

For connection requests between contractors and subcontractors:
- **Email**: info@hdrywallrepair.com
- **Phone**: (555) 123-4567

---

## 📝 Next Steps (Future Development)

1. **Admin Dashboard** - Staff tools to manage contractor/subcontractor connections
2. **Contact Request System** - Formal request flow for monetization
3. **Order History** - Customer order tracking
4. **Email Notifications** - Automated alerts
5. **Dropshipping Integration** - Level 5, Temu suppliers for branded products

---

*Built with FastAPI + React + MongoDB on Emergent Platform*
