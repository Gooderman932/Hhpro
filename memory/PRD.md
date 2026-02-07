# HHDrywall Pro - Construction Intelligence Platform
## Product Requirements Document
**Owner**: Poor Dude Holdings LLC
**Last Updated**: December 2025

---

## Original Problem Statement
Build a premium Construction Intelligence Platform with proprietary AI/ML models as the core intellectual property of Poor Dude Holdings LLC. The platform provides construction industry professionals with market analytics, competitor intelligence, demand forecasting, and project matching capabilities.

## Architecture
- **Frontend**: React + Vite + TypeScript + Tailwind CSS + Shadcn/UI
- **Backend**: FastAPI + Python + SQLAlchemy
- **Database**: PostgreSQL (Supabase - remote)
- **Payments**: Stripe (with webhooks)
- **Email**: Resend
- **ML**: Custom proprietary models (scikit-learn as base tooling)

## What's Been Implemented

### Core Infrastructure (COMPLETE)
- User registration and JWT authentication
- Three-tier Stripe subscription system (Basic $299, Professional $799, Enterprise $1999)
- Payment-to-feature-access pipeline with webhooks
- Supabase PostgreSQL database (fully migrated from MongoDB)
- CORS, hot-reload, supervisor-managed services

### Phase 1: User Personalization (COMPLETE)
- 4-step onboarding form (business type, trade, service area, sectors)
- User profile API (GET/PUT /api/profile)
- My Projects CRUD with AI enrichment
- Tracked Competitors CRUD
- User Clients management
- Saved searches (tier-limited)
- Permits page with filters and match scoring
- Notification settings with Resend email integration

### Phase 2: Proprietary AI/ML Models (COMPLETE - December 2025)
All 4 proprietary models implemented with legal headers, watermarks, and connected to API endpoints:

1. **Win Probability Model** (`/api/ml/win-probability`)
   - Multi-factor bid success prediction
   - Factors: project fit, competitive pressure, historical performance, market conditions, timing, relationships
   - Outputs: probability, confidence, recommendation, watermark

2. **Demand Forecasting Engine** (`/api/ml/demand-forecast`, `/api/ml/regional-outlook`)
   - Market Momentum Score calculation
   - Seasonality-adjusted forecasts (1-12 months)
   - Regional and sector growth factors

3. **Competitive Intelligence Scorer** (`/api/ml/competitive-analysis`, `/api/ml/competitive-landscape`)
   - Competitor Threat Scoring (0-100)
   - Competitive Advantage Index (CAI)
   - Vulnerability and strength identification

4. **Project-Contractor Matching AI** (`/api/ml/project-matching`)
   - Semantic text similarity for trade matching
   - Multi-factor fit scoring
   - Adaptive learning from user feedback

### Mock Data Removal & Real Value Delivery (COMPLETE - December 2025)
- Removed ALL fake/sample/demo data from production endpoints
- PermitDataService returns empty when PERMIT_API_KEY not configured
- FREDService returns empty when FRED_API_KEY not configured
- Competitor endpoints return empty when no real tracked competitors
- Data source status endpoint (`/api/data-sources`) shows configuration status
- Proper empty states in frontend with setup instructions
- Data source labels on all ML predictions

### Legal Documentation (COMPLETE - December 2025)
- `/backend/legal/PATENT_PENDING.md` - 4 patent applications documented with claims
- `/backend/legal/TRADE_SECRETS.md` - Trade secret classification and protections
- `/backend/legal/IP_ASSIGNMENT.md` - IP ownership and third-party component declaration
- `/backend/legal/LICENSE_PROPRIETARY.md` - Proprietary software license terms
- `/backend/app/ml/proprietary/README.md` - Model inventory and patent status
- All 4 ML model files have copyright headers, patent pending notices, and watermarks

### Tier-Based Feature Gating (COMPLETE)
- Basic: Projects, permits (25/mo), basic filters
- Professional: ML predictions, competitor tracking, economic indicators, benchmarks
- Enterprise: All features, batch scoring, API access, LLM insights

## Data Source Configuration (For Deployment)

External API keys needed (set in /backend/.env):
| Variable | Source | Signup URL |
|----------|--------|------------|
| PERMIT_API_KEY | Permit data provider | https://www.permitdata.org |
| FRED_API_KEY | Federal Reserve FRED | https://fred.stlouisfed.org/docs/api/api_key.html |

## Pending / Upcoming Tasks

### P1 - Phase 3: External Data Integrations
- [ ] Connect real FRED API when user provides key
- [ ] Connect permit data source when user provides key
- [ ] Census Bureau / BLS API integration

### P1 - Phase 4: Real-time Features
- [ ] WebSocket setup for live notifications
- [ ] Smart Alerts system based on ML outputs
- [ ] Real-time permit monitoring

### P2 - Refactoring
- [ ] Move inline routes from server.py into /routes/ modules
- [ ] Add comprehensive pytest suite

## Test Credentials
- Enterprise: `malcolmgoodmen@gmail.com` / `Test123!`
- Unpaid: `nopay@test.com` / `test123`
