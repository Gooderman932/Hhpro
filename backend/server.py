from fastapi import FastAPI, APIRouter, HTTPException, Request, Response, Depends
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone, timedelta
import httpx
from passlib.context import CryptContext
import jwt as pyjwt

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Configuration
JWT_SECRET = os.environ.get("JWT_SECRET", "hdrywall-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 168  # 7 days

# Stripe Configuration
STRIPE_API_KEY = os.environ.get("STRIPE_API_KEY")

# Create the main app
app = FastAPI(title="HDrywall Repair Platform API")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# ================== MODELS ==================

# Trade Codes Reference
TRADE_CODES = {
    "03": "Concrete",
    "04": "Masonry",
    "05": "Metals",
    "06": "Wood, Plastics, Composites",
    "07": "Thermal & Moisture Protection",
    "08": "Openings (Doors/Windows)",
    "09": "Finishes (Drywall/Paint)",
    "10": "Specialties",
    "22": "Plumbing",
    "23": "HVAC",
    "26": "Electrical",
    "31": "Earthwork",
    "32": "Exterior Improvements"
}

# Auth Models
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    name: str
    user_type: str  # "contractor" or "subcontractor"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    user_id: str
    email: str
    name: str
    user_type: str
    picture: Optional[str] = None
    created_at: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# Job Models
class JobCreate(BaseModel):
    title: str
    description: str
    trade_codes: List[str]
    location: str
    city: str
    state: str
    pay_rate: str
    pay_type: str  # "hourly", "daily", "project"
    duration: str
    certifications_required: List[str] = []
    experience_years: int = 0

class JobResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    job_id: str
    contractor_id: str
    contractor_name: str
    title: str
    description: str
    trade_codes: List[str]
    location: str
    city: str
    state: str
    pay_rate: str
    pay_type: str
    duration: str
    certifications_required: List[str]
    experience_years: int
    status: str
    created_at: str

# Worker Profile Models
class WorkerProfileCreate(BaseModel):
    headline: str
    bio: str
    trade_codes: List[str]
    skills: List[str]
    experience_years: int
    certifications: List[str] = []
    location: str
    city: str
    state: str
    availability: str  # "immediate", "1_week", "2_weeks", "flexible"
    hourly_rate_min: Optional[float] = None
    hourly_rate_max: Optional[float] = None

class WorkerProfileResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    profile_id: str
    user_id: str
    name: str
    headline: str
    bio: str
    trade_codes: List[str]
    skills: List[str]
    experience_years: int
    certifications: List[str]
    location: str
    city: str
    state: str
    availability: str
    hourly_rate_min: Optional[float]
    hourly_rate_max: Optional[float]
    status: str
    created_at: str

# Product Models
class ProductCreate(BaseModel):
    name: str
    description: str
    category: str
    price: float
    compare_price: Optional[float] = None
    image_url: str
    stock: int
    sku: str

class ProductResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    product_id: str
    name: str
    description: str
    category: str
    price: float
    compare_price: Optional[float]
    image_url: str
    stock: int
    sku: str
    active: bool
    created_at: str

# Cart Models
class CartItemAdd(BaseModel):
    product_id: str
    quantity: int = 1

class CartItemResponse(BaseModel):
    product_id: str
    name: str
    price: float
    quantity: int
    image_url: str

class CartResponse(BaseModel):
    items: List[CartItemResponse]
    subtotal: float
    item_count: int

# Market Data Tier Models
class TierResponse(BaseModel):
    tier_id: str
    name: str
    price: float
    billing_period: str
    features: List[str]
    description: str

# Checkout Models
class CheckoutRequest(BaseModel):
    origin_url: str

class CheckoutResponse(BaseModel):
    url: str
    session_id: str

# ================== HELPERS ==================

def create_token(user_id: str, email: str, user_type: str) -> str:
    payload = {
        "user_id": user_id,
        "email": email,
        "user_type": user_type,
        "exp": datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRATION_HOURS)
    }
    return pyjwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_token(token: str) -> Optional[Dict]:
    try:
        payload = pyjwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except pyjwt.ExpiredSignatureError:
        return None
    except pyjwt.InvalidTokenError:
        return None

async def get_current_user(request: Request) -> Optional[Dict]:
    # Check cookie first
    session_token = request.cookies.get("session_token")
    if session_token:
        session = await db.user_sessions.find_one({"session_token": session_token}, {"_id": 0})
        if session:
            expires_at = session.get("expires_at")
            if isinstance(expires_at, str):
                expires_at = datetime.fromisoformat(expires_at)
            if expires_at.tzinfo is None:
                expires_at = expires_at.replace(tzinfo=timezone.utc)
            if expires_at > datetime.now(timezone.utc):
                user = await db.users.find_one({"user_id": session["user_id"]}, {"_id": 0})
                return user
    
    # Check Authorization header
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        payload = verify_token(token)
        if payload:
            user = await db.users.find_one({"user_id": payload["user_id"]}, {"_id": 0})
            return user
    return None

async def require_user(request: Request) -> Dict:
    user = await get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user

async def require_contractor(request: Request) -> Dict:
    user = await require_user(request)
    if user.get("user_type") != "contractor":
        raise HTTPException(status_code=403, detail="Contractor access required")
    return user

async def require_subcontractor(request: Request) -> Dict:
    user = await require_user(request)
    if user.get("user_type") != "subcontractor":
        raise HTTPException(status_code=403, detail="Subcontractor access required")
    return user

# ================== AUTH ROUTES ==================

@api_router.post("/auth/register", response_model=TokenResponse)
async def register(data: UserRegister):
    # Check if user exists
    existing = await db.users.find_one({"email": data.email}, {"_id": 0})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_id = f"user_{uuid.uuid4().hex[:12]}"
    hashed_password = pwd_context.hash(data.password)
    
    user_doc = {
        "user_id": user_id,
        "email": data.email,
        "name": data.name,
        "user_type": data.user_type,
        "password_hash": hashed_password,
        "picture": None,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.users.insert_one(user_doc)
    
    token = create_token(user_id, data.email, data.user_type)
    user_response = UserResponse(
        user_id=user_id,
        email=data.email,
        name=data.name,
        user_type=data.user_type,
        picture=None,
        created_at=user_doc["created_at"]
    )
    return TokenResponse(access_token=token, user=user_response)

@api_router.post("/auth/login", response_model=TokenResponse)
async def login(data: UserLogin):
    user = await db.users.find_one({"email": data.email}, {"_id": 0})
    if not user or not pwd_context.verify(data.password, user.get("password_hash", "")):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_token(user["user_id"], user["email"], user["user_type"])
    user_response = UserResponse(
        user_id=user["user_id"],
        email=user["email"],
        name=user["name"],
        user_type=user["user_type"],
        picture=user.get("picture"),
        created_at=user["created_at"]
    )
    return TokenResponse(access_token=token, user=user_response)

@api_router.post("/auth/session")
async def process_google_session(request: Request, response: Response):
    """Process Emergent Google OAuth session"""
    body = await request.json()
    session_id = body.get("session_id")
    if not session_id:
        raise HTTPException(status_code=400, detail="session_id required")
    
    # Fetch user data from Emergent Auth
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://demobackend.emergentagent.com/auth/v1/env/oauth/session-data",
            headers={"X-Session-ID": session_id}
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid session")
        auth_data = resp.json()
    
    email = auth_data["email"]
    name = auth_data.get("name", email.split("@")[0])
    picture = auth_data.get("picture")
    session_token = auth_data.get("session_token")
    
    # Check if user exists
    user = await db.users.find_one({"email": email}, {"_id": 0})
    if user:
        # Update existing user
        await db.users.update_one(
            {"email": email},
            {"$set": {"name": name, "picture": picture}}
        )
        user_id = user["user_id"]
        user_type = user["user_type"]
    else:
        # Create new user (default to subcontractor, can change later)
        user_id = f"user_{uuid.uuid4().hex[:12]}"
        user_type = "subcontractor"
        user_doc = {
            "user_id": user_id,
            "email": email,
            "name": name,
            "user_type": user_type,
            "picture": picture,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        await db.users.insert_one(user_doc)
    
    # Store session
    expires_at = datetime.now(timezone.utc) + timedelta(days=7)
    await db.user_sessions.insert_one({
        "user_id": user_id,
        "session_token": session_token,
        "expires_at": expires_at.isoformat(),
        "created_at": datetime.now(timezone.utc).isoformat()
    })
    
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=True,
        samesite="none",
        path="/",
        max_age=7*24*60*60
    )
    
    user = await db.users.find_one({"user_id": user_id}, {"_id": 0})
    return {
        "user_id": user["user_id"],
        "email": user["email"],
        "name": user["name"],
        "user_type": user["user_type"],
        "picture": user.get("picture"),
        "created_at": user["created_at"]
    }

@api_router.get("/auth/me")
async def get_me(request: Request):
    user = await get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return {
        "user_id": user["user_id"],
        "email": user["email"],
        "name": user["name"],
        "user_type": user["user_type"],
        "picture": user.get("picture"),
        "created_at": user["created_at"]
    }

@api_router.post("/auth/logout")
async def logout(request: Request, response: Response):
    session_token = request.cookies.get("session_token")
    if session_token:
        await db.user_sessions.delete_one({"session_token": session_token})
    response.delete_cookie(key="session_token", path="/")
    return {"message": "Logged out"}

@api_router.put("/auth/update-type")
async def update_user_type(request: Request, body: dict):
    user = await require_user(request)
    new_type = body.get("user_type")
    if new_type not in ["contractor", "subcontractor"]:
        raise HTTPException(status_code=400, detail="Invalid user type")
    await db.users.update_one({"user_id": user["user_id"]}, {"$set": {"user_type": new_type}})
    return {"message": "User type updated", "user_type": new_type}

# ================== JOBS ROUTES ==================

@api_router.get("/trade-codes")
async def get_trade_codes():
    return TRADE_CODES

@api_router.post("/jobs", response_model=JobResponse, status_code=201)
async def create_job(data: JobCreate, request: Request):
    user = await require_contractor(request)
    
    job_id = f"job_{uuid.uuid4().hex[:12]}"
    job_doc = {
        "job_id": job_id,
        "contractor_id": user["user_id"],
        "contractor_name": user["name"],
        **data.model_dump(),
        "status": "active",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.jobs.insert_one(job_doc)
    job_doc.pop("_id", None)
    return JobResponse(**job_doc)

@api_router.get("/jobs", response_model=List[JobResponse])
async def list_jobs(
    trade_code: Optional[str] = None,
    state: Optional[str] = None,
    city: Optional[str] = None,
    status: str = "active"
):
    query = {"status": status}
    if trade_code:
        query["trade_codes"] = trade_code
    if state:
        query["state"] = {"$regex": state, "$options": "i"}
    if city:
        query["city"] = {"$regex": city, "$options": "i"}
    
    jobs = await db.jobs.find(query, {"_id": 0}).sort("created_at", -1).to_list(100)
    return [JobResponse(**job) for job in jobs]

@api_router.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job(job_id: str):
    job = await db.jobs.find_one({"job_id": job_id}, {"_id": 0})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobResponse(**job)

@api_router.get("/my-jobs", response_model=List[JobResponse])
async def get_my_jobs(request: Request):
    user = await require_contractor(request)
    jobs = await db.jobs.find({"contractor_id": user["user_id"]}, {"_id": 0}).sort("created_at", -1).to_list(100)
    return [JobResponse(**job) for job in jobs]

@api_router.put("/jobs/{job_id}")
async def update_job(job_id: str, data: JobCreate, request: Request):
    user = await require_contractor(request)
    job = await db.jobs.find_one({"job_id": job_id}, {"_id": 0})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job["contractor_id"] != user["user_id"]:
        raise HTTPException(status_code=403, detail="Not your job listing")
    
    await db.jobs.update_one({"job_id": job_id}, {"$set": data.model_dump()})
    return {"message": "Job updated"}

@api_router.delete("/jobs/{job_id}")
async def delete_job(job_id: str, request: Request):
    user = await require_contractor(request)
    job = await db.jobs.find_one({"job_id": job_id}, {"_id": 0})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job["contractor_id"] != user["user_id"]:
        raise HTTPException(status_code=403, detail="Not your job listing")
    
    await db.jobs.update_one({"job_id": job_id}, {"$set": {"status": "closed"}})
    return {"message": "Job closed"}

# ================== WORKER PROFILES ROUTES ==================

@api_router.post("/profiles", response_model=WorkerProfileResponse, status_code=201)
async def create_profile(data: WorkerProfileCreate, request: Request):
    user = await require_subcontractor(request)
    
    # Check if profile exists
    existing = await db.worker_profiles.find_one({"user_id": user["user_id"]}, {"_id": 0})
    if existing:
        raise HTTPException(status_code=400, detail="Profile already exists")
    
    profile_id = f"profile_{uuid.uuid4().hex[:12]}"
    profile_doc = {
        "profile_id": profile_id,
        "user_id": user["user_id"],
        "name": user["name"],
        **data.model_dump(),
        "status": "active",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.worker_profiles.insert_one(profile_doc)
    return WorkerProfileResponse(**profile_doc)

@api_router.get("/profiles", response_model=List[WorkerProfileResponse])
async def list_profiles(
    trade_code: Optional[str] = None,
    state: Optional[str] = None,
    city: Optional[str] = None,
    availability: Optional[str] = None,
    status: str = "active"
):
    query = {"status": status}
    if trade_code:
        query["trade_codes"] = trade_code
    if state:
        query["state"] = {"$regex": state, "$options": "i"}
    if city:
        query["city"] = {"$regex": city, "$options": "i"}
    if availability:
        query["availability"] = availability
    
    profiles = await db.worker_profiles.find(query, {"_id": 0}).sort("created_at", -1).to_list(100)
    return [WorkerProfileResponse(**p) for p in profiles]

@api_router.get("/profiles/{profile_id}", response_model=WorkerProfileResponse)
async def get_profile(profile_id: str):
    profile = await db.worker_profiles.find_one({"profile_id": profile_id}, {"_id": 0})
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return WorkerProfileResponse(**profile)

@api_router.get("/my-profile")
async def get_my_profile(request: Request):
    user = await require_subcontractor(request)
    profile = await db.worker_profiles.find_one({"user_id": user["user_id"]}, {"_id": 0})
    return profile

@api_router.put("/profiles")
async def update_profile(data: WorkerProfileCreate, request: Request):
    user = await require_subcontractor(request)
    await db.worker_profiles.update_one(
        {"user_id": user["user_id"]},
        {"$set": {**data.model_dump(), "name": user["name"]}}
    )
    return {"message": "Profile updated"}

# ================== PRODUCTS (E-COMMERCE) ROUTES ==================

@api_router.get("/products", response_model=List[ProductResponse])
async def list_products(category: Optional[str] = None, active: bool = True):
    query = {"active": active}
    if category:
        query["category"] = category
    products = await db.products.find(query, {"_id": 0}).sort("created_at", -1).to_list(100)
    return [ProductResponse(**p) for p in products]

@api_router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str):
    product = await db.products.find_one({"product_id": product_id}, {"_id": 0})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductResponse(**product)

@api_router.get("/product-categories")
async def get_product_categories():
    categories = await db.products.distinct("category")
    return categories

@api_router.post("/products", response_model=ProductResponse)
async def create_product(data: ProductCreate, request: Request):
    # Admin only - simplified for now
    product_id = f"prod_{uuid.uuid4().hex[:12]}"
    product_doc = {
        "product_id": product_id,
        **data.model_dump(),
        "active": True,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.products.insert_one(product_doc)
    return ProductResponse(**product_doc)

@api_router.put("/products/{product_id}")
async def update_product(product_id: str, data: ProductCreate, request: Request):
    await db.products.update_one({"product_id": product_id}, {"$set": data.model_dump()})
    return {"message": "Product updated"}

# ================== CART ROUTES ==================

@api_router.get("/cart", response_model=CartResponse)
async def get_cart(request: Request):
    user = await get_current_user(request)
    user_id = user["user_id"] if user else request.cookies.get("cart_id", str(uuid.uuid4()))
    
    cart = await db.carts.find_one({"user_id": user_id}, {"_id": 0})
    if not cart:
        return CartResponse(items=[], subtotal=0.0, item_count=0)
    
    # Batch fetch all products to avoid N+1 queries
    product_ids = [item["product_id"] for item in cart.get("items", [])]
    if not product_ids:
        return CartResponse(items=[], subtotal=0.0, item_count=0)
    
    products = await db.products.find({"product_id": {"$in": product_ids}}, {"_id": 0}).to_list(None)
    products_map = {p["product_id"]: p for p in products}
    
    items = []
    subtotal = 0.0
    for item in cart.get("items", []):
        product = products_map.get(item["product_id"])
        if product:
            items.append(CartItemResponse(
                product_id=item["product_id"],
                name=product["name"],
                price=product["price"],
                quantity=item["quantity"],
                image_url=product["image_url"]
            ))
            subtotal += product["price"] * item["quantity"]
    
    return CartResponse(items=items, subtotal=round(subtotal, 2), item_count=sum(i.quantity for i in items))

@api_router.post("/cart/add")
async def add_to_cart(data: CartItemAdd, request: Request, response: Response):
    user = await get_current_user(request)
    cart_id = request.cookies.get("cart_id")
    
    if user:
        user_id = user["user_id"]
    elif cart_id:
        user_id = cart_id
    else:
        user_id = str(uuid.uuid4())
        response.set_cookie(key="cart_id", value=user_id, max_age=30*24*60*60, path="/")
    
    cart = await db.carts.find_one({"user_id": user_id}, {"_id": 0})
    if not cart:
        cart = {"user_id": user_id, "items": []}
        await db.carts.insert_one(cart)
    
    # Check if item exists
    existing = next((i for i in cart["items"] if i["product_id"] == data.product_id), None)
    if existing:
        await db.carts.update_one(
            {"user_id": user_id, "items.product_id": data.product_id},
            {"$inc": {"items.$.quantity": data.quantity}}
        )
    else:
        await db.carts.update_one(
            {"user_id": user_id},
            {"$push": {"items": {"product_id": data.product_id, "quantity": data.quantity}}}
        )
    
    return {"message": "Added to cart"}

@api_router.post("/cart/update")
async def update_cart_item(data: CartItemAdd, request: Request):
    user = await get_current_user(request)
    cart_id = request.cookies.get("cart_id")
    user_id = user["user_id"] if user else cart_id
    
    if not user_id:
        raise HTTPException(status_code=400, detail="No cart found")
    
    if data.quantity <= 0:
        await db.carts.update_one(
            {"user_id": user_id},
            {"$pull": {"items": {"product_id": data.product_id}}}
        )
    else:
        await db.carts.update_one(
            {"user_id": user_id, "items.product_id": data.product_id},
            {"$set": {"items.$.quantity": data.quantity}}
        )
    return {"message": "Cart updated"}

@api_router.delete("/cart/{product_id}")
async def remove_from_cart(product_id: str, request: Request):
    user = await get_current_user(request)
    cart_id = request.cookies.get("cart_id")
    user_id = user["user_id"] if user else cart_id
    
    if not user_id:
        raise HTTPException(status_code=400, detail="No cart found")
    
    await db.carts.update_one(
        {"user_id": user_id},
        {"$pull": {"items": {"product_id": product_id}}}
    )
    return {"message": "Removed from cart"}

@api_router.delete("/cart")
async def clear_cart(request: Request):
    user = await get_current_user(request)
    cart_id = request.cookies.get("cart_id")
    user_id = user["user_id"] if user else cart_id
    
    if user_id:
        await db.carts.delete_one({"user_id": user_id})
    return {"message": "Cart cleared"}

# ================== CHECKOUT & PAYMENTS ==================

@api_router.post("/checkout/create-session")
async def create_checkout_session(data: CheckoutRequest, request: Request):
    from emergentintegrations.payments.stripe.checkout import StripeCheckout, CheckoutSessionRequest
    
    user = await get_current_user(request)
    cart_id = request.cookies.get("cart_id")
    user_id = user["user_id"] if user else cart_id
    
    if not user_id:
        raise HTTPException(status_code=400, detail="No cart found")
    
    cart = await db.carts.find_one({"user_id": user_id}, {"_id": 0})
    if not cart or not cart.get("items"):
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    # Calculate total
    total = 0.0
    for item in cart["items"]:
        product = await db.products.find_one({"product_id": item["product_id"]}, {"_id": 0})
        if product:
            total += product["price"] * item["quantity"]
    
    if total <= 0:
        raise HTTPException(status_code=400, detail="Invalid cart total")
    
    # Create Stripe session
    host_url = str(request.base_url).rstrip("/")
    webhook_url = f"{host_url}/api/webhook/stripe"
    
    stripe_checkout = StripeCheckout(api_key=STRIPE_API_KEY, webhook_url=webhook_url)
    
    success_url = f"{data.origin_url}/checkout/success?session_id={{CHECKOUT_SESSION_ID}}"
    cancel_url = f"{data.origin_url}/cart"
    
    checkout_request = CheckoutSessionRequest(
        amount=round(total, 2),
        currency="usd",
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={"user_id": user_id, "cart_total": str(total)}
    )
    
    session = await stripe_checkout.create_checkout_session(checkout_request)
    
    # Create payment transaction
    await db.payment_transactions.insert_one({
        "transaction_id": f"txn_{uuid.uuid4().hex[:12]}",
        "session_id": session.session_id,
        "user_id": user_id,
        "amount": total,
        "currency": "usd",
        "status": "pending",
        "payment_status": "initiated",
        "created_at": datetime.now(timezone.utc).isoformat()
    })
    
    return CheckoutResponse(url=session.url, session_id=session.session_id)

@api_router.get("/checkout/status/{session_id}")
async def get_checkout_status(session_id: str, request: Request):
    from emergentintegrations.payments.stripe.checkout import StripeCheckout
    
    host_url = str(request.base_url).rstrip("/")
    webhook_url = f"{host_url}/api/webhook/stripe"
    stripe_checkout = StripeCheckout(api_key=STRIPE_API_KEY, webhook_url=webhook_url)
    
    status = await stripe_checkout.get_checkout_status(session_id)
    
    # Update transaction
    await db.payment_transactions.update_one(
        {"session_id": session_id},
        {"$set": {"status": status.status, "payment_status": status.payment_status}}
    )
    
    # If paid, clear cart
    if status.payment_status == "paid":
        txn = await db.payment_transactions.find_one({"session_id": session_id}, {"_id": 0})
        if txn:
            await db.carts.delete_one({"user_id": txn["user_id"]})
            # Create order
            cart = await db.carts.find_one({"user_id": txn["user_id"]}, {"_id": 0})
            await db.orders.insert_one({
                "order_id": f"order_{uuid.uuid4().hex[:12]}",
                "user_id": txn["user_id"],
                "session_id": session_id,
                "amount": txn["amount"],
                "status": "paid",
                "created_at": datetime.now(timezone.utc).isoformat()
            })
    
    return {
        "status": status.status,
        "payment_status": status.payment_status,
        "amount_total": status.amount_total,
        "currency": status.currency
    }

@api_router.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    from emergentintegrations.payments.stripe.checkout import StripeCheckout
    
    body = await request.body()
    signature = request.headers.get("Stripe-Signature")
    
    host_url = str(request.base_url).rstrip("/")
    webhook_url = f"{host_url}/api/webhook/stripe"
    stripe_checkout = StripeCheckout(api_key=STRIPE_API_KEY, webhook_url=webhook_url)
    
    try:
        event = await stripe_checkout.handle_webhook(body, signature)
        if event.payment_status == "paid":
            await db.payment_transactions.update_one(
                {"session_id": event.session_id},
                {"$set": {"status": "complete", "payment_status": "paid"}}
            )
    except Exception as e:
        logging.error(f"Webhook error: {e}")
    
    return {"received": True}

# ================== MARKET DATA TIERS ==================

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
            "Email support"
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
            "Priority support"
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
            "API access",
            "Custom data integrations",
            "Predictive analytics",
            "Dedicated account manager",
            "White-label reports",
            "24/7 phone support"
        ]
    }
]

@api_router.get("/market-data/tiers", response_model=List[TierResponse])
async def get_market_data_tiers():
    return [TierResponse(**tier) for tier in MARKET_DATA_TIERS]

@api_router.post("/market-data/subscribe")
async def subscribe_to_tier(request: Request, body: dict):
    from emergentintegrations.payments.stripe.checkout import StripeCheckout, CheckoutSessionRequest
    
    tier_id = body.get("tier_id")
    origin_url = body.get("origin_url")
    
    tier = next((t for t in MARKET_DATA_TIERS if t["tier_id"] == tier_id), None)
    if not tier:
        raise HTTPException(status_code=404, detail="Tier not found")
    
    user = await get_current_user(request)
    user_id = user["user_id"] if user else f"guest_{uuid.uuid4().hex[:8]}"
    
    host_url = str(request.base_url).rstrip("/")
    webhook_url = f"{host_url}/api/webhook/stripe"
    stripe_checkout = StripeCheckout(api_key=STRIPE_API_KEY, webhook_url=webhook_url)
    
    success_url = f"{origin_url}/market-data/success?session_id={{CHECKOUT_SESSION_ID}}&tier={tier_id}"
    cancel_url = f"{origin_url}/market-data"
    
    checkout_request = CheckoutSessionRequest(
        amount=tier["price"],
        currency="usd",
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={"user_id": user_id, "tier_id": tier_id, "type": "market_data_subscription"}
    )
    
    session = await stripe_checkout.create_checkout_session(checkout_request)
    
    await db.payment_transactions.insert_one({
        "transaction_id": f"txn_{uuid.uuid4().hex[:12]}",
        "session_id": session.session_id,
        "user_id": user_id,
        "amount": tier["price"],
        "currency": "usd",
        "type": "market_data_subscription",
        "tier_id": tier_id,
        "status": "pending",
        "payment_status": "initiated",
        "created_at": datetime.now(timezone.utc).isoformat()
    })
    
    return {"url": session.url, "session_id": session.session_id}

# ================== HEALTH CHECK ==================

@api_router.get("/")
async def root():
    return {"message": "HDrywall Repair Platform API", "status": "running"}

@api_router.get("/health")
async def health():
    return {"status": "healthy"}

# Include the router
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
