import { useState, useEffect } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
import { Check, Loader2, XCircle } from 'lucide-react'
import { Button } from '../ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card'
import { getPaymentStatus } from '../../services/api'
import type { Subscription } from '../../types/subscription'

export const SubscriptionSuccess = () => {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const sessionId = searchParams.get('session_id')

  const [status, setStatus] = useState<'loading' | 'success' | 'pending' | 'error'>('loading')
  const [subscription, setSubscription] = useState<Subscription | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [pollCount, setPollCount] = useState(0)

  useEffect(() => {
    if (!sessionId) {
      setStatus('error')
      setError('No session ID found')
      return
    }

    const pollPaymentStatus = async () => {
      try {
        const result = await getPaymentStatus(sessionId)

        if (result.payment_status === 'paid') {
          setStatus('success')
          setSubscription(result.subscription)
          return true // Stop polling
        } else if (result.status === 'expired') {
          setStatus('error')
          setError('Payment session expired. Please try again.')
          return true // Stop polling
        }

        // Still pending
        setStatus('pending')
        return false // Continue polling
      } catch (err: any) {
        // Continue polling on error, but limit attempts
        if (pollCount >= 5) {
          setStatus('error')
          setError('Unable to verify payment. Please contact support.')
          return true // Stop polling
        }
        return false // Continue polling
      }
    }

    // Initial poll
    pollPaymentStatus().then((shouldStop) => {
      if (!shouldStop) {
        // Set up interval for continued polling
        const interval = setInterval(async () => {
          setPollCount((prev) => {
            if (prev >= 5) {
              clearInterval(interval)
              return prev
            }
            return prev + 1
          })

          const shouldStop = await pollPaymentStatus()
          if (shouldStop) {
            clearInterval(interval)
          }
        }, 2000) // Poll every 2 seconds

        return () => clearInterval(interval)
      }
    })
  }, [sessionId, pollCount])

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 to-slate-900 flex items-center justify-center py-16 px-4">
      <Card className="max-w-md w-full bg-slate-900/50 backdrop-blur border-slate-700">
        <CardHeader className="text-center">
          {status === 'loading' || status === 'pending' ? (
            <>
              <div className="mx-auto p-4 rounded-full bg-blue-500/20 mb-4">
                <Loader2 className="h-8 w-8 text-blue-400 animate-spin" />
              </div>
              <CardTitle className="text-2xl text-white">
                {status === 'loading' ? 'Verifying Payment...' : 'Processing...'}
              </CardTitle>
              <CardDescription className="text-slate-400">
                Please wait while we confirm your subscription
              </CardDescription>
            </>
          ) : status === 'success' ? (
            <>
              <div className="mx-auto p-4 rounded-full bg-green-500/20 mb-4">
                <Check className="h-8 w-8 text-green-400" />
              </div>
              <CardTitle className="text-2xl text-white">Payment Successful!</CardTitle>
              <CardDescription className="text-slate-400">
                Your subscription is now active
              </CardDescription>
            </>
          ) : (
            <>
              <div className="mx-auto p-4 rounded-full bg-red-500/20 mb-4">
                <XCircle className="h-8 w-8 text-red-400" />
              </div>
              <CardTitle className="text-2xl text-white">Payment Issue</CardTitle>
              <CardDescription className="text-red-400">
                {error || 'Something went wrong'}
              </CardDescription>
            </>
          )}
        </CardHeader>

        <CardContent className="text-center space-y-6">
          {status === 'success' && subscription && (
            <div className="bg-slate-800/50 rounded-lg p-4 text-left space-y-2">
              <div className="flex justify-between">
                <span className="text-slate-400">Plan:</span>
                <span className="text-white font-medium">{subscription.tier_name}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Amount:</span>
                <span className="text-white font-medium">${subscription.price}/month</span>
              </div>
              {subscription.expires_at && (
                <div className="flex justify-between">
                  <span className="text-slate-400">Renewal:</span>
                  <span className="text-white font-medium">
                    {new Date(subscription.expires_at).toLocaleDateString()}
                  </span>
                </div>
              )}
            </div>
          )}

          <div className="flex flex-col gap-3">
            {status === 'success' && (
              <Button
                data-testid="go-to-dashboard-btn"
                className="w-full bg-green-600 hover:bg-green-700"
                onClick={() => navigate('/')}
              >
                Go to Dashboard
              </Button>
            )}

            {status === 'error' && (
              <Button
                data-testid="try-again-btn"
                className="w-full bg-blue-600 hover:bg-blue-700"
                onClick={() => navigate('/pricing')}
              >
                Try Again
              </Button>
            )}

            <Button
              data-testid="view-pricing-btn"
              variant="outline"
              className="w-full border-slate-600 text-slate-300 hover:bg-slate-800"
              onClick={() => navigate('/pricing')}
            >
              View Plans
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default SubscriptionSuccess
