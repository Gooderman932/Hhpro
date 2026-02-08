# Website Integration Guide for hhdrywallrepair.com

## Problem
The main website (hhdrywallrepair.com) is a static/WordPress site that needs to connect to our Construction Intelligence Platform backend. Currently, subscription buttons don't work because there's no JavaScript connecting them to the Stripe checkout flow.

## Solution
Add JavaScript code to your hhdrywallrepair.com website that calls our API to create Stripe checkout sessions.

---

## Quick Start (Copy-Paste)

### Minimal Integration
Add this single script tag to any page with subscription buttons:

```html
<script src="https://agent-env-62160c2c-bc10-4173-9662-8ef2158aecee.stage-preview.emergentagent.com/integration-snippet.js"></script>
```

Or copy the contents from `/frontend/public/integration-snippet.html`

---

## Full Integration Guide

### Step 1: Add JavaScript to Your Site

Add this code to your website's `<head>` section or create a separate `subscription.js` file:

```html
<script>
// ============================================
// Construction Intelligence Platform Integration
// Poor Dude Holdings LLC
// ============================================

// Configuration - UPDATE THIS to your deployed backend URL
const API_BASE_URL = 'https://agent-env-62160c2c-bc10-4173-9662-8ef2158aecee.stage-preview.emergentagent.com';

// Your website URLs
const SUCCESS_URL = 'https://hhdrywallrepair.com/payment-success';
const CANCEL_URL = 'https://hhdrywallrepair.com/pricing';

// Tier mapping
const TIER_INFO = {
  basic: { name: 'Basic', price: 49 },
  professional: { name: 'Pro', price: 149 },
  enterprise: { name: 'Enterprise', price: 399 }
};

/**
 * Subscribe to a tier - redirects to Stripe checkout
 * @param {string} tier - 'basic', 'professional', or 'enterprise'
 */
async function subscribeToTier(tier) {
  const button = event?.target;
  
  try {
    // Show loading state
    if (button) {
      button.disabled = true;
      button.innerHTML = '<span class="loading">Processing...</span>';
    }
    document.body.style.cursor = 'wait';
    
    // Validate tier
    if (!TIER_INFO[tier]) {
      throw new Error('Invalid subscription tier');
    }
    
    // Call backend to create Stripe checkout session
    const response = await fetch(`${API_BASE_URL}/api/stripe/public-checkout`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        tier_id: tier,
        success_url: SUCCESS_URL,
        cancel_url: CANCEL_URL
      })
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || 'Failed to create checkout session');
    }
    
    const data = await response.json();
    
    // Redirect to Stripe checkout
    if (data.checkout_url) {
      window.location.href = data.checkout_url;
    } else {
      throw new Error('No checkout URL returned');
    }
    
  } catch (error) {
    console.error('Subscription error:', error);
    alert(`Something went wrong: ${error.message}\n\nPlease try again or contact support.`);
    
    // Reset button state
    if (button) {
      button.disabled = false;
      const tierData = TIER_INFO[tier];
      button.innerHTML = `Subscribe to ${tierData?.name || tier} - $${tierData?.price || '??'}/month`;
    }
    document.body.style.cursor = 'default';
  }
}

/**
 * Redirect to Market Data login page
 */
function accessMarketData() {
  window.location.href = `${API_BASE_URL}/login`;
}

/**
 * Check subscription status (for logged-in users)
 */
async function checkSubscriptionStatus() {
  const token = localStorage.getItem('hhd_token');
  if (!token) return null;
  
  try {
    const response = await fetch(`${API_BASE_URL}/api/subscription/current`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (response.ok) {
      return await response.json();
    }
  } catch (e) {
    console.error('Error checking subscription:', e);
  }
  return null;
}

// Log integration loaded
console.log('Construction Intelligence Platform integration loaded');
</script>
```

### Step 2: Update Your HTML Buttons

Replace your current pricing buttons with these:

```html
<!-- Basic Tier - $49/month -->
<button 
  onclick="subscribeToTier('basic')" 
  class="subscribe-btn subscribe-basic"
  data-testid="subscribe-basic-btn"
>
  Subscribe to Basic - $49/month
</button>

<!-- Pro Tier - $149/month (Most Popular) -->
<button 
  onclick="subscribeToTier('professional')" 
  class="subscribe-btn subscribe-pro"
  data-testid="subscribe-pro-btn"
>
  Subscribe to Pro - $149/month
</button>

<!-- Enterprise Tier - $399/month -->
<button 
  onclick="subscribeToTier('enterprise')" 
  class="subscribe-btn subscribe-enterprise"
  data-testid="subscribe-enterprise-btn"
>
  Subscribe to Enterprise - $399/month
</button>

<!-- Login button for existing subscribers -->
<button 
  onclick="accessMarketData()" 
  class="login-btn"
  data-testid="access-market-data-btn"
>
  Already Subscribed? Access Market Data →
</button>
```

### Step 3: Add Styling (Optional)

Add this CSS for professional-looking buttons:

```css
/* Subscription Buttons */
.subscribe-btn {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  color: white;
  padding: 14px 28px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3);
  display: inline-block;
  margin: 8px;
}

.subscribe-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4);
}

.subscribe-btn:active {
  transform: translateY(0);
}

.subscribe-btn:disabled {
  background: #9ca3af;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

/* Pro tier highlight */
.subscribe-pro {
  background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
  box-shadow: 0 4px 14px rgba(124, 58, 237, 0.3);
  position: relative;
}

.subscribe-pro::before {
  content: 'MOST POPULAR';
  position: absolute;
  top: -10px;
  left: 50%;
  transform: translateX(-50%);
  background: #f59e0b;
  color: white;
  font-size: 10px;
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: bold;
}

/* Enterprise tier */
.subscribe-enterprise {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  box-shadow: 0 4px 14px rgba(245, 158, 11, 0.3);
}

/* Login button */
.login-btn {
  background: white;
  color: #2563eb;
  border: 2px solid #2563eb;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.login-btn:hover {
  background: #eff6ff;
  border-color: #1d4ed8;
}

/* Loading state */
.loading {
  display: inline-flex;
  align-items: center;
}

.loading::after {
  content: '';
  width: 16px;
  height: 16px;
  margin-left: 8px;
  border: 2px solid white;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
```

---

## WordPress Integration

### Option 1: Using a Plugin (Easiest)

1. Install **"Insert Headers and Footers"** plugin
2. Go to Settings → Insert Headers and Footers
3. Paste the JavaScript code in the "Scripts in Header" section
4. Save

### Option 2: Theme Customizer

1. Go to Appearance → Customize → Additional CSS/JavaScript
2. Add the JavaScript code
3. Publish

### Option 3: Theme Functions.php

Add to your theme's `functions.php`:

```php
function add_subscription_script() {
    ?>
    <script>
    // Paste the JavaScript code here
    </script>
    <?php
}
add_action('wp_head', 'add_subscription_script');
```

### Option 4: Elementor/Page Builder

1. Add a "Custom HTML" or "JavaScript" widget
2. Paste the code
3. Save

---

## Complete HTML Page Example

Here's a complete pricing page you can use:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Pricing - HH Drywall Construction Intelligence</title>
  
  <!-- Add the integration script -->
  <script>
    const API_BASE_URL = 'https://agent-env-62160c2c-bc10-4173-9662-8ef2158aecee.stage-preview.emergentagent.com';
    const SUCCESS_URL = window.location.origin + '/payment-success';
    const CANCEL_URL = window.location.origin + '/pricing';
    
    async function subscribeToTier(tier) {
      const btn = event.target;
      btn.disabled = true;
      btn.textContent = 'Processing...';
      
      try {
        const res = await fetch(`${API_BASE_URL}/api/stripe/public-checkout`, {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ tier_id: tier, success_url: SUCCESS_URL, cancel_url: CANCEL_URL })
        });
        const data = await res.json();
        if (data.checkout_url) window.location.href = data.checkout_url;
        else throw new Error('No checkout URL');
      } catch (e) {
        alert('Error: ' + e.message);
        btn.disabled = false;
        btn.textContent = 'Try Again';
      }
    }
    
    function accessMarketData() {
      window.location.href = API_BASE_URL + '/login';
    }
  </script>
  
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: system-ui, sans-serif; background: #0f172a; color: white; }
    .pricing-container { max-width: 1200px; margin: 0 auto; padding: 60px 20px; }
    h1 { text-align: center; font-size: 2.5rem; margin-bottom: 1rem; }
    .subtitle { text-align: center; color: #94a3b8; margin-bottom: 3rem; }
    .pricing-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px; }
    .pricing-card { background: #1e293b; border-radius: 16px; padding: 32px; border: 2px solid #334155; }
    .pricing-card.popular { border-color: #7c3aed; }
    .tier-name { font-size: 1.5rem; font-weight: bold; margin-bottom: 8px; }
    .tier-price { font-size: 3rem; font-weight: bold; margin-bottom: 16px; }
    .tier-price span { font-size: 1rem; color: #94a3b8; }
    .features { list-style: none; margin-bottom: 24px; }
    .features li { padding: 8px 0; border-bottom: 1px solid #334155; }
    .features li::before { content: '✓ '; color: #22c55e; }
    button { width: 100%; padding: 14px; border: none; border-radius: 8px; font-size: 16px; font-weight: 600; cursor: pointer; }
    .btn-basic { background: #2563eb; color: white; }
    .btn-pro { background: #7c3aed; color: white; }
    .btn-enterprise { background: #f59e0b; color: white; }
    button:hover { opacity: 0.9; }
    button:disabled { background: #64748b; cursor: wait; }
    .login-section { text-align: center; margin-top: 40px; }
    .login-btn { background: transparent; border: 2px solid #2563eb; color: #2563eb; width: auto; padding: 12px 32px; }
  </style>
</head>
<body>
  <div class="pricing-container">
    <h1>Construction Market Intelligence</h1>
    <p class="subtitle">Get the competitive edge with AI-powered permit data and insights</p>
    
    <div class="pricing-grid">
      <!-- Basic -->
      <div class="pricing-card">
        <div class="tier-name">Basic</div>
        <div class="tier-price">$49<span>/month</span></div>
        <ul class="features">
          <li>25 permits per search</li>
          <li>Major metro coverage</li>
          <li>Market analytics dashboard</li>
          <li>Email support</li>
        </ul>
        <button class="btn-basic" onclick="subscribeToTier('basic')">Get Started</button>
      </div>
      
      <!-- Pro -->
      <div class="pricing-card popular">
        <div class="tier-name">Pro <span style="background:#7c3aed;padding:2px 8px;border-radius:4px;font-size:12px;">POPULAR</span></div>
        <div class="tier-price">$149<span>/month</span></div>
        <ul class="features">
          <li>100 permits per search</li>
          <li>Nationwide coverage</li>
          <li>Federal procurement opportunities</li>
          <li>ML-powered insights</li>
          <li>Competitor tracking</li>
          <li>Priority support</li>
        </ul>
        <button class="btn-pro" onclick="subscribeToTier('professional')">Get Started</button>
      </div>
      
      <!-- Enterprise -->
      <div class="pricing-card">
        <div class="tier-name">Enterprise</div>
        <div class="tier-price">$399<span>/month</span></div>
        <ul class="features">
          <li>250 permits per search</li>
          <li>All data sources</li>
          <li>API access</li>
          <li>Custom model training</li>
          <li>White-glove onboarding</li>
          <li>Dedicated account manager</li>
        </ul>
        <button class="btn-enterprise" onclick="subscribeToTier('enterprise')">Contact Sales</button>
      </div>
    </div>
    
    <div class="login-section">
      <button class="login-btn" onclick="accessMarketData()">Already a subscriber? Access Market Data →</button>
    </div>
  </div>
</body>
</html>
```

---

## Troubleshooting

### Button does nothing
1. Open browser console (F12 → Console tab)
2. Look for error messages
3. Verify `API_BASE_URL` is correct
4. Check if script is loaded

### CORS Error
If you see "Access to fetch blocked by CORS policy":
- The backend needs to allow your domain
- Contact support to add hhdrywallrepair.com to allowed origins

### Redirect fails after payment
1. Verify `success_url` points to a real page on your site
2. Create a `/payment-success` page with a thank you message
3. Check Stripe dashboard for webhook errors

### "Invalid tier" error
- Use exact tier IDs: `basic`, `professional`, `enterprise`
- Don't use `pro` (use `professional`)

---

## Support

- **Technical Issues**: Check browser console for errors
- **Payment Issues**: Check Stripe dashboard
- **Integration Help**: Contact support@hhdrywallrepair.com

---

*Last Updated: February 2025*
*Construction Intelligence Platform v2.1*
