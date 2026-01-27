"""
Pydantic models for API request/response
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime


# ============================================
# User Models
# ============================================

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: str = "customer"


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: EmailStr
    password: str


class User(UserBase):
    user_id: str
    created_at: datetime
    is_active: bool = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ============================================
# Job Models
# ============================================

class JobBase(BaseModel):
    title: str
    description: str
    trade_codes: List[str] = []
    location: str
    budget: Optional[float] = None
    status: str = "open"


class JobCreate(JobBase):
    pass


class Job(JobBase):
    job_id: str
    customer_id: str
    created_at: datetime
    updated_at: datetime


# ============================================
# Worker Profile Models
# ============================================

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


# ============================================
# Product Models
# ============================================

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


# ============================================
# Order Models
# ============================================

class OrderBase(BaseModel):
    product_id: str
    quantity: int
    total_amount: float


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    order_id: str
    user_id: str
    status: str = "pending"
    created_at: datetime


# ============================================
# Payment Models
# ============================================

class PaymentTransaction(BaseModel):
    transaction_id: str
    order_id: str
    user_id: str
    amount: float
    status: str
    created_at: datetime


# ============================================
# Subscription Models
# ============================================

class SubscriptionCreate(BaseModel):
    tier_id: str
    origin_url: str


class SubscriptionResponse(BaseModel):
    subscription_id: str
    user_id: str
    tier_id: str
    tier_name: str
    status: str
    price: float
    created_at: datetime
    expires_at: Optional[datetime] = None


class CheckoutResponse(BaseModel):
    url: str
    session_id: str
