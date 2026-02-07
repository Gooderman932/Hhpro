# Production Environment Variables
## Construction Intelligence Platform - Poor Dude Holdings LLC

All variables below are required for production deployment. Set these in your hosting platform's environment configuration.

---

## Application

```bash
# Environment mode (development|production)
ENVIRONMENT=production
DEBUG=false

# JWT Secret Key - Generate a strong random key (64+ chars)
# python3 -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=<generate-strong-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Database (Supabase PostgreSQL)

```bash
# Connection string from Supabase dashboard → Settings → Database → Connection string (pooler)
DATABASE_URL=postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:5432/postgres
```

## Stripe (LIVE KEYS ONLY in Production)

```bash
# Dashboard: https://dashboard.stripe.com/apikeys
STRIPE_API_KEY=sk_live_...          # Secret key (NEVER starts with sk_test_ in production)
STRIPE_WEBHOOK_SECRET=whsec_...     # Webhook signing secret

# Optional: If using Stripe Price IDs for tiered billing
# Create products in Stripe Dashboard first, then add price IDs here
# STRIPE_PRICE_BASIC=price_...
# STRIPE_PRICE_PRO=price_...
# STRIPE_PRICE_ENTERPRISE=price_...
```

### How to Create Stripe Products

1. Go to https://dashboard.stripe.com/products
2. Click "Add product"
3. Create three products:

| Product | Price | Billing |
|---------|-------|---------|
| Basic | $49.00/month | Recurring |
| Pro | $149.00/month | Recurring |
| Enterprise | $399.00/month | Recurring |

4. Copy the secret key from https://dashboard.stripe.com/apikeys
5. Set up webhook at https://dashboard.stripe.com/webhooks
   - Endpoint URL: `https://your-domain.com/api/webhook/stripe`
   - Events to listen for:
     - `checkout.session.completed`
     - `customer.subscription.created`
     - `customer.subscription.updated`
     - `customer.subscription.deleted`
     - `invoice.payment_failed`
6. Copy the webhook signing secret

## External APIs (Optional - can be added after deployment)

```bash
# Federal Reserve Economic Data - Free API key
# Sign up: https://fred.stlouisfed.org/docs/api/api_key.html
FRED_API_KEY=<your-fred-api-key>

# Construction Permit Data Provider
# Options: PermitData.org, BuildZoom, or city-specific open data APIs
PERMIT_API_KEY=<your-permit-api-key>
```

## Email (Resend)

```bash
# Dashboard: https://resend.com/api-keys
RESEND_API_KEY=re_...
SENDER_EMAIL=notifications@your-domain.com
```

## CORS

```bash
# Comma-separated list of allowed frontend origins
# In production, restrict to your actual domain
CORS_ORIGINS=https://your-domain.com,https://www.your-domain.com
```

---

## .env.example Template

Copy this to your backend `.env` file and fill in values:

```
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=
STRIPE_API_KEY=
STRIPE_WEBHOOK_SECRET=
FRED_API_KEY=
PERMIT_API_KEY=
RESEND_API_KEY=
SENDER_EMAIL=
CORS_ORIGINS=
```
