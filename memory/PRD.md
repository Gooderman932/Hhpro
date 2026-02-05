# Construction Intelligence Platform - PRD

## Product Overview
Enterprise SaaS platform for construction market intelligence, combining AI/ML capabilities with real-time market data.

**Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.**

## Architecture

### Tech Stack
- **Backend**: FastAPI + Python 3.11 + PostgreSQL + SQLAlchemy
- **Frontend**: React 18 + TypeScript + Vite + Tailwind CSS
- **ML**: scikit-learn (Win Probability, Demand Forecast, Opportunity Scoring)
- **Payments**: Stripe via emergentintegrations
- **Email**: Resend (for notifications)
- **Infrastructure**: Supervisor process management

### Database: PostgreSQL
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

### 5. Email Notifications (NEW)
- **User-configurable preferences**: sectors, regions, value threshold
- **Frequency options**: Real-time, Daily Digest, Weekly Digest
- **Match logic**: ANY (OR) or ALL (AND)
- **Test notifications**: Send test emails to verify setup

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

## API Endpoints

### Auth
- `POST /api/auth/register` - Register user
- `POST /api/auth/token` - Login
- `GET /api/auth/me` - Current user

### Subscriptions
- `GET /api/pricing/tiers` - Get tiers
- `POST /api/subscriptions/checkout` - Start Stripe checkout
- `GET /api/subscriptions/status/{session_id}` - Check payment
- `GET /api/subscriptions/current` - Current subscription

### Projects (Subscription required)
- `GET /api/projects` - List projects
- `POST /api/projects` - Create project

### Analytics (Basic+)
- `GET /api/analytics/summary` - Dashboard summary
- `GET /api/analytics/regions` - Regional analysis

### ML Predictions (Professional+)
- `GET /api/predictions/win-probability/{project_id}` - Win prediction
- `GET /api/predictions/demand-forecast` - Demand forecast
- `GET /api/predictions/regional-outlook` - Regional outlook

### Scoring (Enterprise)
- `GET /api/scoring/project/{project_id}` - Score project
- `GET /api/scoring/batch` - Batch score projects

### Intelligence (Professional+)
- `GET /api/intelligence/competitors` - Competitor data

### Notifications (NEW)
- `GET /api/notifications/preferences` - Get preferences
- `PUT /api/notifications/preferences` - Update preferences
- `GET /api/notifications/options` - Get available sectors/regions
- `POST /api/notifications/test` - Send test notification
- `GET /api/notifications/history` - Get notification history

## Test Accounts
- **Enterprise**: `malcolmgoodmen@gmail.com` / `Test123!`
- **Professional**: `test@example.com` / `test123`

## File Structure
```
/app/backend/
├── server.py                    # Main FastAPI app
├── app/
│   ├── database.py              # PostgreSQL connection
│   ├── models/                  # SQLAlchemy models
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── company.py
│   │   ├── prediction.py
│   │   ├── subscription.py
│   │   └── notification.py      # NEW
│   ├── ml/                      # ML models
│   │   ├── win_probability.py
│   │   ├── demand_forecast.py
│   │   └── opportunity_scoring.py
│   └── services/                # Business logic
│       ├── prediction.py
│       ├── scoring.py
│       └── notification.py      # NEW
└── requirements.txt

/app/frontend/
├── src/
│   ├── App.tsx                  # Main router
│   ├── components/
│   │   ├── dashboard/
│   │   │   ├── Analytics.tsx
│   │   │   ├── MLDashboard.tsx
│   │   │   └── BatchScoring.tsx
│   │   ├── intelligence/
│   │   │   └── CompetitorMap.tsx
│   │   ├── settings/
│   │   │   └── NotificationSettings.tsx  # NEW
│   │   ├── pricing/
│   │   └── auth/
│   └── services/
│       └── api.ts               # API client
└── package.json
```

## Completed Features
- [x] PostgreSQL with SQLAlchemy ORM
- [x] User authentication with JWT
- [x] Stripe subscription integration
- [x] Win Probability ML model
- [x] Demand Forecasting model
- [x] Opportunity Scoring engine
- [x] Tier-based access control
- [x] Sample data seeding
- [x] Frontend with dark theme
- [x] Analytics Dashboard with charts
- [x] ML Predictions Dashboard
- [x] Batch Scoring (Enterprise)
- [x] Competitor Intelligence
- [x] Email Notification System (NEW)
  - [x] User preferences management
  - [x] Sector/Region/Value filters
  - [x] Frequency options (realtime/daily/weekly)
  - [x] Test notification sending
  - [x] Notification history

## Testing Status
- Backend: 100% (15/15 tests passed)
- Frontend: 100% (all features working)
- Last tested: February 5, 2026

---
*Last Updated: February 5, 2026*
*Version: 2.1.0 (Added Email Notifications)*
