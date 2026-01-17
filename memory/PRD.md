# HDrywall Repair Platform - PRD

## Original Problem Statement
Build a platform for hdrywall repair.com that:
1. Allows contractors to post jobs with specific trade codes (09-Drywall/Paint, etc.), location, pay rate, duration, certifications
2. Allows subcontractors to create profiles with skills, trade codes, experience, availability
3. Partial profile visibility - users can see enough to draw interest but cannot contact directly (staff-mediated monetization)
4. Market data analysis with 3-tiered options for big businesses in construction industry
5. E-commerce/dropshipping platform for contractor tools with categories, inventory management, Stripe checkout

## User Personas
- **Contractors**: Businesses seeking skilled subcontractors for projects. Can post jobs, browse worker profiles, purchase tools
- **Subcontractors**: Skilled tradespeople seeking work. Can create profiles, browse job listings, purchase tools
- **Business Enterprises**: Large construction firms needing market data analytics (3-tier subscription)
- **Tool Buyers**: Any user purchasing contractor tools from the shop

## Core Requirements
- Separate roles: Contractor & Subcontractor
- Both JWT email/password auth AND Google social login (Emergent OAuth)
- Staff-mediated connections (contact info hidden for monetization)
- Trade codes system (CSI MasterFormat: 03-Concrete, 04-Masonry, 05-Metals, 06-Wood, 07-Thermal, 08-Openings, 09-Finishes, etc.)
- E-commerce with Stripe checkout
- Market data analytics tiers: Basic ($299/mo), Professional ($799/mo), Enterprise ($1999/mo)

## What's Been Implemented (January 2025)

### Backend (FastAPI)
- ✅ User authentication (JWT + Emergent Google OAuth)
- ✅ User registration with role selection
- ✅ Job listings CRUD with trade codes, location, pay rate, duration, certifications
- ✅ Worker profiles CRUD with skills, experience, availability
- ✅ Products catalog with categories
- ✅ Shopping cart functionality
- ✅ Stripe checkout integration
- ✅ Market data tiers with Stripe subscription
- ✅ Payment transactions tracking

### Frontend (React)
- ✅ Landing page with hero section, service cards, CTAs
- ✅ User registration & login (email/password + Google)
- ✅ Dashboard for contractors and subcontractors
- ✅ Job Board with filters (trade code, state, city)
- ✅ Job posting form for contractors
- ✅ Worker profiles listing with filters
- ✅ Profile creation form for subcontractors
- ✅ Pro Shop with 12 seeded products
- ✅ Shopping cart & checkout flow
- ✅ Market data tiers page
- ✅ Professional construction-themed UI (Oswald + Inter fonts, slate/orange color scheme)

### Database Collections
- users
- user_sessions
- jobs
- worker_profiles
- products
- carts
- orders
- payment_transactions

## Prioritized Backlog

### P0 - Critical (Deferred)
- Admin dashboard for staff to manage job/profile connections
- Contact request system (staff-mediated)

### P1 - High Priority
- Order history page
- User profile editing
- Job editing/closing for contractors
- Profile editing for subcontractors
- Email notifications

### P2 - Medium Priority
- Advanced search/filtering
- Saved jobs/profiles
- Analytics dashboard for contractors
- Reviews/ratings system

### P3 - Nice to Have
- Mobile app
- Real-time notifications
- Chat system (staff-managed)
- Invoice generation

## Next Tasks
1. Build admin dashboard for staff to manage connections
2. Implement contact request flow
3. Add order history page
4. Set up email notifications
5. Consider adding real product inventory from dropshipping suppliers
