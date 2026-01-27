"""
HDrywall Pro API - Main Server
Construction Intelligence Platform
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pathlib import Path
import os

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Import database and routers
from db.mongo import init_indexes
from routes import auth, jobs, workers, products, orders, payments, market_data

# Parse CORS origins from comma-separated string
cors_origins_str = os.environ.get('CORS_ORIGINS', 'http://localhost:3000')
CORS_ORIGINS = [origin.strip() for origin in cors_origins_str.split(',')]

# FastAPI app
app = FastAPI(title="HDrywall Pro API", version="2.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(jobs.router)
app.include_router(workers.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(payments.router)
app.include_router(market_data.router)


@app.on_event("startup")
async def startup_db():
    """Initialize database indexes on startup"""
    await init_indexes()


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "HDrywall Pro API"}


@app.get("/")
async def root():
    return {
        "message": "HDrywall Pro API",
        "version": "2.0.0",
        "docs": "/docs"
    }
