from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict
from datetime import datetime, timedelta
from passlib.context import CryptContext
from emergentintegrations.payments.stripe.checkout import StripeCheckout, CheckoutSessionRequest
import jwt
import os
import uuid
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Configuration
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'construction_intel_db')
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
ALGORITHM = os.environ.get('ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES', '30'))

# Parse CORS origins from comma-separated string
cors_origins_str = os.environ.get('CORS_ORIGINS', 'http://localhost:3000')
CORS_ORIGINS = [origin.strip() for origin in cors_origins_str.split(',')]

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

# MongoDB connection
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security
security = HTTPBearer()

# FastAPI app
app = FastAPI(title="HDrywall Pro API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# Models
# ============================================

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: str = "customer"  # customer, worker, admin

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: EmailStr  # Using username for OAuth2 compatibility
    password: str

class User(UserBase):
    user_id: str
    created_at: datetime
    is_active: bool = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class JobBase(BaseModel):
    title: str
    description: str
    trade_codes: List[str] = []  # e.g., ["drywall", "painting"]
    location: str
    budget: Optional[float] = None
    status: str = "open"  # open, in_progress, completed, closed

class JobCreate(JobBase):
    pass

class Job(JobBase):
    job_id: str
    customer_id: str
    created_at: datetime
    updated_at: datetime

class WorkerProfileBase(BaseModel):
    trade_codes: List[str]
    hourly_rate: float
    years_experience: int
    bio: Optional[str] = None
    location: str

class WorkerProfileCreate(WorkerProfileBase):
    pass

class WorkerProfile(WorkerProfileBase):
    profile_id: str
    user_id: str
    rating: float = 0.0
    is_active: bool = True
    created_at: datetime

class ProductBase(BaseModel):
    name: str
    description: str
    category: str
    price: float
    stock: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    product_id: str
    created_at: datetime

class OrderBase(BaseModel):
    product_id: str
    quantity: int
    total_amount: float

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    order_id: str
    user_id: str
    status: str = "pending"  # pending, paid, shipped, delivered
    created_at: datetime

class PaymentTransaction(BaseModel):
    transaction_id: str
    order_id: str
    user_id: str
    amount: float
    status: str  # pending, completed, failed
    created_at: datetime

# ============================================
# Helper Functions
# ============================================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    user = await db.users.find_one({"email": email})
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    return User(
        user_id=user["user_id"],
        email=user["email"],
        full_name=user.get("full_name"),
        role=user.get("role", "customer"),
        created_at=user["created_at"],
        is_active=user.get("is_active", True)
    )

# ============================================
# Database Initialization
# ============================================

@app.on_event("startup")
async def startup_db():
    """Create indexes on startup"""
    # Users collection indexes
    await db.users.create_index("email", unique=True)
    await db.users.create_index("user_id")
    
    # Jobs collection indexes
    await db.jobs.create_index("trade_codes")
    await db.jobs.create_index("job_id")
    await db.jobs.create_index("customer_id")
    
    # Worker profiles indexes
    await db.worker_profiles.create_index("profile_id")
    await db.worker_profiles.create_index("user_id")
    
    # Products collection indexes
    await db.products.create_index("category")
    await db.products.create_index("product_id")
    
    # Orders indexes
    await db.orders.create_index("order_id")
    await db.orders.create_index("user_id")
    
    # Payment transactions indexes
    await db.payment_transactions.create_index("transaction_id")
    await db.payment_transactions.create_index("order_id")
    
    print("Database indexes created")

# ============================================
# Authentication Endpoints
# ============================================

@app.post("/api/auth/register", response_model=User)
async def register(user_data: UserCreate):
    # Check if user exists
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    user_id = str(uuid.uuid4())
    user_doc = {
        "user_id": user_id,
        "email": user_data.email,
        "full_name": user_data.full_name,
        "role": user_data.role,
        "hashed_password": get_password_hash(user_data.password),
        "created_at": datetime.utcnow(),
        "is_active": True
    }
    
    await db.users.insert_one(user_doc)
    
    return User(
        user_id=user_id,
        email=user_data.email,
        full_name=user_data.full_name,
        role=user_data.role,
        created_at=user_doc["created_at"],
        is_active=True
    )

@app.post("/api/auth/token", response_model=Token)
async def login(form_data: UserLogin):
    user = await db.users.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": user["email"]})
    return Token(access_token=access_token)

@app.get("/api/auth/me", response_model=User)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

# ============================================
# Jobs Endpoints
# ============================================

@app.get("/api/jobs", response_model=List[Job])
async def list_jobs(
    trade_code: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 50,
    current_user: User = Depends(get_current_user)
):
    query = {}
    if trade_code:
        query["trade_codes"] = trade_code
    if status:
        query["status"] = status
    
    # Projection to fetch only required fields for better performance
    projection = {
        "job_id": 1,
        "title": 1,
        "description": 1,
        "trade_codes": 1,
        "location": 1,
        "budget": 1,
        "status": 1,
        "customer_id": 1,
        "created_at": 1,
        "updated_at": 1,
        "_id": 0,
    }
    jobs_cursor = db.jobs.find(query, projection).limit(limit)
    jobs = await jobs_cursor.to_list(length=limit)
    
    return [
        Job(
            job_id=job["job_id"],
            title=job["title"],
            description=job["description"],
            trade_codes=job["trade_codes"],
            location=job["location"],
            budget=job.get("budget"),
            status=job["status"],
            customer_id=job["customer_id"],
            created_at=job["created_at"],
            updated_at=job["updated_at"]
        )
        for job in jobs
    ]

@app.post("/api/jobs", response_model=Job)
async def create_job(job_data: JobCreate, current_user: User = Depends(get_current_user)):
    job_id = str(uuid.uuid4())
    now = datetime.utcnow()
    
    job_doc = {
        "job_id": job_id,
        "customer_id": current_user.user_id,
        "title": job_data.title,
        "description": job_data.description,
        "trade_codes": job_data.trade_codes,
        "location": job_data.location,
        "budget": job_data.budget,
        "status": job_data.status,
        "created_at": now,
        "updated_at": now
    }
    
    await db.jobs.insert_one(job_doc)
    
    return Job(**job_doc)

@app.put("/api/jobs/{job_id}", response_model=Job)
async def update_job(
    job_id: str,
    job_data: JobCreate,
    current_user: User = Depends(get_current_user)
):
    job = await db.jobs.find_one({"job_id": job_id})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job["customer_id"] != current_user.user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    update_data = {
        "title": job_data.title,
        "description": job_data.description,
        "trade_codes": job_data.trade_codes,
        "location": job_data.location,
        "budget": job_data.budget,
        "status": job_data.status,
        "updated_at": datetime.utcnow()
    }
    
    await db.jobs.update_one({"job_id": job_id}, {"$set": update_data})
    
    updated_job = await db.jobs.find_one({"job_id": job_id})
    return Job(**updated_job)

@app.delete("/api/jobs/{job_id}")
async def close_job(job_id: str, current_user: User = Depends(get_current_user)):
    job = await db.jobs.find_one({"job_id": job_id})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job["customer_id"] != current_user.user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    await db.jobs.update_one(
        {"job_id": job_id},
        {"$set": {"status": "closed", "updated_at": datetime.utcnow()}}
    )
    
    return {"message": "Job closed successfully"}

# ============================================
# Worker Profiles Endpoints
# ============================================

@app.get("/api/workers", response_model=List[WorkerProfile])
async def list_workers(
    trade_code: Optional[str] = None,
    limit: int = 50,
    current_user: User = Depends(get_current_user)
):
    query = {"is_active": True}
    if trade_code:
        query["trade_codes"] = trade_code
    
    # Projection to fetch only required fields for better performance
    projection = {
        "profile_id": 1,
        "user_id": 1,
        "trade_codes": 1,
        "hourly_rate": 1,
        "years_experience": 1,
        "bio": 1,
        "location": 1,
        "rating": 1,
        "is_active": 1,
        "created_at": 1,
        "_id": 0,
    }
    workers_cursor = db.worker_profiles.find(query, projection).limit(limit)
    workers = await workers_cursor.to_list(length=limit)
    
    return [
        WorkerProfile(
            profile_id=worker["profile_id"],
            user_id=worker["user_id"],
            trade_codes=worker["trade_codes"],
            hourly_rate=worker["hourly_rate"],
            years_experience=worker["years_experience"],
            bio=worker.get("bio"),
            location=worker["location"],
            rating=worker.get("rating", 0.0),
            is_active=worker["is_active"],
            created_at=worker["created_at"]
        )
        for worker in workers
    ]

@app.post("/api/workers", response_model=WorkerProfile)
async def create_worker_profile(
    profile_data: WorkerProfileCreate,
    current_user: User = Depends(get_current_user)
):
    # Check if profile already exists for user
    existing_profile = await db.worker_profiles.find_one({"user_id": current_user.user_id})
    if existing_profile:
        raise HTTPException(status_code=400, detail="Worker profile already exists")
    
    profile_id = str(uuid.uuid4())
    profile_doc = {
        "profile_id": profile_id,
        "user_id": current_user.user_id,
        "trade_codes": profile_data.trade_codes,
        "hourly_rate": profile_data.hourly_rate,
        "years_experience": profile_data.years_experience,
        "bio": profile_data.bio,
        "location": profile_data.location,
        "rating": 0.0,
        "is_active": True,
        "created_at": datetime.utcnow()
    }
    
    await db.worker_profiles.insert_one(profile_doc)
    
    return WorkerProfile(**profile_doc)

@app.put("/api/workers/{profile_id}", response_model=WorkerProfile)
async def update_worker_profile(
    profile_id: str,
    profile_data: WorkerProfileCreate,
    current_user: User = Depends(get_current_user)
):
    profile = await db.worker_profiles.find_one({"profile_id": profile_id})
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    if profile["user_id"] != current_user.user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    update_data = {
        "trade_codes": profile_data.trade_codes,
        "hourly_rate": profile_data.hourly_rate,
        "years_experience": profile_data.years_experience,
        "bio": profile_data.bio,
        "location": profile_data.location
    }
    
    await db.worker_profiles.update_one({"profile_id": profile_id}, {"$set": update_data})
    
    updated_profile = await db.worker_profiles.find_one({"profile_id": profile_id})
    return WorkerProfile(**updated_profile)

@app.delete("/api/workers/{profile_id}")
async def deactivate_worker_profile(
    profile_id: str,
    current_user: User = Depends(get_current_user)
):
    profile = await db.worker_profiles.find_one({"profile_id": profile_id})
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    if profile["user_id"] != current_user.user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    await db.worker_profiles.update_one(
        {"profile_id": profile_id},
        {"$set": {"is_active": False}}
    )
    
    return {"message": "Worker profile deactivated"}

# ============================================
# Products Endpoints (Shop)
# ============================================

@app.get("/api/products", response_model=List[Product])
async def list_products(
    category: Optional[str] = None,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
):
    query = {}
    if category:
        query["category"] = category
    
    # Projection to fetch only required fields for better performance
    projection = {
        "product_id": 1,
        "name": 1,
        "description": 1,
        "category": 1,
        "price": 1,
        "stock": 1,
        "created_at": 1,
        "_id": 0,
    }
    products_cursor = db.products.find(query, projection).limit(limit)
    products = await products_cursor.to_list(length=limit)
    
    return [
        Product(
            product_id=product["product_id"],
            name=product["name"],
            description=product["description"],
            category=product["category"],
            price=product["price"],
            stock=product["stock"],
            created_at=product["created_at"]
        )
        for product in products
    ]

@app.post("/api/products", response_model=Product)
async def create_product(
    product_data: ProductCreate,
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    product_id = str(uuid.uuid4())
    product_doc = {
        "product_id": product_id,
        "name": product_data.name,
        "description": product_data.description,
        "category": product_data.category,
        "price": product_data.price,
        "stock": product_data.stock,
        "created_at": datetime.utcnow()
    }
    
    await db.products.insert_one(product_doc)
    
    return Product(**product_doc)

@app.put("/api/products/{product_id}/stock")
async def update_stock(
    product_id: str,
    quantity: int,
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    product = await db.products.find_one({"product_id": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    new_stock = product["stock"] + quantity
    if new_stock < 0:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    
    await db.products.update_one(
        {"product_id": product_id},
        {"$set": {"stock": new_stock}}
    )
    
    return {"message": "Stock updated", "new_stock": new_stock}

# ============================================
# Orders Endpoints
# ============================================

@app.get("/api/orders", response_model=List[Order])
async def list_orders(
    limit: int = 50,
    current_user: User = Depends(get_current_user)
):
    query = {"user_id": current_user.user_id}
    if current_user.role == "admin":
        query = {}  # Admin sees all orders
    
    # Projection to fetch only required fields for better performance
    projection = {
        "order_id": 1,
        "user_id": 1,
        "product_id": 1,
        "quantity": 1,
        "total_amount": 1,
        "status": 1,
        "created_at": 1,
        "_id": 0,
    }
    orders_cursor = db.orders.find(query, projection).limit(limit)
    orders = await orders_cursor.to_list(length=limit)
    
    return [
        Order(
            order_id=order["order_id"],
            user_id=order["user_id"],
            product_id=order["product_id"],
            quantity=order["quantity"],
            total_amount=order["total_amount"],
            status=order["status"],
            created_at=order["created_at"]
        )
        for order in orders
    ]

@app.post("/api/orders", response_model=Order)
async def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_user)
):
    # Verify product exists and has stock
    product = await db.products.find_one({"product_id": order_data.product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product["stock"] < order_data.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    
    order_id = str(uuid.uuid4())
    order_doc = {
        "order_id": order_id,
        "user_id": current_user.user_id,
        "product_id": order_data.product_id,
        "quantity": order_data.quantity,
        "total_amount": order_data.total_amount,
        "status": "pending",
        "created_at": datetime.utcnow()
    }
    
    await db.orders.insert_one(order_doc)
    
    # Decrease product stock
    await db.products.update_one(
        {"product_id": order_data.product_id},
        {"$inc": {"stock": -order_data.quantity}}
    )
    
    return Order(**order_doc)

# ============================================
# Payment Transactions Endpoints
# ============================================

@app.post("/api/payments")
async def create_payment(
    order_id: str,
    current_user: User = Depends(get_current_user)
):
    # Verify order exists and belongs to user
    order = await db.orders.find_one({"order_id": order_id})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order["user_id"] != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    if order["status"] == "paid":
        raise HTTPException(status_code=400, detail="Order already paid")
    
    # Create payment transaction
    transaction_id = str(uuid.uuid4())
    transaction_doc = {
        "transaction_id": transaction_id,
        "order_id": order_id,
        "user_id": current_user.user_id,
        "amount": order["total_amount"],
        "status": "completed",  # In real app, integrate with payment processor
        "created_at": datetime.utcnow()
    }
    
    await db.payment_transactions.insert_one(transaction_doc)
    
    # Update order status
    await db.orders.update_one(
        {"order_id": order_id},
        {"$set": {"status": "paid"}}
    )
    
    return PaymentTransaction(**transaction_doc)

# ============================================
# Health Check
# ============================================

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "HDrywall Pro API"}

@app.get("/")
async def root():
    return {
        "message": "HDrywall Pro API",
        "version": "1.0.0",
        "docs": "/docs"
    }

# ============================================
# Pricing Tiers Endpoint
# ============================================

@app.get("/api/pricing/tiers")
async def get_pricing_tiers():
    """Get available subscription tiers"""
    return MARKET_DATA_TIERS