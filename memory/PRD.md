# HHDrywall Pro - Construction Intelligence Platform
## Product Requirements Document
**Owner**: Poor Dude Holdings LLC
**Last Updated**: December 2025

---

## Original Problem Statement
Build a premium Construction Intelligence Platform with proprietary AI/ML models as the core intellectual property of Poor Dude Holdings LLC. Production-ready SaaS with live billing, tier-based gating, and real data delivery.

## Architecture
- **Frontend**: React + Vite + TypeScript + Tailwind CSS + Shadcn/UI
- **Backend**: FastAPI + Python + SQLAlchemy
- **Database**: PostgreSQL (Supabase - remote)
- **Payments**: Stripe (via emergentintegrations)
- **Email**: Resend
- **ML**: Custom proprietary models (scikit-learn as base tooling)

## Pricing Structure
| Tier | Price | Key Features |
|------|-------|-------------|
| Basic | $49/mo | Projects, 25 permits/mo, basic indicators, weekly digest |
| Pro | $149/mo | State-wide permits, real-time alerts, Win Probability, 3-month forecast, competitor intel |
| Enterprise | $399/mo | Multi-state, 6-month forecast, advanced ML, API access, custom training |

## What's Been Implemented

### Core Infrastructure (COMPLETE)
- User registration and JWT authentication
- Stripe checkout with webhook handling
- Customer portal endpoint
- Production mode validation (rejects test keys)
- Health check with system status

### Tier-Based Feature Gating (COMPLETE)
- require_subscription (Basic+), require_professional_tier (Pro+), require_enterprise_tier
- Proper 403 responses with upgrade messages
- Demand forecast: Pro=3 months, Enterprise=6 months

### Proprietary AI/ML Models (COMPLETE)
1. Win Probability - Multi-factor bid success prediction
2. Demand Forecasting - Market Momentum + forecasts
3. Competitive Intelligence - Threat scoring + CAI
4. Project-Contractor Matching AI

### Onboarding Wizard (COMPLETE)
- 4-step wizard: Subscription -> Profile -> Data Sources -> First Project
- Progress tracking via /api/onboarding/status

### Mock Data Removal (COMPLETE)
- Zero sample/demo data in production
- Data source labels on all ML predictions

### Legal Documentation (COMPLETE)
- PATENT_PENDING.md, TRADE_SECRETS.md, IP_ASSIGNMENT.md, LICENSE_PROPRIETARY.md

### Admin Revenue Dashboard (COMPLETE - December 2025)
- Admin-only access (is_admin=true on users table, locked to malcolmgoodmen@gmail.com)
- KPI Cards: MRR, ARR, Active Subscribers, Churn Rate
- Secondary Metrics: ARPU, Conversion Rate, Growth Rate, Top Tier, Total Users
- Revenue by Tier bar chart, Subscriber Mix donut chart, LTV by Tier cards
- Revenue Trend (90-day timeline)
- Recent Transactions and Recent Signups tables
- Alerts: Failed payments, cancellations
- CSV Export, Date range selector (30/60/90d), Refresh button
- Non-admin users see "Access Denied" page

### Deployment Documentation (COMPLETE)
- /docs/PRODUCTION_ENV_VARS.md, /docs/DEPLOYMENT_CHECKLIST.md, .env.example

## External API Keys Needed
| Variable | Source | URL |
|----------|--------|-----|
| STRIPE_API_KEY | Stripe (live) | https://dashboard.stripe.com/apikeys |
| STRIPE_WEBHOOK_SECRET | Stripe webhooks | https://dashboard.stripe.com/webhooks |
| FRED_API_KEY | Federal Reserve | https://fred.stlouisfed.org/docs/api/api_key.html |
| PERMIT_API_KEY | Permit provider | https://www.permitdata.org |

## Pending / Upcoming Tasks

### P1 - Real External Data
- [ ] Connect FRED API when user provides key
- [ ] Connect permit data source when user provides key

### P1 - Real-time Features
- [ ] WebSocket setup for live notifications
- [ ] Smart Alerts system

### P2 - Refactoring
- [ ] Move inline routes from server.py into /routes/ modules
- [ ] Comprehensive pytest suite

## Test Credentials
- Admin: `malcolmgoodmen@gmail.com` / `Test123!` (is_admin=true)
- Unpaid: `nopay@test.com` / `test123`
