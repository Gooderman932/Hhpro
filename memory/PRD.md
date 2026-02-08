# Construction Intelligence Platform - PRD
## Poor Dude Holdings LLC - Market Data Module

### Original Problem Statement
Build a proprietary AI-powered Construction Intelligence SaaS platform that will serve as the "Market Data" section of the job-trade-match application. The platform provides:
- Real-time permit intelligence from nationwide sources
- Federal procurement opportunities with AI scoring
- Proprietary ML models for win probability, demand forecasting, and competitive intelligence
- Tiered subscription model ($49/$149/$399)

### User Personas
1. **Basic Users ($49/mo)** - Small contractors needing market insights
2. **Pro Users ($149/mo)** - Mid-size contractors needing nationwide permits + federal opps
3. **Enterprise Users ($399/mo)** - Large contractors needing full API access + custom models

---

## What's Been Implemented ✅

### Phase 1: Core Platform (Complete)
- [x] User authentication (JWT-based)
- [x] Supabase PostgreSQL database integration
- [x] Stripe payment integration (checkout, webhooks, customer portal)
- [x] Three-tier subscription system ($49/$149/$399)
- [x] Tier-based feature gating (`@require_subscription` decorator)

### Phase 2: ML & Analytics (Complete)
- [x] Proprietary Win Probability Model
- [x] Demand Forecasting Model
- [x] Competitive Intelligence Model
- [x] Project Matching Algorithm
- [x] AI enrichment service for permits and federal opportunities

### Phase 3: Data Integrations (Complete)
- [x] FRED API integration (economic data)
- [x] Census API integration (demographic/construction stats)
- [x] Multi-city Open Data Aggregator (12+ cities):
  - NYC, Chicago, San Francisco, Austin, Seattle, Boston
  - New Orleans, Kansas City, Baltimore, Hartford, Norfolk, Albuquerque
- [x] USAspending.gov integration (federal procurement) - *Note: External API intermittent issues*

### Phase 4: Admin & UX (Complete)
- [x] Admin-only revenue dashboard (malcolmgoodmen@gmail.com)
- [x] Onboarding wizard for new subscribers
- [x] All 50 US states + territories support
- [x] Legal/IP protections (Patent Pending notices)

### Recent Updates (Feb 2025)
- [x] **Fixed pricing**: Updated database subscriptions from old ($799/$1999) to new ($149/$399)
- [x] **Real permit data**: Replaced NYC-only data with 12+ city nationwide coverage
- [x] **Federal Opps navigation**: Added to Pro/Enterprise navigation
- [x] Seed data script updated with correct pricing

---

## Current Pricing Tiers

| Tier | Price | Features |
|------|-------|----------|
| Basic | $49/mo | 25 permits/search, major metros, market analytics |
| Professional | $149/mo | 100 permits/search, nationwide, federal opps, ML insights |
| Enterprise | $399/mo | 250 permits/search, all sources, API access, custom models |

---

## Known Limitations

### USAspending.gov API (Federal Procurement)
- **Issue**: Returns 500 errors when called from uvicorn server process
- **Works**: Direct terminal calls work fine
- **Root Cause**: Unknown - possibly SSL/certificate issue in container environment
- **Impact**: Federal procurement opportunities may show empty results
- **Workaround**: API structure is correct; external API reliability issue

### Permit Coverage
- **Current**: 12 major US cities with verified open data portals
- **Limitation**: States without open data portals show data from nearest major metros
- **Solution**: Add commercial permit API (PERMIT_API_KEY) for full nationwide coverage

---

## Prioritized Backlog

### P0 - Critical
- [ ] Debug USAspending.gov 500 errors (try requests library with different SSL settings)

### P1 - High Priority
- [ ] Integrate commercial permit API (Shovels.ai/BatchData) when key provided
- [ ] Real-time WebSocket alerts for Pro tier
- [ ] Add more city open data portals (Dallas, Houston, Phoenix, Miami)

### P2 - Medium Priority
- [ ] API access endpoints for Enterprise tier
- [ ] CSV export functionality
- [ ] Enhanced admin metrics (trial-to-paid conversions)

### P3 - Future
- [ ] Custom model training for Enterprise clients
- [ ] Mobile-responsive improvements
- [ ] Frontend refactoring (separate pages from components)

---

## Technical Architecture

```
/app
├── backend/
│   ├── server.py                    # Main FastAPI app
│   ├── app/
│   │   ├── services/
│   │   │   ├── open_data_permits_service.py  # 12+ city aggregator
│   │   │   ├── federal_procurement_service.py # USAspending integration
│   │   │   ├── permit_enrichment_service.py   # AI scoring
│   │   │   └── procurement_enrichment_service.py
│   │   ├── ml/proprietary/          # ML models
│   │   └── dependencies/auth.py     # Tier gating
│   └── tests/
└── frontend/
    └── src/components/
        ├── pricing/PricingPage.tsx
        ├── permits/PermitsDashboard.tsx
        ├── procurement/FederalOpportunities.tsx
        └── admin/AdminDashboard.tsx
```

---

## Key Endpoints

| Endpoint | Auth | Description |
|----------|------|-------------|
| `/api/pricing/tiers` | Public | Get pricing tiers |
| `/api/permits/search` | Basic+ | Search AI-enriched permits |
| `/api/procurement/federal` | Pro+ | Search federal opportunities |
| `/api/admin/revenue` | Admin | Revenue dashboard metrics |
| `/api/stripe/create-checkout-session` | Auth | Start subscription |

---

## Deployment Notes

This app (Construction Intelligence Platform) is the **Market Data** section of the larger `job-trade-match` application. To deploy:

1. Build frontend: `cd frontend && yarn build`
2. Ensure all environment variables are set (see `.env.example`)
3. Deploy backend and frontend to production
4. The pricing, permits, and federal opps will replace the Market Data section

---

*Last Updated: February 8, 2025*
*Version: 2.1.0*
