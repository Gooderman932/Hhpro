"""
Payment routes
"""
from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
import uuid

from db.mongo import db
from auth.deps import get_current_user
from models.schemas import PaymentTransaction, User

router = APIRouter(prefix="/api/payments", tags=["Payments"])


@router.post("")
async def create_payment(order_id: str, current_user: User = Depends(get_current_user)):
    order = await db.orders.find_one({"order_id": order_id})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order["user_id"] != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    if order["status"] == "paid":
        raise HTTPException(status_code=400, detail="Order already paid")
    
    transaction_id = str(uuid.uuid4())
    transaction_doc = {
        "transaction_id": transaction_id,
        "order_id": order_id,
        "user_id": current_user.user_id,
        "amount": order["total_amount"],
        "status": "completed",
        "created_at": datetime.utcnow()
    }
    
    await db.payment_transactions.insert_one(transaction_doc)
    await db.orders.update_one({"order_id": order_id}, {"$set": {"status": "paid"}})
    
    return PaymentTransaction(**transaction_doc)
