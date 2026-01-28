"""
HDrywall Pro Platform - Backend Server
FastAPI backend with MongoDB, Stripe integration, and Market Data subscriptions

Copyright © 2025 HDrywall Repair / Poor Dude Holdings LLC
"""

import os
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Optional, List

import httpx
import stripe
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, EmailStr

# ============================================================================
# APPLICATION SETUP
# ============================================================================

app = FastAPI(
    title="HDrywall Pro Platform API",
    description="Professional contractor/subcontractor job matching with e-commerce",
    version="2.0.0"
)

# CORS Configuration
CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB Connection
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.environ.get("DB_NAME", "test_database")
mongo_client = AsyncIOMotorClient(MONGO_URL)
db = mongo_client[DB_NAME]

# Stripe Configuration
stripe.api_key = os.environ.get("STRIPE_API_KEY", "sk_test_emergent")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")

# Market Data Integration
MARKET_DATA_API_URL = os.environ.get("MARKET_DATA_API_URL", "http://localhost:8000")
MARKET_DATA_API_KEY = os.environ.get("MARKET_DATA_API_KEY", "")

# JWT Configuration
JWT_SECRET = os.environ.get("JWT_SECRET", "your-secret-key-change-this")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# ============================================================================
# MARKET DATA TIERS CONFIGURATION
# ============================================================================

MARKET_DATA_TIERS = [
    {
        "tier_id": "basic",
        "name": "Basic Analytics",
        "price": 299.00,
        "billing_period": "monthly",
        "description": "Essential market insights for growing businesses",
        "features": [
            "Regional labor market trends",
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
            "National market data",
            "Real-time wage tracking",
            "Competitor analysis",
            "Custom report generation",
            "Priority support",
            "Up to 1,000 projects"
        ],
        "popular": True
    },
    {
        "tier_id": "enterprise",
        "name": "Enterprise Platform",
        "price": 1999.00,
        "billing_period": "monthly",
        "description": "Full-scale intelligence for large construction firms",
        "features": [
            "All Professional features",
            "API access",
            "Custom data integrations",
            "Predictive analytics",
            "Win probability models",
            "Demand forecasting",
            "Dedicated account manager",
            "White-label reports",
            "24/7 phone support",
            "Unlimited projects"
        ]
    }
]

# Subscription status types
SUBSCRIPTION_STATUS = {
    "active": "Active subscription with full access",
    "expired": "Subscription period ended",
    "cancelled": "User cancelled subscription",
    "pending": "Payment processing",
    "failed": "Payment failed"
}

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    user_type: str  # "contractor" or "subcontractor"
    company: Optional[str] = None
    phone: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class JobCreate(BaseModel):
    title: str
    description: str
    location: str
    trade_codes: List[str]
    budget: Optional[float] = None
    timeline: Optional[str] = None

class WorkerProfileCreate(BaseModel):
    trade_codes: List[str]
    experience_years: int
    hourly_rate: Optional[float] = None
    availability: str  # "immediate", "2-weeks", "1-month"
    bio: Optional[str] = None
    certifications: Optional[List[str]] = None

class SubscriptionCreate(BaseModel):
    tier_id: str

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token() -> str:
    """Generate secure random token"""
    return secrets.token_urlsafe(32)

async def require_user(request: Request) -> dict:
    """Require authenticated user from session"""
    session_token = request.cookies.get("session_token")
    
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    session = await db.user_sessions.find_one({"session_token": session_token})
    
    if not session:
        raise HTTPException(status_code=401, detail="Invalid session")
    
    # Check session expiry
    expires_at = datetime.fromisoformat(session["expires_at"])
    if datetime.utcnow() > expires_at:
        raise HTTPException(status_code=401, detail="Session expired")
    
    user = await db.users.find_one({"user_id": session["user_id"]}, {"_id": 0, "password_hash": 0})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

def get_project_limit(tier_id: str) -> int:
    """Get project limit based on tier"""
    limits = {
        "basic": 100,
        "professional": 1000,
        "enterprise": 0  # 0 = unlimited
    }
    return limits.get(tier_id, 100)

# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

@app.post("/api/v1/auth/register")
async def register(user_data: UserRegister):
    """Register a new user"""
    
    # Check if user exists
    existing = await db.users.find_one({"email": user_data.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Validate user type
    if user_data.user_type not in ["contractor", "subcontractor"]:
        raise HTTPException(status_code=400, detail="Invalid user type")
    
    # Create user
    user_id = "user_" + secrets.token_urlsafe(16)
    password_hash = hash_password(user_data.password)
    
    user = {
        "user_id": user_id,
        "email": user_data.email,
        "password_hash": password_hash,
        "first_name": user_data.first_name,
        "last_name": user_data.last_name,
        "user_type": user_data.user_type,
        "company": user_data.company,
        "phone": user_data.phone,
        "created_at": datetime.utcnow().isoformat()
    }
    
    await db.users.insert_one(user)
    
    return {"message": "User registered successfully", "user_id": user_id}

@app.post("/api/v1/auth/login")
async def login(credentials: UserLogin):
    """Login user and create session"""
    
    # Find user
    user = await db.users.find_one({"email": credentials.email})
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verify password
    password_hash = hash_password(credentials.password)
    if password_hash != user["password_hash"]:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create session
    session_token = generate_token()
    expires_at = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    session = {
        "session_id": "sess_" + secrets.token_urlsafe(16),
        "user_id": user["user_id"],
        "session_token": session_token,
        "created_at": datetime.utcnow().isoformat(),
        "expires_at": expires_at.isoformat()
    }
    
    await db.user_sessions.insert_one(session)
    
    response = JSONResponse({
        "message": "Login successful",
        "user_id": user["user_id"],
        "user_type": user["user_type"]
    })
    
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax"
    )
    
    return response

@app.post("/api/v1/auth/logout")
async def logout(request: Request):
    """Logout user and destroy session"""
    session_token = request.cookies.get("session_token")
    
    if session_token:
        await db.user_sessions.delete_one({"session_token": session_token})
    
    response = JSONResponse({"message": "Logged out successfully"})
    response.delete_cookie("session_token")
    
    return response

@app.get("/api/v1/auth/me")
async def get_current_user(request: Request):
    """Get current authenticated user"""
    user = await require_user(request)
    return {"user": user}

# ============================================================================
# JOB ENDPOINTS
# ============================================================================

@app.get("/api/v1/jobs")
async def list_jobs(
    trade_code: Optional[str] = None,
    location: Optional[str] = None,
    status: str = "active"
):
    """List all jobs with optional filters"""
    
    query = {"status": status}
    
    if trade_code:
        query["trade_codes"] = trade_code
    
    if location:
        query["location"] = {"$regex": location, "$options": "i"}
    
    jobs = await db.jobs.find(query, {"_id": 0}).to_list(100)
    
    return {"jobs": jobs, "count": len(jobs)}

@app.post("/api/v1/jobs")
async def create_job(job_data: JobCreate, request: Request):
    """Create a new job posting"""
    user = await require_user(request)
    
    if user["user_type"] != "contractor":
        raise HTTPException(status_code=403, detail="Only contractors can post jobs")
    
    job_id = "job_" + secrets.token_urlsafe(16)
    
    job = {
        "job_id": job_id,
        "title": job_data.title,
        "description": job_data.description,
        "location": job_data.location,
        "trade_codes": job_data.trade_codes,
        "budget": job_data.budget,
        "timeline": job_data.timeline,
        "status": "active",
        "created_by": user["user_id"],
        "created_at": datetime.utcnow().isoformat()
    }
    
    await db.jobs.insert_one(job)
    
    return {"message": "Job created successfully", "job_id": job_id, "job": job}

@app.get("/api/v1/jobs/{job_id}")
async def get_job(job_id: str):
    """Get job details"""
    job = await db.jobs.find_one({"job_id": job_id}, {"_id": 0})
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return {"job": job}

# ============================================================================
# WORKER PROFILE ENDPOINTS
# ============================================================================

@app.get("/api/v1/worker-profiles")
async def list_worker_profiles(
    trade_code: Optional[str] = None,
    availability: Optional[str] = None
):
    """List worker profiles with optional filters"""
    
    query = {"status": "active"}
    
    if trade_code:
        query["trade_codes"] = trade_code
    
    if availability:
        query["availability"] = availability
    
    profiles = await db.worker_profiles.find(query, {"_id": 0}).to_list(100)
    
    return {"profiles": profiles, "count": len(profiles)}

@app.post("/api/v1/worker-profiles")
async def create_worker_profile(profile_data: WorkerProfileCreate, request: Request):
    """Create worker profile"""
    user = await require_user(request)
    
    if user["user_type"] != "subcontractor":
        raise HTTPException(status_code=403, detail="Only subcontractors can create profiles")
    
    # Check if profile already exists
    existing = await db.worker_profiles.find_one({"user_id": user["user_id"]})
    if existing:
        raise HTTPException(status_code=400, detail="Profile already exists")
    
    profile_id = "profile_" + secrets.token_urlsafe(16)
    
    profile = {
        "profile_id": profile_id,
        "user_id": user["user_id"],
        "trade_codes": profile_data.trade_codes,
        "experience_years": profile_data.experience_years,
        "hourly_rate": profile_data.hourly_rate,
        "availability": profile_data.availability,
        "bio": profile_data.bio,
        "certifications": profile_data.certifications or [],
        "status": "active",
        "created_at": datetime.utcnow().isoformat()
    }
    
    await db.worker_profiles.insert_one(profile)
    
    return {"message": "Profile created successfully", "profile_id": profile_id, "profile": profile}

# ============================================================================
# PRODUCTS (E-COMMERCE) ENDPOINTS
# ============================================================================

@app.get("/api/v1/shop/products")
async def list_products(
    category: Optional[str] = None,
    active_only: bool = True
):
    """List products in shop"""
    
    query = {}
    
    if active_only:
        query["active"] = True
    
    if category:
        query["category"] = category
    
    products = await db.products.find(query, {"_id": 0}).to_list(100)
    
    return {"products": products, "count": len(products)}

@app.get("/api/v1/shop/products/{product_id}")
async def get_product(product_id: str):
    """Get product details"""
    product = await db.products.find_one({"product_id": product_id}, {"_id": 0})
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {"product": product}

@app.post("/api/v1/shop/checkout")
async def create_checkout_session(request: Request):
    """Create Stripe checkout session for products"""
    data = await request.json()
    user = await require_user(request)
    
    items = data.get("items", [])
    
    if not items:
        raise HTTPException(status_code=400, detail="No items in cart")
    
    # Create line items for Stripe
    line_items = []
    
    for item in items:
        product = await db.products.find_one({"product_id": item["product_id"]})
        
        if not product:
            continue
        
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'unit_amount': int(product["price"] * 100),
                'product_data': {
                    'name': product["name"],
                    'description': product.get("description", ""),
                    'images': [product["image_url"]] if product.get("image_url") else []
                },
            },
            'quantity': item.get("quantity", 1),
        })
    
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=f'{request.base_url}shop/success?session_id={{CHECKOUT_SESSION_ID}}',
            cancel_url=f'{request.base_url}shop',
            client_reference_id=user["user_id"],
            metadata={'user_id': user["user_id"]}
        )
        
        return {
            "checkout_url": checkout_session.url,
            "session_id": checkout_session.id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# MARKET DATA SUBSCRIPTION ENDPOINTS
# ============================================================================

@app.get("/api/v1/billing/tiers")
async def get_market_data_tiers():
    """Get available Market Data subscription tiers"""
    return {"tiers": MARKET_DATA_TIERS}

@app.post("/api/v1/subscriptions/subscribe")
async def create_subscription(subscription_data: SubscriptionCreate, request: Request):
    """Create a new Market Data subscription"""
    user = await require_user(request)
    
    tier_id = subscription_data.tier_id
    
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
    
    try:
        # Create Stripe Checkout Session
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

@app.get("/api/v1/subscriptions/current")
async def get_current_subscription(request: Request):
    """Get user's current subscription"""
    user = await require_user(request)
    
    subscription = await db.subscriptions.find_one(
        {"user_id": user["user_id"], "status": "active"},
        {"_id": 0}
    )
    
    if not subscription:
        return {"subscription": None}
    
    return {"subscription": subscription}

@app.post("/api/v1/subscriptions/cancel")
async def cancel_subscription(request: Request):
    """Cancel user's subscription"""
    user = await require_user(request)
    
    subscription = await db.subscriptions.find_one({
        "user_id": user["user_id"],
        "status": "active"
    })
    
    if not subscription:
        raise HTTPException(status_code=404, detail="No active subscription found")
    
    # Cancel in Stripe
    if subscription.get("stripe_subscription_id"):
        try:
            stripe.Subscription.delete(subscription["stripe_subscription_id"])
        except Exception as e:
            print(f"Error cancelling Stripe subscription: {e}")
    
    # Update local record
    await db.subscriptions.update_one(
        {"subscription_id": subscription["subscription_id"]},
        {
            "$set": {
                "status": "cancelled",
                "cancelled_at": datetime.utcnow().isoformat()
            }
        }
    )
    
    # Revoke access
    await revoke_market_data_access(user["user_id"])
    
    return {"message": "Subscription cancelled successfully"}

# ============================================================================
# STRIPE WEBHOOK HANDLER
# ============================================================================

@app.post("/api/stripe/webhook")
async def stripe_webhook(request: Request):
    """Handle Stripe webhooks for subscription events"""
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        await handle_checkout_success(session)
        
    elif event['type'] == 'customer.subscription.updated':
        subscription = event['data']['object']
        await handle_subscription_updated(subscription)
        
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        await handle_subscription_cancelled(subscription)
        
    elif event['type'] == 'invoice.payment_succeeded':
        invoice = event['data']['object']
        await handle_payment_succeeded(invoice)
        
    elif event['type'] == 'invoice.payment_failed':
        invoice = event['data']['object']
        await handle_payment_failed(invoice)
    
    return {"status": "success"}

async def handle_checkout_success(session):
    """Activate subscription after successful checkout"""
    metadata = session.get('metadata', {})
    user_id = metadata.get('user_id')
    tier_id = metadata.get('tier_id')
    stripe_subscription_id = session.get('subscription')
    
    if not user_id or not tier_id:
        print("Missing metadata in checkout session")
        return
    
    # Calculate subscription period
    now = datetime.utcnow()
    period_end = now + timedelta(days=30)
    
    # Generate Market Data access token
    access_token = secrets.token_urlsafe(32)
    
    # Update subscription to active
    result = await db.subscriptions.update_one(
        {
            "user_id": user_id,
            "tier_id": tier_id,
            "status": "pending"
        },
        {
            "$set": {
                "status": "active",
                "stripe_subscription_id": stripe_subscription_id,
                "current_period_start": now.isoformat(),
                "current_period_end": period_end.isoformat(),
                "market_data_access_token": access_token,
                "activated_at": now.isoformat()
            }
        }
    )
    
    # Create payment transaction record
    await db.payment_transactions.insert_one({
        "transaction_id": "txn_" + secrets.token_urlsafe(16),
        "user_id": user_id,
        "amount": session['amount_total'] / 100,  # Convert from cents
        "currency": session['currency'],
        "payment_status": "paid",
        "stripe_payment_intent": session.get('payment_intent'),
        "stripe_subscription_id": stripe_subscription_id,
        "description": f"Market Data Subscription - {metadata.get('tier_name')}",
        "created_at": now.isoformat()
    })
    
    # Provision access in Market Data platform
    await provision_market_data_access(user_id, tier_id, access_token)
    
    print(f"✅ Subscription activated for user {user_id}")

async def handle_subscription_updated(subscription):
    """Handle subscription updates"""
    stripe_subscription_id = subscription['id']
    
    # Update subscription period
    period_start = datetime.fromtimestamp(subscription['current_period_start'])
    period_end = datetime.fromtimestamp(subscription['current_period_end'])
    
    await db.subscriptions.update_one(
        {"stripe_subscription_id": stripe_subscription_id},
        {
            "$set": {
                "current_period_start": period_start.isoformat(),
                "current_period_end": period_end.isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
        }
    )

async def handle_subscription_cancelled(subscription):
    """Handle subscription cancellation"""
    stripe_subscription_id = subscription['id']
    
    await db.subscriptions.update_one(
        {"stripe_subscription_id": stripe_subscription_id},
        {
            "$set": {
                "status": "cancelled",
                "cancelled_at": datetime.utcnow().isoformat()
            }
        }
    )
    
    # Revoke access in Market Data platform
    sub = await db.subscriptions.find_one({"stripe_subscription_id": stripe_subscription_id})
    if sub:
        await revoke_market_data_access(sub["user_id"])

async def handle_payment_succeeded(invoice):
    """Handle successful recurring payment"""
    stripe_subscription_id = invoice['subscription']
    
    # Extend subscription period
    period_end = datetime.fromtimestamp(invoice['period_end'])
    
    await db.subscriptions.update_one(
        {"stripe_subscription_id": stripe_subscription_id},
        {
            "$set": {
                "status": "active",
                "current_period_end": period_end.isoformat(),
                "last_payment_at": datetime.utcnow().isoformat()
            }
        }
    )
    
    # Record payment
    sub = await db.subscriptions.find_one({"stripe_subscription_id": stripe_subscription_id})
    if sub:
        await db.payment_transactions.insert_one({
            "transaction_id": "txn_" + secrets.token_urlsafe(16),
            "user_id": sub["user_id"],
            "amount": invoice['amount_paid'] / 100,
            "currency": invoice['currency'],
            "payment_status": "paid",
            "stripe_invoice_id": invoice['id'],
            "stripe_subscription_id": stripe_subscription_id,
            "description": f"Market Data Subscription Renewal - {sub['tier_name']}",
            "created_at": datetime.utcnow().isoformat()
        })

async def handle_payment_failed(invoice):
    """Handle failed payment"""
    stripe_subscription_id = invoice['subscription']
    
    await db.subscriptions.update_one(
        {"stripe_subscription_id": stripe_subscription_id},
        {
            "$set": {
                "status": "failed",
                "payment_failed_at": datetime.utcnow().isoformat()
            }
        }
    )

# ============================================================================
# MARKET DATA ACCESS PROVISIONING
# ============================================================================

async def provision_market_data_access(user_id: str, tier_id: str, access_token: str):
    """Provision access in the Market Data platform"""
    
    # Get user details
    user = await db.users.find_one({"user_id": user_id})
    if not user:
        return
    
    # Get tier details
    tier = next((t for t in MARKET_DATA_TIERS if t["tier_id"] == tier_id), None)
    if not tier:
        return
    
    # Determine project limit
    project_limit = get_project_limit(tier_id)
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{MARKET_DATA_API_URL}/api/admin/provision-user",
                headers={
                    "Authorization": f"Bearer {MARKET_DATA_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "user_id": user_id,
                    "email": user["email"],
                    "tier_id": tier_id,
                    "tier_name": tier["name"],
                    "project_limit": project_limit,
                    "access_token": access_token,
                    "features": tier["features"]
                },
                timeout=10.0
            )
            
            if response.status_code == 200:
                print(f"✅ Provisioned Market Data access for user {user_id}")
            else:
                print(f"❌ Failed to provision access: {response.text}")
                
    except Exception as e:
        print(f"❌ Error provisioning access: {str(e)}")

async def revoke_market_data_access(user_id: str):
    """Revoke access in the Market Data platform"""
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{MARKET_DATA_API_URL}/api/admin/revoke-user",
                headers={
                    "Authorization": f"Bearer {MARKET_DATA_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={"user_id": user_id},
                timeout=10.0
            )
            
            if response.status_code == 200:
                print(f"✅ Revoked Market Data access for user {user_id}")
            else:
                print(f"❌ Failed to revoke access: {response.text}")
                
    except Exception as e:
        print(f"❌ Error revoking access: {str(e)}")

# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "database": "connected",
        "version": "2.0.0"
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "HDrywall Pro Platform API",
        "version": "2.0.0",
        "docs": "/docs"
    }

# ============================================================================
# STARTUP EVENT
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    print("🚀 HDrywall Pro Platform API starting...")
    print(f"📊 Database: {DB_NAME}")
    print(f"💳 Stripe Mode: {'Live' if stripe.api_key.startswith('sk_live') else 'Test'}")
    print(f"🔗 Market Data API: {MARKET_DATA_API_URL}")
    print("✅ Server ready!")

# ============================================================================
# SHUTDOWN EVENT
# ============================================================================

@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    mongo_client.close()
    print("👋 Server shutdown complete")
