from datetime import datetime, timedelta
import secrets

# Subscription status types
SUBSCRIPTION_STATUS = {
    "active": "Active subscription with full access",
    "expired": "Subscription period ended",
    "cancelled": "User cancelled subscription",
    "pending": "Payment processing",
    "failed": "Payment failed"
}

@api_router.post("/api/subscriptions/subscribe")
async def create_subscription(request: Request):
    """Create a new Market Data subscription"""
    data = await request.json()
    user = await require_user(request)
    
    tier_id = data.get("tier_id")
    
    # Find tier details
    tier = next((t for t in MARKET_DATA_TIERS if t["tier_id"] == tier_id), None)
    if not tier:
        raise HTTPException(status_code=404, detail="Tier not found")
    
    # Check for existing active subscription
    existing = await db.subscriptions.find_one({
        "user_id": user["user_id"],
        "status": "active"
    })
    
    if existing:
        raise HTTPException(
            status_code=400, 
            detail="You already have an active subscription. Please cancel it first."
        )
    
    # Create Stripe Checkout Session
    import stripe
    stripe.api_key = os.environ.get("STRIPE_API_KEY")
    
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(tier["price"] * 100),  # Convert to cents
                    'product_data': {
                        'name': tier["name"],
                        'description': tier["description"],
                    },
                    'recurring': {
                        'interval': 'month',
                    },
                },
                'quantity': 1,
            }],
            mode='subscription',
            success_url=f'{request.base_url}dashboard?session_id={{CHECKOUT_SESSION_ID}}',
            cancel_url=f'{request.base_url}market-data',
            client_reference_id=user["user_id"],
            metadata={
                'tier_id': tier_id,
                'user_id': user["user_id"],
                'tier_name': tier["name"]
            }
        )
        
        # Create pending subscription record
        subscription_id = "sub_" + secrets.token_urlsafe(16)
        
        await db.subscriptions.insert_one({
            "subscription_id": subscription_id,
            "user_id": user["user_id"],
            "tier_id": tier_id,
            "tier_name": tier["name"],
            "price": tier["price"],
            "billing_period": tier["billing_period"],
            "status": "pending",
            "stripe_session_id": checkout_session.id,
            "stripe_subscription_id": None,  # Will be filled after webhook
            "created_at": datetime.utcnow().isoformat(),
            "current_period_start": None,
            "current_period_end": None,
            "market_data_access_token": None,  # Generated after activation
            "project_count": 0,
            "project_limit": get_project_limit(tier_id)
        })
        
        return {
            "checkout_url": checkout_session.url,
            "session_id": checkout_session.id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_project_limit(tier_id: str) -> int:
    """Get project limit based on tier"""
    limits = {
        "basic": 100,
        "professional": 1000,
        "enterprise": 0  # 0 = unlimited
    }
    return limits.get(tier_id, 100)
