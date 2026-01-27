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

## Core Requirements
1. ✅ Database Migration: PostgreSQL/SQLAlchemy → MongoDB/Motor (async)
2. ✅ Dependency Cleanup: Remove all local ML libraries, Redis
3. ✅ Configuration: Environment-driven (.env files)
4. ✅ Deployment: Frontend port 3000, Backend port 8001
5. ✅ Market Data pricing tiers with Stripe payments

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
│   │   ├── components/     # Dashboard, Intelligence components
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── vite-env.d.ts
│   ├── dist/               # Built production assets
│   ├── vite.config.ts
│   ├── package.json
│   └── .env
└── scripts/                # Deployment and maintenance scripts
```

## Key API Endpoints
### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/token` - Login and get JWT
- `GET /api/auth/me` - Get current user

### Jobs
- `GET /api/jobs` - List jobs (with projections)
- `POST /api/jobs` - Create job
- `PUT /api/jobs/{job_id}` - Update job
- `DELETE /api/jobs/{job_id}` - Close job

### Workers
- `GET /api/workers` - List workers (with projections)
- `POST /api/workers` - Create worker profile
- `PUT /api/workers/{profile_id}` - Update profile
- `DELETE /api/workers/{profile_id}` - Deactivate profile

### Products & Orders
- `GET /api/products` - List products (with projections)
- `POST /api/products` - Create product (admin)
- `PUT /api/products/{product_id}/stock` - Update stock
- `GET /api/orders` - List orders (with projections)
- `POST /api/orders` - Create order
- `POST /api/payments` - Process payment

### Subscriptions (Stripe Integration)
- `GET /api/pricing/tiers` - Get pricing tiers
- `POST /api/subscriptions/checkout` - Create Stripe checkout session
- `GET /api/subscriptions/status/{session_id}` - Check payment status
- `GET /api/subscriptions/current` - Get active subscription
- `POST /api/webhook/stripe` - Stripe webhook handler

### Health
- `GET /health` - Health check
- `GET /` - API info

## Database Schema (MongoDB)
- **Database**: `construction_intel_db`
- **Collections**: 
  - `users` - User accounts
  - `jobs` - Job listings
  - `worker_profiles` - Worker profiles
  - `products` - Shop products
  - `orders` - Product orders
  - `payment_transactions` - Payment records (Stripe sessions)
  - `subscriptions` - Active subscriptions

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

## What's Been Implemented ✅

### P0 - Deployment Readiness (COMPLETE)
- [x] Database Migration: PostgreSQL → MongoDB (Motor async driver)
- [x] Removed all SQLAlchemy, PostgreSQL, Redis dependencies
- [x] Backend consolidated into server.py with FastAPI
- [x] Configuration externalized to .env files
- [x] Frontend build errors fixed (TypeScript issues)
- [x] Supervisor configurations for production
- [x] Frontend builds successfully (dist/ folder exists)
- [x] Deployment blockers resolved

### P1 - MongoDB Query Optimizations (COMPLETE)
- [x] Added projections to Jobs list query
- [x] Added projections to Workers list query
- [x] Added projections to Products list query
- [x] Added projections to Orders list query

### P2 - Stripe Integration (COMPLETE)
- [x] Installed emergentintegrations library
- [x] Added Stripe configuration to .env
- [x] Created `/api/subscriptions/checkout` endpoint
- [x] Created `/api/subscriptions/status/{session_id}` endpoint
- [x] Created `/api/subscriptions/current` endpoint
- [x] Created `/api/webhook/stripe` endpoint
- [x] Created payment_transactions collection for tracking
- [x] Created subscriptions collection for active subs

### P3 - Code Refactoring (COMPLETE)
- [x] Created modular directory structure (db/, models/, auth/, routes/)
- [x] Moved MongoDB client to `db/mongo.py`
- [x] Moved Pydantic models to `models/schemas.py`
- [x] Moved auth helpers to `auth/deps.py`
- [x] Split routes into separate files:
  - `routes/auth.py`
  - `routes/jobs.py`
  - `routes/workers.py`
  - `routes/products.py`
  - `routes/orders.py`
  - `routes/payments.py`
  - `routes/market_data.py`
- [x] Reduced server.py to minimal router inclusion

## Deployment Status: READY ✅
- Frontend: Running on port 3000 (200 OK)
- Backend: Running on port 8001 (healthy, v2.0.0)
- MongoDB: Connected
- Stripe: Configured and working

## Pending Tasks

### Backlog (Future)
- [ ] Subscription usage tracking (per-tenant limits, project counts)
- [ ] Admin billing/usage dashboard
- [ ] Remove outdated SQLAlchemy scripts
- [ ] Add frontend UI for subscription flow

## Test Credentials
- **Demo User**: demo@example.com / demo123
- **Test User**: test@example.com / test123

## Tech Stack
- Frontend: React, Vite, TypeScript, TailwindCSS, TanStack Query
- Backend: FastAPI, Python, Motor (async MongoDB)
- Database: MongoDB
- Payments: Stripe (via emergentintegrations)
- DevOps: Supervisor, Docker

---
*Last Updated: January 27, 2026*
*Version: 2.0.0 (Modular Architecture)*
