"""
Products and shop routes
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, List
from datetime import datetime
import uuid

from db.mongo import db
from auth.deps import get_current_user
from models.schemas import Product, ProductCreate, User

router = APIRouter(prefix="/api/products", tags=["Products"])


@router.get("", response_model=List[Product])
async def list_products(
    category: Optional[str] = None,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
):
    query = {}
    if category:
        query["category"] = category
    
    projection = {
        "product_id": 1, "name": 1, "description": 1, "category": 1,
        "price": 1, "stock": 1, "created_at": 1, "_id": 0,
    }
    products_cursor = db.products.find(query, projection).limit(limit)
    products = await products_cursor.to_list(length=limit)
    
    return [
        Product(
            product_id=product["product_id"], name=product["name"],
            description=product["description"], category=product["category"],
            price=product["price"], stock=product["stock"], created_at=product["created_at"]
        )
        for product in products
    ]


@router.post("", response_model=Product)
async def create_product(product_data: ProductCreate, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    product_id = str(uuid.uuid4())
    product_doc = {
        "product_id": product_id, "name": product_data.name,
        "description": product_data.description, "category": product_data.category,
        "price": product_data.price, "stock": product_data.stock,
        "created_at": datetime.utcnow()
    }
    
    await db.products.insert_one(product_doc)
    return Product(**product_doc)


@router.put("/{product_id}/stock")
async def update_stock(product_id: str, quantity: int, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    product = await db.products.find_one({"product_id": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    new_stock = product["stock"] + quantity
    if new_stock < 0:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    
    await db.products.update_one({"product_id": product_id}, {"$set": {"stock": new_stock}})
    return {"message": "Stock updated", "new_stock": new_stock}
