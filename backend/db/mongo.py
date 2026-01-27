"""
Database configuration and MongoDB client
"""
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'construction_intel_db')

# MongoDB connection
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]


async def init_indexes():
    """Create database indexes on startup"""
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
    await db.payment_transactions.create_index("session_id")
    
    # Subscriptions indexes
    await db.subscriptions.create_index("subscription_id")
    await db.subscriptions.create_index("user_id")
    await db.subscriptions.create_index("session_id", unique=True)
    
    print("Database indexes created")
