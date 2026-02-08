# Deployment Guide: Construction Intelligence Platform

## Current Situation

You have **two separate Emergent apps**:

| App | URL | Status |
|-----|-----|--------|
| **job-trade-match** | `job-trade-match.preview.emergentagent.com` | Has broken Market Data with old pricing |
| **Construction Intelligence** | `agent-env-62160c2c...stage-preview.emergentagent.com` | Working app with correct pricing |

## Deployment Options

### Option 1: Quick Fix for job-trade-match (Immediate)

Add this script to the job-trade-match Market Data page:

```html
<script src="https://agent-env-62160c2c-bc10-4173-9662-8ef2158aecee.stage-preview.emergentagent.com/integration-snippet.js"></script>
<script>
// Fix pricing and attach handlers
document.addEventListener('DOMContentLoaded', function() {
  // Fix prices
  document.body.innerHTML = document.body.innerHTML
    .replace(/\$299/g, '$49')
    .replace(/\$799/g, '$149')
    .replace(/\$1,?999/g, '$399');
  
  // Find subscribe buttons and attach handlers
  document.querySelectorAll('button').forEach(btn => {
    if (btn.textContent.toLowerCase().includes('subscribe')) {
      const card = btn.closest('div') || btn.parentElement;
      const text = card?.textContent || '';
      
      let tier = 'basic';
      if (text.includes('Professional')) tier = 'professional';
      if (text.includes('Enterprise')) tier = 'enterprise';
      
      btn.onclick = () => subscribe(tier);
    }
  });
});
</script>
```

**Pros:** Immediate fix, no deployment needed
**Cons:** Relies on external script, not ideal for production

---

### Option 2: Replace Market Data Section (Recommended)

The Construction Intelligence Platform should **replace** the Market Data section of job-trade-match.

**Steps in Emergent:**

1. **Open job-trade-match project** in Emergent dashboard
2. **Navigate to Market Data components** (likely in `/src/components/market-data/` or similar)
3. **Replace the pricing/subscription components** with code from this project

**Key files to copy:**
```
From: Construction Intelligence (this project)
├── frontend/src/components/pricing/PricingPage.tsx
├── frontend/src/services/api.ts (subscription functions)
└── frontend/public/integration-snippet.js

To: job-trade-match project
└── Replace market-data pricing components
```

---

### Option 3: Merge Apps via GitHub (Production)

1. **Export this project to GitHub** using Emergent's "Save to GitHub" feature
2. **In job-trade-match**, import the relevant components
3. **Update routing** to use new Market Data components

---

## Environment Variables Required

Make sure job-trade-match has these in `.env`:

```bash
# Stripe (for payments)
STRIPE_API_KEY=sk_live_... # or sk_test_... for testing
STRIPE_WEBHOOK_SECRET=whsec_...

# Database (already configured in job-trade-match)
DATABASE_URL=postgresql://...

# API Keys for data sources
FRED_API_KEY=your_fred_key
CENSUS_API_KEY=your_census_key
```

---

## API Endpoints to Add

If merging manually, add these endpoints to job-trade-match backend:

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/stripe/public-checkout` | POST | None | Create checkout without login |
| `/api/permits/search` | GET | Basic+ | Search permits |
| `/api/procurement/federal` | GET | Pro+ | Federal opportunities |
| `/api/admin/revenue` | GET | Admin | Revenue dashboard |

---

## Quick Test After Deployment

```bash
# Test public checkout
curl -X POST https://YOUR-DOMAIN/api/stripe/public-checkout \
  -H "Content-Type: application/json" \
  -d '{"tier_id": "basic"}'

# Should return:
# {"checkout_url": "https://checkout.stripe.com/...", "session_id": "cs_..."}
```

---

## Recommended Path Forward

1. **TODAY**: Apply quick fix to job-trade-match (Option 1)
2. **THIS WEEK**: Plan component migration (Option 2)
3. **PRODUCTION**: Full deployment with proper CI/CD (Option 3)

---

## Support

If you need help with deployment:
- Use Emergent's "Save to GitHub" to version control
- Contact Emergent support for app merging questions
- Check `/app/docs/WEBSITE_INTEGRATION.md` for integration details

---

*Last Updated: February 2025*
