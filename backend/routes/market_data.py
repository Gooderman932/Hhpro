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


# ============================================
# Subscription-Gated Market Data Endpoints
# ============================================

async def require_active_subscription(current_user: User = Depends(get_current_user)):
    """Dependency to check for active subscription"""
    subscription = await db.subscriptions.find_one({
        "user_id": current_user.user_id,
        "status": "active",
        "expires_at": {"$gt": datetime.utcnow()}
    })
    if not subscription:
        raise HTTPException(
            status_code=403,
            detail="Active subscription required. Please subscribe to access market data."
        )
    return subscription


@router.get("/api/analytics/summary")
async def get_analytics_summary(
    current_user: User = Depends(get_current_user),
    subscription: dict = Depends(require_active_subscription)
):
    """Get market analytics summary - requires active subscription"""
    tier_id = subscription.get("tier_id", "basic")
    
    # Base analytics available to all tiers
    summary = {
        "total_projects": 1247,
        "active_contractors": 892,
        "avg_project_value": 125000,
        "market_growth": 12.5,
        "sector_distribution": {
            "Residential": 45,
            "Commercial": 30,
            "Industrial": 15,
            "Infrastructure": 10
        },
        "subscription_tier": tier_id,
        "data_as_of": datetime.utcnow().isoformat()
    }
    
    # Professional and Enterprise get more data
    if tier_id in ["professional", "enterprise"]:
        summary["national_trends"] = {
            "year_over_year_growth": 8.3,
            "regional_hotspots": ["Texas", "Florida", "Arizona"],
            "emerging_sectors": ["Green Building", "Data Centers"]
        }
        summary["wage_analytics"] = {
            "avg_hourly_rate": 32.50,
            "rate_change_yoy": 4.2,
            "top_paying_trades": ["Electrical", "Plumbing", "HVAC"]
        }
    
    # Enterprise gets predictive analytics
    if tier_id == "enterprise":
        summary["predictive_insights"] = {
            "projected_growth_q1": 15.2,
            "demand_forecast": "High",
            "recommended_regions": ["Austin", "Phoenix", "Nashville"],
            "win_probability_model": "Available via API"
        }
    
    return summary


@router.get("/api/analytics/trends")
async def get_analytics_trends(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    subscription: dict = Depends(require_active_subscription)
):
    """Get market trends over time - requires active subscription"""
    import random
    
    tier_id = subscription.get("tier_id", "basic")
    
    # Generate trend data
    trends = []
    base_value = 100
    for i in range(days):
        date = datetime.utcnow() - timedelta(days=days - i)
        trends.append({
            "date": date.strftime("%Y-%m-%d"),
            "project_volume": base_value + random.randint(-10, 20),
            "avg_bid_value": 120000 + random.randint(-5000, 10000)
        })
        base_value += random.randint(-5, 10)
    
    response = {
        "period_days": days,
        "trends": trends,
        "subscription_tier": tier_id
    }
    
    # Professional+ gets competitor trends
    if tier_id in ["professional", "enterprise"]:
        response["competitor_activity"] = {
            "new_entrants": 12,
            "market_exits": 3,
            "consolidations": 2
        }
    
    return response


@router.get("/api/analytics/regions")
async def get_regional_analysis(
    current_user: User = Depends(get_current_user),
    subscription: dict = Depends(require_active_subscription)
):
    """Get regional market analysis - requires active subscription"""
    tier_id = subscription.get("tier_id", "basic")
    
    regions = [
        {"state": "Texas", "project_count": 245, "total_value": 28500000, "growth": 15.2},
        {"state": "Florida", "project_count": 198, "total_value": 22100000, "growth": 12.8},
        {"state": "California", "project_count": 312, "total_value": 45200000, "growth": 8.5},
        {"state": "Arizona", "project_count": 156, "total_value": 18900000, "growth": 18.3},
        {"state": "Georgia", "project_count": 134, "total_value": 15600000, "growth": 11.2}
    ]
    
    response = {
        "regions": regions,
        "subscription_tier": tier_id
    }
    
    # Professional+ gets detailed breakdown
    if tier_id in ["professional", "enterprise"]:
        response["detailed_breakdown"] = True
        for region in response["regions"]:
            region["top_sectors"] = ["Commercial", "Residential"]
            region["avg_project_size"] = region["total_value"] // region["project_count"]
    
    return response


@router.get("/api/intelligence/competitors")
async def get_competitors(
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    subscription: dict = Depends(require_active_subscription)
):
    """Get competitor intelligence - requires Professional or Enterprise subscription"""
    tier_id = subscription.get("tier_id", "basic")
    
    if tier_id == "basic":
        raise HTTPException(
            status_code=403,
            detail="Competitor intelligence requires Professional or Enterprise subscription."
        )
    
    competitors = [
        {"name": "ABC Construction", "market_share": 12.5, "win_rate": 0.34, "avg_bid": 145000, "region": "Southwest"},
        {"name": "BuildRight Inc", "market_share": 8.3, "win_rate": 0.28, "avg_bid": 132000, "region": "Southeast"},
        {"name": "Premier Builders", "market_share": 6.7, "win_rate": 0.31, "avg_bid": 158000, "region": "West"},
        {"name": "Construct Co", "market_share": 5.9, "win_rate": 0.25, "avg_bid": 128000, "region": "Midwest"},
        {"name": "Quality Build LLC", "market_share": 4.2, "win_rate": 0.29, "avg_bid": 115000, "region": "Northeast"}
    ]
    
    response = {
        "competitors": competitors[:limit],
        "total_tracked": len(competitors),
        "subscription_tier": tier_id
    }
    
    # Enterprise gets deeper insights
    if tier_id == "enterprise":
        response["advanced_metrics"] = True
        for comp in response["competitors"]:
            comp["trend"] = "growing"
            comp["threat_level"] = "medium"
            comp["recent_wins"] = 5
    
    return response


@router.get("/api/intelligence/market-share")
async def get_market_share(
    region: str = None,
    current_user: User = Depends(get_current_user),
    subscription: dict = Depends(require_active_subscription)
):
    """Get market share analysis - requires Professional or Enterprise subscription"""
    tier_id = subscription.get("tier_id", "basic")
    
    if tier_id == "basic":
        raise HTTPException(
            status_code=403,
            detail="Market share analysis requires Professional or Enterprise subscription."
        )
    
    market_data = {
        "total_market_size": 2500000000,
        "your_estimated_share": 2.3,
        "top_players": [
            {"name": "Major Corp", "share": 15.2},
            {"name": "BigBuild Inc", "share": 11.8},
            {"name": "National Contractors", "share": 9.4}
        ],
        "growth_opportunity": "High",
        "subscription_tier": tier_id
    }
    
    if region:
        market_data["region_filter"] = region
        market_data["regional_market_size"] = 450000000
    
    return market_data

