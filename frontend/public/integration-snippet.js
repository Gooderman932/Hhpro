/**
 * Construction Intelligence Platform - Website Integration
 * Poor Dude Holdings LLC
 * 
 * Include this script on your website to enable subscription buttons:
 * <script src="https://YOUR-BACKEND-URL/integration-snippet.js"></script>
 */

(function() {
  'use strict';
  
  // Auto-detect API URL from script source or use default
  const scripts = document.getElementsByTagName('script');
  let API_URL = '';
  
  for (let i = 0; i < scripts.length; i++) {
    const src = scripts[i].src;
    if (src && src.includes('integration-snippet.js')) {
      API_URL = src.replace('/integration-snippet.js', '');
      break;
    }
  }
  
  // Fallback to default
  if (!API_URL) {
    API_URL = 'https://agent-env-62160c2c-bc10-4173-9662-8ef2158aecee.stage-preview.emergentagent.com';
  }
  
  // Tier information
  const TIERS = {
    basic: { name: 'Basic', price: 49 },
    professional: { name: 'Pro', price: 149 },
    enterprise: { name: 'Enterprise', price: 399 }
  };
  
  /**
   * Subscribe to a tier
   * @param {string} tier - 'basic', 'professional', or 'enterprise'
   */
  async function subscribe(tier) {
    const btn = event?.target;
    const originalHTML = btn?.innerHTML;
    
    try {
      // Validate tier
      if (!TIERS[tier]) {
        throw new Error('Invalid tier: ' + tier);
      }
      
      // Loading state
      if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<span style="display:inline-flex;align-items:center;">Processing<span style="margin-left:8px;width:14px;height:14px;border:2px solid currentColor;border-top-color:transparent;border-radius:50%;animation:hhd-spin 1s linear infinite;"></span></span>';
      }
      
      // Create checkout session
      const response = await fetch(API_URL + '/api/stripe/public-checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tier_id: tier,
          success_url: window.location.origin + '/payment-success',
          cancel_url: window.location.href
        })
      });
      
      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || 'Failed to create checkout');
      }
      
      const data = await response.json();
      
      if (data.checkout_url) {
        window.location.href = data.checkout_url;
      } else {
        throw new Error('No checkout URL returned');
      }
      
    } catch (error) {
      console.error('HHD Subscription Error:', error);
      alert('Error: ' + error.message + '\n\nPlease try again or contact support.');
      
      if (btn) {
        btn.disabled = false;
        btn.innerHTML = originalHTML;
      }
    }
  }
  
  /**
   * Redirect to Market Data login
   */
  function goToMarketData() {
    window.location.href = API_URL + '/login';
  }
  
  // Add spinner animation style
  const style = document.createElement('style');
  style.textContent = '@keyframes hhd-spin { to { transform: rotate(360deg); } }';
  document.head.appendChild(style);
  
  // Expose functions globally
  window.HHDSubscribe = subscribe;
  window.HHDGoToMarketData = goToMarketData;
  
  // Also expose as simple function names for convenience
  window.subscribe = subscribe;
  window.goToMarketData = goToMarketData;
  
  console.log('✅ HH Drywall subscription integration loaded');
  console.log('   API URL:', API_URL);
  console.log('   Usage: subscribe("basic"), subscribe("professional"), subscribe("enterprise")');
})();
