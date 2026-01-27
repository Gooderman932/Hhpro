"""
Orders routes
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import datetime
import uuid

from db.mongo import db
from auth.deps import get_current_user
from models.schemas import Order, OrderCreate, User

router = APIRouter(prefix="/api/orders", tags=["Orders"])


@router.get("", response_model=List[Order])
async def list_orders(limit: int = 50, current_user: User = Depends(get_current_user)):
    query = {"user_id": current_user.user_id}
    if current_user.role == "admin":
        query = {}
    
    projection = {
        "order_id": 1, "user_id": 1, "product_id": 1, "quantity": 1,
        "total_amount": 1, "status": 1, "created_at": 1, "_id": 0,
    }
    orders_cursor = db.orders.find(query, projection).limit(limit)
    orders = await orders_cursor.to_list(length=limit)
    
    return [
        Order(
            order_id=order["order_id"], user_id=order["user_id"],
            product_id=order["product_id"], quantity=order["quantity"],
            total_amount=order["total_amount"], status=order["status"],
            created_at=order["created_at"]
        )
        for order in orders
    ]


@router.post("", response_model=Order)
async def create_order(order_data: OrderCreate, current_user: User = Depends(get_current_user)):
    product = await db.products.find_one({"product_id": order_data.product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product["stock"] < order_data.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    
    order_id = str(uuid.uuid4())
    order_doc = {
        "order_id": order_id, "user_id": current_user.user_id,
        "product_id": order_data.product_id, "quantity": order_data.quantity,
        "total_amount": order_data.total_amount, "status": "pending",
        "created_at": datetime.utcnow()
    }
    
    await db.orders.insert_one(order_doc)
    await db.products.update_one(
        {"product_id": order_data.product_id},
        {"$inc": {"stock": -order_data.quantity}}
    )
    
    return Order(**order_doc)
