# HHDrywall Pro - Construction Intelligence Platform
## Product Requirements Document
**Owner**: Poor Dude Holdings LLC
**Last Updated**: December 2025

---

## Original Problem Statement
Build a premium Construction Intelligence Platform with proprietary AI/ML models as the core IP of Poor Dude Holdings LLC.

## Architecture
- **Frontend**: React + Vite + TypeScript + Tailwind CSS + Shadcn/UI
- **Backend**: FastAPI + Python + SQLAlchemy
- **Database**: PostgreSQL (Supabase)
- **Payments**: Stripe
- **Email**: Resend
- **ML**: Custom proprietary models
- **Data Sources**: FRED (live), NYC DOB Open Data (live), Census Bureau (live), Shovels.ai/BatchData (pluggable)

## What's Been Implemented

### Core: Auth, Stripe ($49/$149/$399), Tier Gating, Admin Dashboard (COMPLETE)
### Proprietary ML: 4 models with legal headers, watermarks, patent docs (COMPLETE)
### Mock Data Removal: Zero fake data, proper empty states (COMPLETE)
### 50 States + Territories: All dropdowns and ML models expanded (COMPLETE)

### Permit Intelligence System (COMPLETE - December 2025)
- **Commercial Permits Service**: Pluggable Shovels.ai / BatchData integration via PERMIT_API_KEY
- **NYC DOB Open Data**: Live free permits from NYC Department of Buildings (no key required)
- **Census Bureau**: Aggregate building permit stats with CENSUS_API_KEY
- **Enrichment Engine**: Every permit scored by ProjectMatcherAI + WinProbabilityModel
  - Opportunity Score (0-100, weighted composite)
  - Match Score, Win Probability, Required Trades, Timeline Estimate
  - Actionable recommendations per permit
- **Unified API**: `GET /api/permits/search` with tier-based limits
- **Frontend**: Full Permit Intelligence dashboard with search, AI scores, trade chips
- **Docs**: `/docs/PERMIT_INTELLIGENCE_SYSTEM.md`

### Live Data Sources
| Source | Status | Key |
|--------|--------|-----|
| FRED Economic Data | CONNECTED | FRED_API_KEY |
| NYC DOB Open Data | CONNECTED | No key needed |
| Census Bureau | CONNECTED | CENSUS_API_KEY |
| Shovels.ai / BatchData | READY (needs key) | PERMIT_API_KEY |

## Pending Tasks

### P1 - Connect Paid Permit Source
- [ ] Get Shovels.ai or BatchData API key for nationwide coverage
- [ ] Set PERMIT_API_KEY in .env

### P1 - Real-time Features
- [ ] WebSocket live notifications
- [ ] Smart Alerts for high-score permits

### P2 - Refactoring
- [ ] Break server.py into route modules

## Test Credentials
- Admin: `malcolmgoodmen@gmail.com` / `Test123!`
- Unpaid: `nopay@test.com` / `test123`
