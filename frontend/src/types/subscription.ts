// Subscription and Pricing Types

export interface PricingTier {
  tier_id: string
  name: string
  price: number
  billing_period: string
  description: string
  features: string[]
}

export interface Subscription {
  subscription_id: string
  user_id: string
  tier_id: string
  tier_name: string
  status: string
  price: number
  created_at: string
  expires_at: string | null
}

export interface CheckoutResponse {
  url: string
  session_id: string
}

export interface PaymentStatus {
  status: string
  payment_status: string
  subscription: Subscription | null
}
