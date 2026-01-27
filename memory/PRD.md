# Construction Intelligence Platform - PRD

## Original Problem Statement
Build a working application from the user's private GitHub repository `gooderman932/market-data`. The scope evolved to perform a major technical migration from PostgreSQL to MongoDB and prepare the application for deployment with monetization features.

## Product Overview
A full-stack construction intelligence platform with:
- **Frontend**: React/Vite/TypeScript with Tailwind CSS
- **Backend**: FastAPI with Python (modular architecture)
- **Database**: MongoDB (migrated from PostgreSQL)
- **Payments**: Stripe integration for subscriptions
- **Process Management**: Supervisor

## Current Architecture (v2.0.0 - Modular)
```
/app/
├── backend/
│   ├── server.py           # Minimal FastAPI app - includes routers
│   ├── db/
│   │   └── mongo.py        # MongoDB client and index initialization
│   ├── models/
│   │   └── schemas.py      # Pydantic models for all entities
│   ├── auth/
│   │   └── deps.py         # Auth helpers (JWT, password hashing)
│   ├── routes/
│   │   ├── auth.py         # /api/auth/* endpoints
│   │   ├── jobs.py         # /api/jobs/* endpoints
│   │   ├── workers.py      # /api/workers/* endpoints
│   │   ├── products.py     # /api/products/* endpoints
│   │   ├── orders.py       # /api/orders/* endpoints
│   │   ├── payments.py     # /api/payments/* endpoints
│   │   └── market_data.py  # /api/pricing/*, /api/subscriptions/*
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── auth/AuthPage.tsx        # Login/Register page
│   │   │   ├── pricing/PricingPage.tsx  # Pricing tiers page
│   │   │   ├── pricing/SubscriptionSuccess.tsx # Post-payment page
│   │   │   ├── dashboard/
│   │   │   ├── intelligence/
│   │   │   └── ui/                      # Shadcn components
│   │   ├── services/api.ts              # API service layer
│   │   ├── types/                       # TypeScript types
│   │   ├── App.tsx                      # Main app with routing
│   │   └── main.tsx
│   ├── dist/               # Built production assets
│   ├── vite.config.ts
│   ├── package.json
│   └── .env
└── scripts/                # Deployment and maintenance scripts
```

## Key Pages & Routes

### Frontend Routes
- `/` - Homepage with hero section and features
- `/pricing` - Subscription tiers page (Basic $299, Professional $799, Enterprise $1999)
- `/login` - Login/Register page with tabs
- `/subscription/success` - Post-payment confirmation page

### API Endpoints
See full list in backend routes documentation.

## What's Been Implemented ✅

### P0 - Deployment Readiness (COMPLETE)
- [x] Database Migration: PostgreSQL → MongoDB
- [x] Backend modularized into separate files
- [x] Frontend builds successfully
- [x] All deployment blockers resolved

### P1 - MongoDB Query Optimizations (COMPLETE)
- [x] Added projections to all list queries

### P2 - Stripe Integration (COMPLETE)
- [x] Backend subscription endpoints
- [x] payment_transactions collection
- [x] subscriptions collection

### P3 - Code Refactoring (COMPLETE)
- [x] Modular backend structure

### P4 - Frontend Pricing UI (COMPLETE)
- [x] Homepage with hero, features, CTA
- [x] Pricing page with 3 tiers
- [x] Login/Register page with tabs
- [x] Subscription success page with polling
- [x] Navigation with login state
- [x] Stripe checkout flow integration

## Environment Variables

### Backend (.env)
```
MONGO_URL=mongodb://localhost:27017
DB_NAME=construction_intel_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=*
STRIPE_API_KEY=sk_test_emergent
STRIPE_WEBHOOK_SECRET=
```

### Frontend (.env)
```
VITE_API_URL=/api
```

## Deployment Status: READY ✅
- Frontend: Running on port 3000
- Backend: Running on port 8001
- MongoDB: Connected
- Stripe: Configured and working

## Test Credentials
- **Test User**: test@example.com / test123

## Pending Tasks

### Backlog (Future)
- [ ] Subscription usage tracking (per-tenant limits)
- [ ] Admin billing/usage dashboard
- [ ] Email notifications for subscription events
- [ ] Subscription cancellation/renewal flow

---
*Last Updated: January 27, 2026*
*Version: 2.0.0 (Full Monetization)*
