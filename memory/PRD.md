# Construction Intelligence Platform - PRD

## Original Problem Statement
Build a working application from the user's private GitHub repository `gooderman932/market-data`. The scope evolved to perform a major technical migration from PostgreSQL to MongoDB and prepare the application for deployment.

## Product Overview
A full-stack construction intelligence platform with:
- **Frontend**: React/Vite/TypeScript with Tailwind CSS
- **Backend**: FastAPI with Python
- **Database**: MongoDB (migrated from PostgreSQL)
- **Process Management**: Supervisor

## Core Requirements
1. Database Migration: PostgreSQL/SQLAlchemy → MongoDB/Motor (async)
2. Dependency Cleanup: Remove all local ML libraries, Redis
3. Configuration: Environment-driven (.env files)
4. Deployment: Frontend port 3000, Backend port 8001
5. Feature: Market Data pricing tiers endpoint

## Current Architecture
```
/app/
├── backend/
│   ├── server.py        # Monolithic FastAPI app with MongoDB operations
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/  # Dashboard, Intelligence components
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── vite-env.d.ts
│   ├── dist/            # Built production assets
│   ├── vite.config.ts
│   ├── package.json
│   └── .env
└── scripts/             # Deployment and maintenance scripts
```

## Key API Endpoints
- `/api/auth/register`, `/api/auth/token`, `/api/auth/me`
- `/api/jobs`, `/api/jobs/{job_id}`
- `/api/workers`, `/api/workers/{profile_id}`
- `/api/products`, `/api/products/{product_id}/stock`
- `/api/orders`
- `/api/payments`
- `/api/pricing/tiers`
- `/health`

## Database Schema (MongoDB)
- **Database**: `construction_intel_db`
- **Collections**: `users`, `jobs`, `worker_profiles`, `products`, `orders`, `payment_transactions`, `user_sessions`, `subscriptions`

## What's Been Implemented ✅
- [x] Database Migration: PostgreSQL → MongoDB (Motor async driver)
- [x] Removed all SQLAlchemy, PostgreSQL, Redis dependencies
- [x] Backend consolidated into server.py with FastAPI
- [x] Configuration externalized to .env files
- [x] Frontend build errors fixed (TypeScript issues)
- [x] Supervisor configurations for production
- [x] Market Data pricing tiers endpoint (`/api/pricing/tiers`)
- [x] Frontend builds successfully (dist/ folder exists)
- [x] Deployment blockers resolved (.dockerignore, supervisor config)

## Deployment Status: READY ✅
- Frontend: Running on port 3000
- Backend: Running on port 8001
- MongoDB: Running
- All blockers resolved

## Pending Tasks (Priority Order)

### P1 - Performance Optimization (Non-blocking)
- [ ] Add MongoDB projections to queries in server.py
  - Jobs endpoint (line ~340)
  - Workers endpoint (line ~439)
  - Products endpoint (line ~545)
  - Orders endpoint (line ~621)

### P2 - Monetization Features
- [ ] Stripe integration for payments
- [ ] Subscription logic implementation
- [ ] Usage tracking and credit system
- [ ] Admin billing dashboard

### P3 - Code Quality
- [ ] Refactor server.py into modular structure (routers, models, services)
- [ ] Remove outdated SQLAlchemy scripts (seed_data.py, setup_db.py, verify_database.py)
- [ ] Consider removing unused openai dependency if not needed

## Test Credentials
- **Demo User**: demo@example.com / demo123

## Tech Stack
- Frontend: React, Vite, TypeScript, TailwindCSS, TanStack Query
- Backend: FastAPI, Python, Motor (async MongoDB)
- Database: MongoDB
- DevOps: Supervisor, Docker

---
*Last Updated: January 27, 2026*
