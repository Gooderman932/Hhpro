# Production Deployment Checklist
## Construction Intelligence Platform - Poor Dude Holdings LLC

---

## Pre-Deployment

### Environment Setup
- [ ] All environment variables set (see `PRODUCTION_ENV_VARS.md`)
- [ ] `ENVIRONMENT=production` is set
- [ ] `SECRET_KEY` is a strong random value (not the development default)
- [ ] `CORS_ORIGINS` restricted to production domain only (not `*`)

### Stripe Configuration
- [ ] Stripe API key is LIVE mode (`sk_live_...`, NOT `sk_test_...`)
- [ ] Three Stripe products created with monthly recurring prices:
  - Basic: $49/month
  - Pro: $149/month
  - Enterprise: $399/month
- [ ] Webhook endpoint configured in Stripe dashboard
  - URL: `https://your-domain.com/api/webhook/stripe`
  - Events: `checkout.session.completed`, `customer.subscription.created`, `customer.subscription.updated`, `customer.subscription.deleted`, `invoice.payment_failed`
- [ ] Webhook signing secret (`whsec_...`) set in environment
- [ ] Test payment flow with a real card (then refund)

### Database
- [ ] Supabase PostgreSQL connection string is correct
- [ ] Database tables created (SQLAlchemy auto-creates on first run)
- [ ] Connection pooler URL used (not direct connection)

### Security Audit
- [ ] No `sk_test_` keys in production environment
- [ ] No API keys hardcoded in frontend code
- [ ] No database credentials in client-side code
- [ ] SSL/HTTPS enabled on domain
- [ ] CORS origins restricted to production domain

### External APIs (Optional)
- [ ] FRED API key obtained and set (or left empty for later)
- [ ] Permit data API key obtained and set (or left empty for later)

---

## Deployment Steps

1. **Set environment variables** in your hosting platform
2. **Deploy backend** (FastAPI application)
3. **Deploy frontend** (React/Vite build)
4. **Run database migrations** (auto-created by SQLAlchemy)
5. **Configure Stripe webhook** endpoint URL
6. **Test health endpoint**: `GET /health`
7. **Test full user flow**: Register → Pay → Onboarding → Dashboard

---

## Post-Deployment Verification

### Immediate (First 30 minutes)
- [ ] Health check returns `status: healthy` with `stripe_mode: live`
- [ ] Homepage loads correctly
- [ ] User registration works
- [ ] Login/logout works
- [ ] Pricing page shows correct tiers ($49/$149/$399)
- [ ] Stripe checkout redirects correctly
- [ ] Webhook processes payment events
- [ ] Subscription activates after payment
- [ ] Dashboard accessible for paid users
- [ ] ML predictions return valid results
- [ ] Onboarding wizard appears for new users
- [ ] No sample/test/demo data visible

### First 24 Hours
- [ ] Monitor error logs
- [ ] Check Stripe dashboard for successful payments
- [ ] Verify webhook events processing
- [ ] Test subscription cancellation flow
- [ ] Test tier upgrade flow
- [ ] Verify email notifications (if Resend configured)

---

## Monitoring

### Health Check Endpoint
```
GET /health
```
Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "stripe_mode": "live",
  "external_apis": {
    "fred": "connected" or "not_configured",
    "permits": "connected" or "not_configured"
  },
  "ml_models": "loaded"
}
```

### Key Metrics to Monitor
- API response times
- Error rate (should be < 1%)
- Stripe webhook delivery success rate
- Database connection pool usage
- ML model prediction latency

---

## Rollback Plan

If issues are detected post-deployment:
1. Use Emergent's "Rollback" feature to revert to previous checkpoint
2. Or revert environment variables to previous known-good state
3. Contact support if Stripe webhook issues persist

---

**© 2025 Poor Dude Holdings LLC. All Rights Reserved.**
