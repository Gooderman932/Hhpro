import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Check, Zap, Building2, Rocket } from 'lucide-react'
import { Button } from '../ui/button'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '../ui/card'
import { Badge } from '../ui/badge'
import { getPricingTiers, createCheckoutSession, getCurrentSubscription } from '../../services/api'
import type { PricingTier, Subscription } from '../../types/subscription'

const tierIcons: Record<string, React.ReactNode> = {
  basic: <Zap className="h-6 w-6" />,
  professional: <Building2 className="h-6 w-6" />,
  enterprise: <Rocket className="h-6 w-6" />
}

const tierColors: Record<string, string> = {
  basic: 'border-blue-500/50 hover:border-blue-500',
  professional: 'border-purple-500/50 hover:border-purple-500 ring-2 ring-purple-500/20',
  enterprise: 'border-amber-500/50 hover:border-amber-500'
}

export const PricingPage = () => {
  const navigate = useNavigate()
  const [tiers, setTiers] = useState<PricingTier[]>([])
  const [currentSubscription, setCurrentSubscription] = useState<Subscription | null>(null)
  const [loading, setLoading] = useState(true)
  const [checkoutLoading, setCheckoutLoading] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const isLoggedIn = !!localStorage.getItem('token')

  useEffect(() => {
    const fetchData = async () => {
      try {
        const tiersData = await getPricingTiers()
        setTiers(tiersData)

        if (isLoggedIn) {
          try {
            const sub = await getCurrentSubscription()
            setCurrentSubscription(sub)
          } catch {
            // User might not have a subscription
          }
        }
      } catch (err) {
        setError('Failed to load pricing information')
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [isLoggedIn])

  const handleSubscribe = async (tierId: string) => {
    if (!isLoggedIn) {
      navigate('/login?redirect=/pricing')
      return
    }

    setCheckoutLoading(tierId)
    setError(null)

    try {
      const { url } = await createCheckoutSession(tierId)
      window.location.href = url
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to start checkout')
      setCheckoutLoading(null)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-slate-950 to-slate-900 flex items-center justify-center">
        <div className="animate-pulse text-white">Loading pricing...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 to-slate-900 py-16 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <Badge variant="outline" className="mb-4 text-blue-400 border-blue-400/30">
            Market Data Intelligence
          </Badge>
          <h1 className="text-4xl sm:text-5xl font-bold text-white mb-4">
            Choose Your Plan
          </h1>
          <p className="text-lg text-slate-400 max-w-2xl mx-auto">
            Get access to powerful construction market analytics, competitor insights, and demand forecasting.
          </p>
        </div>

        {/* Current Subscription Banner */}
        {currentSubscription && (
          <div className="mb-8 p-4 bg-green-500/10 border border-green-500/30 rounded-lg text-center">
            <p className="text-green-400">
              <Check className="inline h-5 w-5 mr-2" />
              You're currently subscribed to <strong>{currentSubscription.tier_name}</strong>
              {currentSubscription.expires_at && (
                <span className="text-slate-400 ml-2">
                  (expires {new Date(currentSubscription.expires_at).toLocaleDateString()})
                </span>
              )}
            </p>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="mb-8 p-4 bg-red-500/10 border border-red-500/30 rounded-lg text-center">
            <p className="text-red-400">{error}</p>
          </div>
        )}

        {/* Pricing Cards */}
        <div className="grid md:grid-cols-3 gap-8">
          {tiers.map((tier) => {
            const isCurrentPlan = currentSubscription?.tier_id === tier.tier_id
            const isProfessional = tier.tier_id === 'professional'

            return (
              <Card
                key={tier.tier_id}
                data-testid={`pricing-card-${tier.tier_id}`}
                className={`relative bg-slate-900/50 backdrop-blur border-2 transition-all duration-300 ${tierColors[tier.tier_id] || 'border-slate-700'}`}
              >
                {isProfessional && (
                  <div className="absolute -top-3 left-1/2 -translate-x-1/2">
                    <Badge className="bg-purple-600 text-white">Most Popular</Badge>
                  </div>
                )}

                <CardHeader className="text-center pb-4">
                  <div className={`mx-auto p-3 rounded-full mb-4 ${
                    tier.tier_id === 'basic' ? 'bg-blue-500/20 text-blue-400' :
                    tier.tier_id === 'professional' ? 'bg-purple-500/20 text-purple-400' :
                    'bg-amber-500/20 text-amber-400'
                  }`}>
                    {tierIcons[tier.tier_id]}
                  </div>
                  <CardTitle className="text-2xl text-white">{tier.name}</CardTitle>
                  <CardDescription className="text-slate-400">
                    {tier.description}
                  </CardDescription>
                </CardHeader>

                <CardContent className="text-center">
                  <div className="mb-6">
                    <span className="text-5xl font-bold text-white">${tier.price}</span>
                    <span className="text-slate-400">/{tier.billing_period}</span>
                  </div>

                  <ul className="space-y-3 text-left">
                    {tier.features.map((feature, idx) => (
                      <li key={idx} className="flex items-start gap-3 text-slate-300">
                        <Check className="h-5 w-5 text-green-500 flex-shrink-0 mt-0.5" />
                        <span>{feature}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>

                <CardFooter>
                  <Button
                    data-testid={`subscribe-btn-${tier.tier_id}`}
                    className={`w-full ${
                      tier.tier_id === 'basic' ? 'bg-blue-600 hover:bg-blue-700' :
                      tier.tier_id === 'professional' ? 'bg-purple-600 hover:bg-purple-700' :
                      'bg-amber-600 hover:bg-amber-700'
                    } text-white`}
                    onClick={() => handleSubscribe(tier.tier_id)}
                    disabled={isCurrentPlan || checkoutLoading === tier.tier_id}
                  >
                    {checkoutLoading === tier.tier_id ? (
                      <span className="animate-pulse">Processing...</span>
                    ) : isCurrentPlan ? (
                      'Current Plan'
                    ) : (
                      'Get Started'
                    )}
                  </Button>
                </CardFooter>
              </Card>
            )
          })}
        </div>

        {/* Footer */}
        <div className="mt-16 text-center text-slate-500">
          <p>All plans include a 30-day money-back guarantee</p>
          <p className="mt-2">Need custom features? <a href="mailto:sales@hhdrywall.pro" className="text-blue-400 hover:underline">Contact sales</a></p>
        </div>
      </div>
    </div>
  )
}

export default PricingPage
