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
- **ML**: Custom proprietary models (scikit-learn acceptable as base)

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
   - Outputs: probability, confidence, recommendation (STRONG PURSUE/PURSUE/EVALUATE/PASS), watermark

2. **Demand Forecasting Engine** (`/api/ml/demand-forecast`, `/api/ml/regional-outlook`)
   - Market Momentum Score calculation
   - Seasonality-adjusted forecasts (1-12 months)
   - Regional and sector growth factors
   - Confidence intervals per period

3. **Competitive Intelligence Scorer** (`/api/ml/competitive-analysis`, `/api/ml/competitive-landscape`)
   - Competitor Threat Scoring (0-100)
   - Competitive Advantage Index (CAI)
   - Multi-factor analysis: market share, win rate, project overlap, pricing, capacity, reputation
   - Vulnerability and strength identification

4. **Project-Contractor Matching AI** (`/api/ml/project-matching`)
   - Semantic text similarity for trade matching
   - Multi-factor fit scoring: trade, value, geography, sector, complexity
   - Adaptive learning from user feedback
   - Match reasons and concerns

### Frontend ML Dashboard (COMPLETE - December 2025)
- 4-tab AI Intelligence Hub at `/predictions`
- Win Probability tab with project selection and factor breakdown
- Demand Forecast tab with momentum score, timeline, and regional outlook
- Competitive Intel tab with CAI and threat rankings
- Project Matching tab with fit scores and recommendations

### Tier-Based Feature Gating (COMPLETE)
- Basic: Projects, permits (25/mo), basic filters
- Professional: ML predictions, competitor tracking, economic indicators, benchmarks
- Enterprise: All features, batch scoring, API access, LLM insights

## Pending / Upcoming Tasks

### P1 - Phase 3: External Data Integrations
- [ ] Integrate FRED API with real API key (currently mock/demo mode)
- [ ] Integrate construction permit data source (currently mocked)
- [ ] Census Bureau / BLS API integration
- [ ] ENV vars: FRED_API_KEY, PERMIT_API_KEY

### P1 - Phase 4: Real-time Features
- [ ] WebSocket setup for live notifications
- [ ] Smart Alerts system based on ML outputs
- [ ] Real-time permit monitoring

### P2 - Legal Documentation
- [ ] /legal/PATENT_PENDING.md
- [ ] IP documentation and license files
- [ ] Full copyright audit of all ML files

### P2 - Refactoring
- [ ] Move inline routes from server.py into /routes/ modules
- [ ] Clean up deprecated route directory
- [ ] Add comprehensive pytest suite

## Test Credentials
- Enterprise: `malcolmgoodmen@gmail.com` / `Test123!`
- Unpaid: `nopay@test.com` / `test123`

## MOCKED Services
- **PermitDataService**: Generates random mock permit data
- **FREDService**: Falls back to demo mode without real FRED_API_KEY
