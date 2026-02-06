# Construction Intelligence Platform - PRD

## Product Overview
Enterprise SaaS platform for construction market intelligence, combining AI/ML capabilities with real-time market data.

**Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.**

## Architecture

### Tech Stack
- **Backend**: FastAPI + Python 3.11 + PostgreSQL (Supabase) + SQLAlchemy
- **Frontend**: React 18 + TypeScript + Vite + Tailwind CSS
- **ML**: scikit-learn (Win Probability, Demand Forecast, Opportunity Scoring)
- **Payments**: Stripe via emergentintegrations
- **Email**: Resend (for notifications)
- **Database**: Supabase PostgreSQL (external managed)

### Database Configuration
- **Provider**: Supabase (PostgreSQL 17)
- **Connection**: Session Pooler (aws-1-us-east-2.pooler.supabase.com)
- **Tables**: tenants, users, projects, companies, project_participations, predictions, opportunity_scores, subscriptions, payment_transactions, notification_preferences, notification_logs

## Key Features

### 1. Project Discovery
- Track opportunities, permits, tenders
- Filter by sector, region, value
- Status management

### 2. ML Predictions (Professional+)
- **Win Probability**: Random Forest classifier predicting project win likelihood
- **Demand Forecasting**: Time series forecasts by sector/region
- **Regional Outlook**: Multi-region demand analysis

### 3. Opportunity Scoring (Enterprise)
- Multi-factor scoring engine
- Value, fit, competition, timing, risk scores
- Actionable recommendations (PURSUE/EVALUATE/CONSIDER/PASS)

### 4. Competitive Intelligence (Professional+)
- Competitor tracking
- Market share analysis
- Win rate calculations

### 5. Email Notifications
- User-configurable preferences: sectors, regions, value threshold
- Frequency options: Real-time, Daily Digest, Weekly Digest
- Match logic: ANY (OR) or ALL (AND)
- Test notifications to verify setup

## Subscription Tiers

| Feature | Basic ($299) | Professional ($799) | Enterprise ($1999) |
|---------|--------------|---------------------|-------------------|
| Projects | 100 | 1,000 | Unlimited |
| Analytics Summary | ✅ | ✅ | ✅ |
| Regional Analysis | ✅ | ✅ | ✅ |
| Win Probability | ❌ | ✅ | ✅ |
| Demand Forecasting | ❌ | ✅ | ✅ |
| Competitor Intel | ❌ | ✅ | ✅ |
| Opportunity Scoring | ❌ | ❌ | ✅ |
| Email Notifications | ✅ | ✅ | ✅ |
| API Access | ❌ | ❌ | ✅ |

## Test Accounts
- **Enterprise**: `malcolmgoodmen@gmail.com` / `Test123!`
- **Professional**: `test@example.com` / `test123`

## File Structure
```
/app/backend/
├── server.py                    # Main FastAPI app
├── .env                         # Supabase DATABASE_URL + secrets
├── requirements.txt             # Python deps (no MongoDB)
├── app/
│   ├── database.py              # PostgreSQL/SQLAlchemy connection
│   ├── models/                  # SQLAlchemy models
│   ├── ml/                      # ML models
│   └── services/                # Business logic
└── scripts/
    └── seed_data.py             # Database seeding

/app/frontend/
├── src/
│   ├── App.tsx                  # Main router
│   ├── components/              # React components
│   └── services/api.ts          # API client
└── package.json
```

## Deployment Status

### ✅ Completed
- [x] MongoDB removed from codebase
- [x] PostgreSQL-only architecture
- [x] External Supabase database connected
- [x] All endpoints verified working
- [x] Test data seeded in production DB

### ⚠️ For Production Deployment
- Update .gitignore to allow .env tracking (or use env vars at deployment)
- ML dependencies may need resource tuning

## Recent Changes (Feb 6, 2026)
- Migrated from local PostgreSQL to Supabase
- Removed all MongoDB dependencies (pymongo, motor)
- Cleaned up unused route files
- Verified all 6 major endpoint groups working

---
*Last Updated: February 6, 2026*
*Version: 2.2.0 (Supabase Integration)*
