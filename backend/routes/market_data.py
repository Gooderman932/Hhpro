"""
Market data and subscription routes (Stripe integration)
"""
from fastapi import APIRouter, HTTPException, Depends, Request
from typing import Optional
from datetime import datetime, timedelta
from emergentintegrations.payments.stripe.checkout import StripeCheckout, CheckoutSessionRequest
import uuid
import os

from db.mongo import db
from auth.deps import get_current_user
from models.schemas import User, SubscriptionCreate, SubscriptionResponse, CheckoutResponse

router = APIRouter(tags=["Market Data"])

# Stripe Configuration
STRIPE_API_KEY = os.environ.get('STRIPE_API_KEY', '')

# Market Data Pricing Tiers
MARKET_DATA_TIERS = [
    {
        "tier_id": "basic",
        "name": "Basic Analytics",
        "price": 299.00,
        "billing_period": "monthly",
        "description": "Essential market insights for growing contractors",
        "features": [
            "Regional labor and project trends",
            "Basic wage analytics",
            "Monthly industry reports",
            "Email support",
            "Up to 100 projects"
        ]
    },
    {
        "tier_id": "professional",
        "name": "Professional Suite",
        "price": 799.00,
        "billing_period": "monthly",
        "description": "Comprehensive analytics for established contractors",
        "features": [
            "All Basic features",
            "National market data coverage",
            "Real-time wage and demand tracking",
            "Competitor analysis and market share",
            "Custom report generation",
            "Priority support",
            "Up to 1,000 projects"
        ]
    },
    {
        "tier_id": "enterprise",
        "name": "Enterprise Platform",
        "price": 1999.00,
        "billing_period": "monthly",
        "description": "Full-scale intelligence for large construction firms",
        "features": [
            "All Professional features",
            "API access for custom integrations",
            "Custom data pipelines and ETL",
            "Predictive analytics and win probability models",
            "Demand forecasting by region and trade",
            "Dedicated account manager",
            "White-label branded reports",
            "24/7 phone support",
            "Unlimited projects"
        ]
    }
]

TIER_PRICES = {
    "basic": 299.00,
    "professional": 799.00,
    "enterprise": 1999.00
}


@router.get("/api/pricing/tiers")
async def get_pricing_tiers():
    """Get available subscription tiers"""
    return MARKET_DATA_TIERS


@router.post("/api/subscriptions/checkout", response_model=CheckoutResponse)
async def create_subscription_checkout(
    request: Request,
    data: SubscriptionCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a Stripe checkout session for a subscription tier"""
    if data.tier_id not in TIER_PRICES:
        raise HTTPException(status_code=400, detail="Invalid tier selected")
    
    amount = TIER_PRICES[data.tier_id]
    tier_info = next((t for t in MARKET_DATA_TIERS if t["tier_id"] == data.tier_id), None)
    
    if not tier_info:
        raise HTTPException(status_code=400, detail="Tier not found")
    
    origin_url = data.origin_url.rstrip('/')
    success_url = f"{origin_url}/subscription/success?session_id={{CHECKOUT_SESSION_ID}}"
    cancel_url = f"{origin_url}/pricing"
    
    host_url = str(request.base_url).rstrip('/')
    webhook_url = f"{host_url}/api/webhook/stripe"
    stripe_checkout = StripeCheckout(api_key=STRIPE_API_KEY, webhook_url=webhook_url)
    
    checkout_request = CheckoutSessionRequest(
        amount=amount,
        currency="usd",
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={
            "user_id": current_user.user_id,
            "user_email": current_user.email,
            "tier_id": data.tier_id,
            "tier_name": tier_info["name"],
            "subscription_type": "market_data"
        }
    )
    
    session = await stripe_checkout.create_checkout_session(checkout_request)
    
    transaction_doc = {
        "transaction_id": str(uuid.uuid4()),
        "session_id": session.session_id,
        "user_id": current_user.user_id,
        "user_email": current_user.email,
        "tier_id": data.tier_id,
        "tier_name": tier_info["name"],
        "amount": amount,
        "currency": "usd",
        "payment_status": "pending",
        "subscription_type": "market_data",
        "created_at": datetime.utcnow()
    }
    await db.payment_transactions.insert_one(transaction_doc)
    
    return CheckoutResponse(url=session.url, session_id=session.session_id)


@router.get("/api/subscriptions/status/{session_id}")
async def get_payment_status(request: Request, session_id: str, current_user: User = Depends(get_current_user)):
    """Check payment status and update subscription if paid"""
    host_url = str(request.base_url).rstrip('/')
    webhook_url = f"{host_url}/api/webhook/stripe"
    stripe_checkout = StripeCheckout(api_key=STRIPE_API_KEY, webhook_url=webhook_url)
    
    checkout_status = await stripe_checkout.get_checkout_status(session_id)
    
    transaction = await db.payment_transactions.find_one({"session_id": session_id})
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    if transaction.get("payment_status") == "paid":
        subscription = await db.subscriptions.find_one({"session_id": session_id})
        return {"status": checkout_status.status, "payment_status": "paid", "subscription": subscription}
    
    new_status = checkout_status.payment_status
    await db.payment_transactions.update_one(
        {"session_id": session_id},
        {"$set": {"payment_status": new_status, "updated_at": datetime.utcnow()}}
    )
    
    if checkout_status.payment_status == "paid":
        existing_sub = await db.subscriptions.find_one({"session_id": session_id})
        if not existing_sub:
            subscription_doc = {
                "subscription_id": str(uuid.uuid4()),
                "session_id": session_id,
                "user_id": transaction["user_id"],
                "user_email": transaction["user_email"],
                "tier_id": transaction["tier_id"],
                "tier_name": transaction["tier_name"],
                "status": "active",
                "price": transaction["amount"],
                "created_at": datetime.utcnow(),
                "expires_at": datetime.utcnow() + timedelta(days=30)
            }
            await db.subscriptions.insert_one(subscription_doc)
            return {"status": checkout_status.status, "payment_status": "paid", "subscription": subscription_doc}
    
    return {"status": checkout_status.status, "payment_status": new_status, "subscription": None}


@router.get("/api/subscriptions/current", response_model=Optional[SubscriptionResponse])
async def get_current_subscription(current_user: User = Depends(get_current_user)):
    """Get user's current active subscription"""
    subscription = await db.subscriptions.find_one({
        "user_id": current_user.user_id,
        "status": "active",
        "expires_at": {"$gt": datetime.utcnow()}
    })
    
    if not subscription:
        return None
    
    return SubscriptionResponse(
        subscription_id=subscription["subscription_id"],
        user_id=subscription["user_id"],
        tier_id=subscription["tier_id"],
        tier_name=subscription["tier_name"],
        status=subscription["status"],
        price=subscription["price"],
        created_at=subscription["created_at"],
        expires_at=subscription.get("expires_at")
    )


@router.post("/api/webhook/stripe")
async def stripe_webhook(request: Request):
    """Handle Stripe webhook events"""
    try:
        body = await request.body()
        signature = request.headers.get("Stripe-Signature", "")
        
        host_url = str(request.base_url).rstrip('/')
        webhook_url = f"{host_url}/api/webhook/stripe"
        stripe_checkout = StripeCheckout(api_key=STRIPE_API_KEY, webhook_url=webhook_url)
        
        webhook_response = await stripe_checkout.handle_webhook(body, signature)
        
        if webhook_response.payment_status == "paid":
            session_id = webhook_response.session_id
            
            await db.payment_transactions.update_one(
                {"session_id": session_id},
                {"$set": {"payment_status": "paid", "updated_at": datetime.utcnow()}}
            )
            
            existing_sub = await db.subscriptions.find_one({"session_id": session_id})
            if not existing_sub:
                transaction = await db.payment_transactions.find_one({"session_id": session_id})
                if transaction:
                    subscription_doc = {
                        "subscription_id": str(uuid.uuid4()),
                        "session_id": session_id,
                        "user_id": transaction["user_id"],
                        "user_email": transaction["user_email"],
                        "tier_id": transaction["tier_id"],
                        "tier_name": transaction["tier_name"],
                        "status": "active",
                        "price": transaction["amount"],
                        "created_at": datetime.utcnow(),
                        "expires_at": datetime.utcnow() + timedelta(days=30)
                    }
                    await db.subscriptions.insert_one(subscription_doc)
        
        return {"status": "received", "event_id": webhook_response.event_id}
    
    except Exception as e:
        print(f"Webhook error: {e}")
        return {"status": "error", "message": str(e)}
