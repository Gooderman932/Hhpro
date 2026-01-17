import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime, timezone
import uuid

MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.environ.get("DB_NAME", "test_database")

SAMPLE_PRODUCTS = [
    {
        "product_id": f"prod_{uuid.uuid4().hex[:12]}",
        "name": "Professional Drywall Taping Knife Set",
        "description": "Complete 4-piece set including 6\", 8\", 10\", and 12\" knives. Stainless steel blades with comfortable rubber grips.",
        "category": "Drywall Tools",
        "price": 45.99,
        "compare_price": 59.99,
        "image_url": "https://images.unsplash.com/photo-1572981779307-38b8cabb2407?w=400",
        "stock": 50,
        "sku": "DWT-001",
        "active": True,
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "product_id": f"prod_{uuid.uuid4().hex[:12]}",
        "name": "Automatic Drywall Taper",
        "description": "Professional automatic taping tool. Saves time on large projects. Includes extra tape roll.",
        "category": "Drywall Tools",
        "price": 289.99,
        "compare_price": 349.99,
        "image_url": "https://images.unsplash.com/photo-1504148455328-c376907d081c?w=400",
        "stock": 15,
        "sku": "DWT-002",
        "active": True,
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "product_id": f"prod_{uuid.uuid4().hex[:12]}",
        "name": "Drywall Sanding Pole - 48\"",
        "description": "Extendable aluminum pole for ceiling and wall sanding. Lightweight yet durable.",
        "category": "Drywall Tools",
        "price": 34.99,
        "compare_price": None,
        "image_url": "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=400",
        "stock": 75,
        "sku": "DWT-003",
        "active": True,
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "product_id": f"prod_{uuid.uuid4().hex[:12]}",
        "name": "Premium Joint Compound - 5 Gallon",
        "description": "All-purpose ready-mixed joint compound. Low shrinkage, easy sanding formula.",
        "category": "Materials",
        "price": 28.99,
        "compare_price": None,
        "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400",
        "stock": 200,
        "sku": "MAT-001",
        "active": True,
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "product_id": f"prod_{uuid.uuid4().hex[:12]}",
        "name": "Mesh Drywall Tape - 300ft Roll",
        "description": "Self-adhesive fiberglass mesh tape. Prevents cracking, easy to apply.",
        "category": "Materials",
        "price": 12.99,
        "compare_price": 15.99,
        "image_url": "https://images.unsplash.com/photo-1628002580365-f3c0a322d577?w=400",
        "stock": 500,
        "sku": "MAT-002",
        "active": True,
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "product_id": f"prod_{uuid.uuid4().hex[:12]}",
        "name": "Cordless Drywall Screw Gun",
        "description": "20V lithium-ion powered. Variable speed, depth adjustment. Includes 2 batteries.",
        "category": "Power Tools",
        "price": 179.99,
        "compare_price": 229.99,
        "image_url": "https://images.unsplash.com/photo-1607731493668-bfd0fc28c3bc?w=400",
        "stock": 25,
        "sku": "PWR-001",
        "active": True,
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "product_id": f"prod_{uuid.uuid4().hex[:12]}",
        "name": "Random Orbital Sander",
        "description": "5\" disc, variable speed control. Dust collection bag included. Perfect for finishing.",
        "category": "Power Tools",
        "price": 89.99,
        "compare_price": 109.99,
        "image_url": "https://images.unsplash.com/photo-1504148455328-c376907d081c?w=400",
        "stock": 40,
        "sku": "PWR-002",
        "active": True,
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "product_id": f"prod_{uuid.uuid4().hex[:12]}",
        "name": "Professional Dust Mask - 10 Pack",
        "description": "N95 rated, adjustable nose piece. Comfortable fit for all-day wear.",
        "category": "Safety Gear",
        "price": 24.99,
        "compare_price": None,
        "image_url": "https://images.unsplash.com/photo-1584634731339-252c581abfc5?w=400",
        "stock": 1000,
        "sku": "SAF-001",
        "active": True,
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "product_id": f"prod_{uuid.uuid4().hex[:12]}",
        "name": "Safety Glasses - Clear",
        "description": "Impact-resistant polycarbonate lenses. Anti-fog coating. ANSI Z87.1 certified.",
        "category": "Safety Gear",
        "price": 8.99,
        "compare_price": None,
        "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400",
        "stock": 300,
        "sku": "SAF-002",
        "active": True,
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "product_id": f"prod_{uuid.uuid4().hex[:12]}",
        "name": "Utility Knife Blades - 100 Pack",
        "description": "Heavy-duty carbon steel blades. Fits standard utility knives.",
        "category": "Blades & Accessories",
        "price": 19.99,
        "compare_price": 24.99,
        "image_url": "https://images.unsplash.com/photo-1607731493668-bfd0fc28c3bc?w=400",
        "stock": 250,
        "sku": "BLD-001",
        "active": True,
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "product_id": f"prod_{uuid.uuid4().hex[:12]}",
        "name": "Sanding Discs Variety Pack",
        "description": "5\" hook and loop discs. 80, 120, 180, 220 grit. 50 discs total.",
        "category": "Blades & Accessories",
        "price": 29.99,
        "compare_price": None,
        "image_url": "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=400",
        "stock": 150,
        "sku": "BLD-002",
        "active": True,
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "product_id": f"prod_{uuid.uuid4().hex[:12]}",
        "name": "Tool Belt with Pouches",
        "description": "Heavy-duty leather belt with multiple pouches. Padded back support.",
        "category": "Storage & Organization",
        "price": 65.99,
        "compare_price": 79.99,
        "image_url": "https://images.unsplash.com/photo-1504148455328-c376907d081c?w=400",
        "stock": 60,
        "sku": "ORG-001",
        "active": True,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
]

async def seed_products():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    # Check if products already exist
    count = await db.products.count_documents({})
    if count > 0:
        print(f"Products already seeded ({count} products found)")
        return
    
    # Insert products
    result = await db.products.insert_many(SAMPLE_PRODUCTS)
    print(f"Seeded {len(result.inserted_ids)} products")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_products())
