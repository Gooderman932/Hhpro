"""
HHDrywall Pro API - Construction Intelligence Platform
Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.
"""
from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from passlib.context import CryptContext
from emergentintegrations.payments.stripe.checkout import StripeCheckout, CheckoutSessionRequest
import jwt
import uuid
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Import database and models
from app.database import engine, get_db, Base
from app.models.user import User, Tenant
from app.models.project import Project, ProjectParticipation
from app.models.company import Company
from app.models.prediction import Prediction, OpportunityScore
from app.models.subscription import Subscription, PaymentTransaction

# Import services
from app.services.prediction import PredictionService
from app.services.scoring import ScoringService

# Create all tables
Base.metadata.create_all(bind=engine)

# Configuration
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
ALGORITHM = os.environ.get('ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES', '30'))
STRIPE_API_KEY = os.environ.get('STRIPE_API_KEY', '')

# Parse CORS origins
cors_origins_str = os.environ.get('CORS_ORIGINS', '*')
CORS_ORIGINS = [origin.strip() for origin in cors_origins_str.split(',')]

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# FastAPI app
app = FastAPI(title="HHDrywall Pro API", version="2.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# Pydantic Models
# ============================================

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    username: EmailStr
    password: str

class UserResponse(BaseModel):
    user_id: str
    email: str
    full_name: Optional[str]
    role: str
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class SubscriptionCreate(BaseModel):
    tier_id: str
    origin_url: str

class CheckoutResponse(BaseModel):
    url: str
    session_id: str

class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None
    project_type: Optional[str] = "opportunity"
    sector: Optional[str] = None
    value: Optional[float] = None
    city: Optional[str] = None
    state: Optional[str] = None

# ============================================
# Auth Helpers
# ============================================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

# ============================================
# Subscription Helpers
# ============================================

MARKET_DATA_TIERS = [
    {
        "tier_id": "basic",
        "name": "Basic Analytics",
        "price": 299.00,
        "billing_period": "monthly",
        "description": "Essential market insights for growing contractors",
        "features": ["Regional trends", "Basic analytics", "Up to 100 projects", "Email support"]
    },
    {
        "tier_id": "professional",
        "name": "Professional Suite",
        "price": 799.00,
        "billing_period": "monthly",
        "description": "Comprehensive analytics for established contractors",
        "features": ["All Basic features", "Win probability predictions", "Demand forecasting", 
                     "Competitor analysis", "Up to 1,000 projects", "Priority support"]
    },
    {
        "tier_id": "enterprise",
        "name": "Enterprise Platform",
        "price": 1999.00,
        "billing_period": "monthly",
        "description": "Full-scale intelligence for large construction firms",
        "features": ["All Professional features", "Opportunity scoring", "API access",
                     "Custom predictions", "Unlimited projects", "Dedicated support"]
    }
]

TIER_PRICES = {"basic": 299.00, "professional": 799.00, "enterprise": 1999.00}

async def get_user_subscription(user: User, db: Session) -> Optional[Subscription]:
    """Get active subscription for user."""
    return db.query(Subscription).filter(
        Subscription.user_id == user.id,
        Subscription.status == "active",
        Subscription.expires_at > datetime.utcnow()
    ).first()

async def require_subscription(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Subscription:
    """Require active subscription."""
    subscription = await get_user_subscription(user, db)
    if not subscription:
        raise HTTPException(status_code=403, detail="Active subscription required")
    return subscription

async def require_professional_tier(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Subscription:
    """Require Professional or Enterprise tier."""
    subscription = await get_user_subscription(user, db)
    if not subscription:
        raise HTTPException(status_code=403, detail="Active subscription required")
    if subscription.tier_id not in ["professional", "enterprise"]:
        raise HTTPException(status_code=403, detail="Professional or Enterprise subscription required")
    return subscription

async def require_enterprise_tier(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Subscription:
    """Require Enterprise tier."""
    subscription = await get_user_subscription(user, db)
    if not subscription:
        raise HTTPException(status_code=403, detail="Active subscription required")
    if subscription.tier_id != "enterprise":
        raise HTTPException(status_code=403, detail="Enterprise subscription required")
    return subscription

# ============================================
# Auth Endpoints
# ============================================

@app.post("/api/auth/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create default tenant
    tenant = Tenant(name=f"{user_data.email}'s Organization")
    db.add(tenant)
    db.flush()
    
    # Create user
    user = User(
        user_id=str(uuid.uuid4()),
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=get_password_hash(user_data.password),
        tenant_id=tenant.id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return UserResponse(
        user_id=user.user_id,
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        created_at=user.created_at
    )

@app.post("/api/auth/token", response_model=Token)
async def login(form_data: UserLogin, db: Session = Depends(get_db)):
    """Login and get access token."""
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": user.email})
    return Token(access_token=access_token)

@app.get("/api/auth/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user info."""
    return UserResponse(
        user_id=current_user.user_id,
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role,
        created_at=current_user.created_at
    )

# ============================================
# Subscription Endpoints
# ============================================

@app.get("/api/pricing/tiers")
async def get_pricing_tiers():
    """Get available subscription tiers."""
    return MARKET_DATA_TIERS

@app.post("/api/subscriptions/checkout", response_model=CheckoutResponse)
async def create_checkout(
    request: Request,
    data: SubscriptionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create Stripe checkout session."""
    if data.tier_id not in TIER_PRICES:
        raise HTTPException(status_code=400, detail="Invalid tier")
    
    amount = TIER_PRICES[data.tier_id]
    tier_info = next((t for t in MARKET_DATA_TIERS if t["tier_id"] == data.tier_id), None)
    
    origin_url = data.origin_url.rstrip('/')
    success_url = f"{origin_url}/subscription/success?session_id={{CHECKOUT_SESSION_ID}}"
    cancel_url = f"{origin_url}/pricing"
    
    host_url = str(request.base_url).rstrip('/')
    stripe_checkout = StripeCheckout(api_key=STRIPE_API_KEY, webhook_url=f"{host_url}/api/webhook/stripe")
    
    checkout_request = CheckoutSessionRequest(
        amount=amount,
        currency="usd",
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={
            "user_id": str(current_user.id),
            "user_email": current_user.email,
            "tier_id": data.tier_id,
            "tier_name": tier_info["name"]
        }
    )
    
    session = await stripe_checkout.create_checkout_session(checkout_request)
    
    # Store pending transaction
    transaction = PaymentTransaction(
        transaction_id=str(uuid.uuid4()),
        session_id=session.session_id,
        user_id=current_user.id,
        user_email=current_user.email,
        tier_id=data.tier_id,
        tier_name=tier_info["name"],
        amount=amount
    )
    db.add(transaction)
    db.commit()
    
    return CheckoutResponse(url=session.url, session_id=session.session_id)

@app.get("/api/subscriptions/status/{session_id}")
async def get_payment_status(
    request: Request,
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Check payment status."""
    host_url = str(request.base_url).rstrip('/')
    stripe_checkout = StripeCheckout(api_key=STRIPE_API_KEY, webhook_url=f"{host_url}/api/webhook/stripe")
    
    checkout_status = await stripe_checkout.get_checkout_status(session_id)
    
    transaction = db.query(PaymentTransaction).filter(PaymentTransaction.session_id == session_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    if checkout_status.payment_status == "paid" and transaction.payment_status != "paid":
        transaction.payment_status = "paid"
        
        # Create subscription
        existing_sub = db.query(Subscription).filter(Subscription.session_id == session_id).first()
        if not existing_sub:
            subscription = Subscription(
                subscription_id=str(uuid.uuid4()),
                session_id=session_id,
                user_id=current_user.id,
                tier_id=transaction.tier_id,
                tier_name=transaction.tier_name,
                price=transaction.amount,
                expires_at=datetime.utcnow() + timedelta(days=30)
            )
            db.add(subscription)
        
        db.commit()
    
    return {
        "status": checkout_status.status,
        "payment_status": checkout_status.payment_status
    }

@app.get("/api/subscriptions/current")
async def get_current_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's current subscription."""
    subscription = await get_user_subscription(current_user, db)
    if not subscription:
        return None
    
    return {
        "subscription_id": subscription.subscription_id,
        "tier_id": subscription.tier_id,
        "tier_name": subscription.tier_name,
        "status": subscription.status,
        "price": subscription.price,
        "expires_at": subscription.expires_at.isoformat() if subscription.expires_at else None
    }

# ============================================
# Project Endpoints
# ============================================

@app.get("/api/projects")
async def list_projects(
    limit: int = 50,
    sector: Optional[str] = None,
    state: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    subscription: Subscription = Depends(require_subscription),
    db: Session = Depends(get_db)
):
    """List projects (subscription required)."""
    # Tier-based limits
    tier_limits = {"basic": 100, "professional": 1000, "enterprise": 10000}
    max_limit = tier_limits.get(subscription.tier_id, 100)
    limit = min(limit, max_limit)
    
    query = db.query(Project).filter(Project.tenant_id == current_user.tenant_id)
    if sector:
        query = query.filter(Project.sector == sector)
    if state:
        query = query.filter(Project.state == state)
    
    projects = query.limit(limit).all()
    
    return [
        {
            "id": p.id,
            "title": p.title,
            "project_type": p.project_type,
            "sector": p.sector,
            "value": p.value,
            "city": p.city,
            "state": p.state,
            "status": p.status,
            "created_at": p.created_at.isoformat() if p.created_at else None
        }
        for p in projects
    ]

@app.post("/api/projects")
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    subscription: Subscription = Depends(require_subscription),
    db: Session = Depends(get_db)
):
    """Create a new project."""
    project = Project(
        title=project_data.title,
        description=project_data.description,
        project_type=project_data.project_type,
        sector=project_data.sector,
        value=project_data.value,
        city=project_data.city,
        state=project_data.state,
        tenant_id=current_user.tenant_id
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    
    return {"id": project.id, "title": project.title, "message": "Project created"}

# ============================================
# Analytics Endpoints (Basic tier+)
# ============================================

@app.get("/api/analytics/summary")
async def get_analytics_summary(
    current_user: User = Depends(get_current_user),
    subscription: Subscription = Depends(require_subscription),
    db: Session = Depends(get_db)
):
    """Get analytics summary."""
    tenant_id = current_user.tenant_id
    
    # Get project stats
    total_projects = db.query(Project).filter(Project.tenant_id == tenant_id).count()
    total_value = db.query(func.sum(Project.value)).filter(Project.tenant_id == tenant_id).scalar() or 0
    
    # Sector distribution
    sector_counts = db.query(
        Project.sector, func.count(Project.id)
    ).filter(Project.tenant_id == tenant_id).group_by(Project.sector).all()
    
    sector_distribution = {s: c for s, c in sector_counts if s}
    
    summary = {
        "total_projects": total_projects,
        "total_value": total_value,
        "avg_project_value": total_value / total_projects if total_projects > 0 else 0,
        "sector_distribution": sector_distribution,
        "subscription_tier": subscription.tier_id,
        "data_as_of": datetime.utcnow().isoformat()
    }
    
    # Professional+ gets more data
    if subscription.tier_id in ["professional", "enterprise"]:
        summary["national_trends"] = {
            "year_over_year_growth": 8.3,
            "regional_hotspots": ["Texas", "Florida", "Arizona"],
            "emerging_sectors": ["Green Building", "Data Centers"]
        }
    
    return summary

@app.get("/api/analytics/regions")
async def get_regional_analysis(
    current_user: User = Depends(get_current_user),
    subscription: Subscription = Depends(require_subscription),
    db: Session = Depends(get_db)
):
    """Get regional analysis."""
    tenant_id = current_user.tenant_id
    
    # Get stats by state
    region_stats = db.query(
        Project.state,
        func.count(Project.id).label('count'),
        func.sum(Project.value).label('total_value')
    ).filter(
        Project.tenant_id == tenant_id,
        Project.state.isnot(None)
    ).group_by(Project.state).all()
    
    regions = [
        {
            "state": r.state,
            "project_count": r.count,
            "total_value": float(r.total_value or 0)
        }
        for r in region_stats
    ]
    
    return {"regions": regions, "subscription_tier": subscription.tier_id}

# ============================================
# ML Prediction Endpoints (Professional tier+)
# ============================================

@app.get("/api/predictions/win-probability/{project_id}")
async def predict_win_probability(
    project_id: int,
    current_user: User = Depends(get_current_user),
    subscription: Subscription = Depends(require_professional_tier),
    db: Session = Depends(get_db)
):
    """Get win probability prediction for a project."""
    service = PredictionService(db)
    try:
        result = service.predict_win_probability(project_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/api/predictions/demand-forecast")
async def get_demand_forecast(
    sector: str = "Commercial",
    region: str = "TX",
    months: int = 6,
    current_user: User = Depends(get_current_user),
    subscription: Subscription = Depends(require_professional_tier),
    db: Session = Depends(get_db)
):
    """Get demand forecast for sector/region."""
    service = PredictionService(db)
    return service.forecast_demand(sector, region, months)

@app.get("/api/predictions/regional-outlook")
async def get_regional_outlook(
    current_user: User = Depends(get_current_user),
    subscription: Subscription = Depends(require_professional_tier),
    db: Session = Depends(get_db)
):
    """Get regional demand outlook."""
    service = PredictionService(db)
    return service.get_regional_outlook()

# ============================================
# Opportunity Scoring Endpoints (Enterprise tier)
# ============================================

@app.get("/api/scoring/project/{project_id}")
async def score_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    subscription: Subscription = Depends(require_enterprise_tier),
    db: Session = Depends(get_db)
):
    """Score a project opportunity."""
    service = ScoringService(db)
    try:
        result = service.score_project(project_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/api/scoring/batch")
async def batch_score_projects(
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    subscription: Subscription = Depends(require_enterprise_tier),
    db: Session = Depends(get_db)
):
    """Score and rank multiple projects."""
    service = ScoringService(db)
    return service.batch_score_projects(current_user.tenant_id, limit)

# ============================================
# Competitor Intelligence (Professional tier+)
# ============================================

@app.get("/api/intelligence/competitors")
async def get_competitors(
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    subscription: Subscription = Depends(require_professional_tier),
    db: Session = Depends(get_db)
):
    """Get competitor intelligence."""
    companies = db.query(Company).filter(
        Company.tenant_id == current_user.tenant_id
    ).limit(limit).all()
    
    # If no companies, return sample data
    if not companies:
        return {
            "competitors": [
                {"name": "ABC Construction", "market_share": 12.5, "win_rate": 0.34},
                {"name": "BuildRight Inc", "market_share": 8.3, "win_rate": 0.28},
                {"name": "Premier Builders", "market_share": 6.7, "win_rate": 0.31}
            ],
            "subscription_tier": subscription.tier_id
        }
    
    return {
        "competitors": [
            {
                "id": c.id,
                "name": c.name,
                "company_type": c.company_type,
                "city": c.city,
                "state": c.state
            }
            for c in companies
        ],
        "subscription_tier": subscription.tier_id
    }

# ============================================
# Health Check
# ============================================

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "HHDrywall Pro API", "version": "2.0.0"}

@app.get("/")
async def root():
    return {"message": "HHDrywall Pro API", "version": "2.0.0", "docs": "/docs"}
