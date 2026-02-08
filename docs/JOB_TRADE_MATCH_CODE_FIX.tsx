// ============================================
// JOB-TRADE-MATCH MARKET DATA FIX
// Add this to the MarketData.tsx or MarketData.jsx file
// ============================================

// STEP 1: Add this function inside your component (before the return statement)

const handleSubscribe = async (tierId: string) => {
  // Map old tier names to correct tier IDs
  const tierMap: Record<string, string> = {
    'basic': 'basic',
    'professional': 'professional', 
    'enterprise': 'enterprise'
  };
  
  const actualTierId = tierMap[tierId] || tierId;
  
  try {
    // Show loading state
    const btn = document.querySelector(`[data-testid="subscribe-${tierId}"]`) as HTMLButtonElement;
    if (btn) {
      btn.disabled = true;
      btn.textContent = 'Processing...';
    }
    
    // Call the Construction Intelligence backend
    const API_URL = 'https://agent-env-62160c2c-bc10-4173-9662-8ef2158aecee.stage-preview.emergentagent.com';
    
    const response = await fetch(`${API_URL}/api/stripe/public-checkout`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        tier_id: actualTierId,
        success_url: `${window.location.origin}/market-data?payment=success`,
        cancel_url: window.location.href
      })
    });
    
    if (!response.ok) {
      throw new Error('Failed to create checkout session');
    }
    
    const data = await response.json();
    
    if (data.checkout_url) {
      window.location.href = data.checkout_url;
    } else {
      throw new Error('No checkout URL returned');
    }
    
  } catch (error) {
    console.error('Subscription error:', error);
    alert('Error starting checkout. Please try again.');
    
    // Reset button
    const btn = document.querySelector(`[data-testid="subscribe-${tierId}"]`) as HTMLButtonElement;
    if (btn) {
      btn.disabled = false;
      btn.textContent = 'Subscribe Now';
    }
  }
};

// STEP 2: Update the pricing tiers array - replace the old prices
const tiers = [
  {
    id: 'basic',
    name: 'Basic Analytics',
    description: 'Essential market insights for growing businesses',
    price: 49,  // Changed from 299
    features: [
      'Regional labor market trends',
      'Basic wage analytics', 
      'Monthly industry reports',
      'Email support'
    ],
    popular: false
  },
  {
    id: 'professional',
    name: 'Professional Suite',
    description: 'Comprehensive analytics for established contractors',
    price: 149,  // Changed from 799
    features: [
      'All Basic features',
      'National market data',
      'Real-time wage tracking',
      'Competitor analysis',
      'Custom report generation',
      'Priority support'
    ],
    popular: true
  },
  {
    id: 'enterprise',
    name: 'Enterprise Platform',
    description: 'Full-scale intelligence for large construction firms',
    price: 399,  // Changed from 1999
    features: [
      'All Professional features',
      'API access',
      'Custom data integrations',
      'Predictive analytics',
      'Dedicated account manager',
      'White-label reports',
      '24/7 phone support'
    ],
    popular: false
  }
];

// STEP 3: Update each Subscribe button to have onClick handler
// Find this in your JSX:
//   <Button data-testid="subscribe-basic">Subscribe Now</Button>
// Change to:
//   <Button data-testid="subscribe-basic" onClick={() => handleSubscribe('basic')}>Subscribe Now</Button>

// Example button JSX:
/*
<Button 
  data-testid={`subscribe-${tier.id}`}
  onClick={() => handleSubscribe(tier.id)}
  className={tier.popular ? "bg-orange-500 hover:bg-orange-600" : "bg-slate-900 hover:bg-slate-800"}
>
  Subscribe Now
</Button>
*/
