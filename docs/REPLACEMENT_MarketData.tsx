import { useState } from 'react';
import { Check, BarChart3, TrendingUp, Building2 } from 'lucide-react';
import { Card, CardContent } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Button } from '../components/ui/button';

// Correct pricing tiers
const tiers = [
  {
    id: 'basic',
    name: 'Basic Analytics',
    description: 'Essential market insights for growing businesses',
    price: 49,
    icon: BarChart3,
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
    price: 149,
    icon: TrendingUp,
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
    price: 399,
    icon: Building2,
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

const includedFeatures = [
  { title: 'Labor Trends', description: 'Regional and national workforce analytics' },
  { title: 'Wage Data', description: 'Real-time compensation benchmarks' },
  { title: 'Market Reports', description: 'Monthly industry insights' },
  { title: 'Custom Analysis', description: 'Tailored data for your needs' }
];

// Backend API URL - Construction Intelligence Platform
const API_URL = 'https://agent-env-62160c2c-bc10-4173-9662-8ef2158aecee.stage-preview.emergentagent.com';

export default function MarketData() {
  const [loadingTier, setLoadingTier] = useState<string | null>(null);

  // Handle subscription checkout
  const handleSubscribe = async (tierId: string) => {
    setLoadingTier(tierId);
    
    try {
      const response = await fetch(`${API_URL}/api/stripe/public-checkout`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tier_id: tierId,
          success_url: `${window.location.origin}/market-data?payment=success`,
          cancel_url: window.location.href
        })
      });
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Failed to create checkout session');
      }
      
      const data = await response.json();
      
      if (data.checkout_url) {
        // Redirect to Stripe checkout
        window.location.href = data.checkout_url;
      } else {
        throw new Error('No checkout URL returned');
      }
      
    } catch (error: any) {
      console.error('Subscription error:', error);
      alert('Error starting checkout: ' + (error.message || 'Please try again.'));
      setLoadingTier(null);
    }
  };

  // Check for payment success on page load
  const urlParams = new URLSearchParams(window.location.search);
  const paymentSuccess = urlParams.get('payment') === 'success';

  return (
    <div className="min-h-screen bg-slate-50" data-testid="market-data-page">
      {/* Success Banner */}
      {paymentSuccess && (
        <div className="bg-green-500 text-white py-4 px-6 text-center">
          <p className="font-semibold">
            🎉 Payment Successful! Check your email for login instructions to access Market Data.
          </p>
          <button 
            onClick={() => window.history.replaceState({}, '', window.location.pathname)}
            className="ml-4 underline text-sm"
          >
            Dismiss
          </button>
        </div>
      )}

      {/* Hero Section */}
      <div className="bg-gradient-to-br from-slate-900 to-slate-800 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <Badge className="bg-orange-500/20 text-orange-400 border-orange-500/30 mb-4">
            For Enterprise
          </Badge>
          <h1 className="text-4xl md:text-5xl font-bold font-['Oswald'] uppercase tracking-tight mb-4">
            Market Data Analytics
          </h1>
          <p className="text-xl text-slate-300 max-w-2xl mx-auto">
            Comprehensive construction industry intelligence to power your business decisions
          </p>
        </div>
      </div>

      {/* Pricing Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid md:grid-cols-3 gap-8">
          {tiers.map((tier) => {
            const Icon = tier.icon;
            const isLoading = loadingTier === tier.id;
            
            return (
              <Card
                key={tier.id}
                className={`relative ${
                  tier.popular 
                    ? 'border-2 border-orange-500 shadow-lg scale-105' 
                    : 'border border-slate-200'
                }`}
                data-testid={`tier-card-${tier.id}`}
              >
                {tier.popular && (
                  <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                    <Badge className="bg-orange-500 text-white">MOST POPULAR</Badge>
                  </div>
                )}
                
                <CardContent className="p-8">
                  {/* Icon and Title */}
                  <div className="text-center mb-6">
                    <div className={`w-14 h-14 bg-slate-100 rounded-sm flex items-center justify-center mx-auto mb-4`}>
                      <Icon className={`w-7 h-7 ${tier.popular ? 'text-orange-500' : 'text-slate-600'}`} />
                    </div>
                    <h3 className="text-xl font-bold text-slate-900 font-['Oswald'] uppercase mb-1">
                      {tier.name}
                    </h3>
                    <p className="text-sm text-slate-600">{tier.description}</p>
                  </div>
                  
                  {/* Price */}
                  <div className="text-center mb-6">
                    <span className="text-4xl font-bold text-slate-900">${tier.price}</span>
                    <span className="text-slate-500">/monthly</span>
                  </div>
                  
                  {/* Features */}
                  <ul className="space-y-3 mb-8">
                    {tier.features.map((feature, idx) => (
                      <li key={idx} className="flex items-start gap-2 text-sm">
                        <Check className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                        <span className="text-slate-600">{feature}</span>
                      </li>
                    ))}
                  </ul>
                  
                  {/* Subscribe Button */}
                  <Button
                    className={`w-full rounded-sm py-6 ${
                      tier.popular 
                        ? 'bg-orange-500 hover:bg-orange-600 text-white' 
                        : 'bg-slate-900 hover:bg-slate-800 text-white'
                    }`}
                    onClick={() => handleSubscribe(tier.id)}
                    disabled={isLoading}
                    data-testid={`subscribe-${tier.id}`}
                  >
                    {isLoading ? 'Processing...' : 'Subscribe Now'}
                  </Button>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {/* Features Grid */}
        <div className="mt-20 text-center">
          <h2 className="text-2xl font-bold text-slate-900 font-['Oswald'] uppercase mb-8">
            What's Included
          </h2>
          <div className="grid md:grid-cols-4 gap-6">
            {includedFeatures.map((feature, idx) => (
              <div key={idx} className="bg-white p-6 border border-slate-200 rounded-sm">
                <h4 className="font-semibold text-slate-900 mb-2">{feature.title}</h4>
                <p className="text-sm text-slate-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
