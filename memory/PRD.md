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
- Stripe checkout with webhook handling (checkout.session.completed, subscription.updated, subscription.deleted, invoice.payment_failed)
- Customer portal endpoint
- Production mode validation (rejects test keys)
- Health check with system status

### Tier-Based Feature Gating (COMPLETE - December 2025)
- `require_subscription` (Basic+), `require_professional_tier` (Pro+), `require_enterprise_tier`
- Proper 403 responses with upgrade messages and pricing info
- Demand forecast capped at 3 months for Pro, 6 months for Enterprise
- Permit limits per tier

### Proprietary AI/ML Models (COMPLETE)
1. **Win Probability** - Multi-factor bid success prediction with legal_notice, watermark
2. **Demand Forecasting** - Market Momentum + forecasts with tier-based limits
3. **Competitive Intelligence** - Threat scoring + CAI
4. **Project Matching** - Semantic matching with fit scores

### Onboarding Wizard (COMPLETE - December 2025)
- 4-step wizard: Subscription → Profile → Data Sources → First Project
- Progress tracking via `/api/onboarding/status`
- Appears on Analytics dashboard for incomplete users
- Dismissible via sessionStorage

### Mock Data Removal (COMPLETE)
- Zero sample/demo data in production endpoints
- All data sources return empty with setup hints when unconfigured
- Data source labels on all ML predictions

### Legal Documentation (COMPLETE)
- `/backend/legal/PATENT_PENDING.md` - 4 patent applications with claims
- `/backend/legal/TRADE_SECRETS.md` - Trade secret classification
- `/backend/legal/IP_ASSIGNMENT.md` - IP ownership declaration
- `/backend/legal/LICENSE_PROPRIETARY.md` - Proprietary license terms
- All ML files have copyright headers and watermarks

### Deployment Documentation (COMPLETE)
- `/docs/PRODUCTION_ENV_VARS.md` - All env vars with setup instructions
- `/docs/DEPLOYMENT_CHECKLIST.md` - Pre/post deployment verification
- `/backend/.env.example` - Template for production env

## External API Keys Needed (For Deployment)
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
- [ ] Census Bureau / BLS API integration

### P1 - Real-time Features
- [ ] WebSocket setup for live notifications
- [ ] Smart Alerts system based on ML outputs

### P2 - Refactoring
- [ ] Move inline routes from server.py into /routes/ modules
- [ ] Add comprehensive pytest suite beyond production readiness tests

## Test Credentials
- Enterprise: `malcolmgoodmen@gmail.com` / `Test123!`
- Unpaid: `nopay@test.com` / `test123`
