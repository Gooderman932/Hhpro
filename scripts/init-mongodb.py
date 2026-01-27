#!/usr/bin/env python3
"""
MongoDB Database Initialization Script for HDrywall Pro
Creates collections and adds sample data
"""

import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'backend'))

from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent.parent / 'backend' / '.env')

MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'test_database')

async def initialize_database():
    """Initialize MongoDB database with collections and indexes"""
    print("Connecting to MongoDB...")
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    print(f"Initializing database: {DB_NAME}")
    
    # Collections to create
    collections = [
        'users',
        'jobs',
        'worker_profiles',
        'products',
        'orders',
        'payment_transactions',
        'user_sessions',
        'subscriptions'
    ]
    
    # Create collections
    existing_collections = await db.list_collection_names()
    for collection in collections:
        if collection not in existing_collections:
            await db.create_collection(collection)
            print(f"✓ Created collection: {collection}")
        else:
            print(f"  Collection already exists: {collection}")
    
    # Create indexes
    print("\nCreating indexes...")
    
    # Users indexes
    await db.users.create_index("email", unique=True)
    await db.users.create_index("user_id")
    print("✓ Users indexes created")
    
    # Jobs indexes
    await db.jobs.create_index("trade_codes")
    await db.jobs.create_index("job_id")
    await db.jobs.create_index("customer_id")
    await db.jobs.create_index("status")
    print("✓ Jobs indexes created")
    
    # Worker profiles indexes
    await db.worker_profiles.create_index("profile_id")
    await db.worker_profiles.create_index("user_id")
    await db.worker_profiles.create_index("trade_codes")
    print("✓ Worker profiles indexes created")
    
    # Products indexes
    await db.products.create_index("category")
    await db.products.create_index("product_id")
    print("✓ Products indexes created")
    
    # Orders indexes
    await db.orders.create_index("order_id")
    await db.orders.create_index("user_id")
    print("✓ Orders indexes created")
    
    # Payment transactions indexes
    await db.payment_transactions.create_index("transaction_id")
    await db.payment_transactions.create_index("order_id")
    print("✓ Payment transactions indexes created")
    
    # User sessions indexes
    await db.user_sessions.create_index("session_id")
    await db.user_sessions.create_index("user_id")
    print("✓ User sessions indexes created")
    
    # Subscriptions indexes
    await db.subscriptions.create_index("subscription_id")
    await db.subscriptions.create_index("user_id")
    print("✓ Subscriptions indexes created")
    
    print("\n" + "="*50)
    print("Database initialization complete!")
    print("="*50)
    print(f"\nDatabase: {DB_NAME}")
    print(f"Collections: {len(collections)}")
    print("\nCollections created:")
    for collection in collections:
        count = await db[collection].count_documents({})
        print(f"  - {collection}: {count} documents")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(initialize_database())
