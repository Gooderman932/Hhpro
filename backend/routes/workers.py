"""
Worker profile routes
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, List
from datetime import datetime
import uuid

from db.mongo import db
from auth.deps import get_current_user
from models.schemas import WorkerProfile, WorkerProfileCreate, User

router = APIRouter(prefix="/api/workers", tags=["Workers"])


@router.get("", response_model=List[WorkerProfile])
async def list_workers(
    trade_code: Optional[str] = None,
    limit: int = 50,
    current_user: User = Depends(get_current_user)
):
    query = {"is_active": True}
    if trade_code:
        query["trade_codes"] = trade_code
    
    projection = {
        "profile_id": 1, "user_id": 1, "trade_codes": 1, "hourly_rate": 1,
        "years_experience": 1, "bio": 1, "location": 1, "rating": 1,
        "is_active": 1, "created_at": 1, "_id": 0,
    }
    workers_cursor = db.worker_profiles.find(query, projection).limit(limit)
    workers = await workers_cursor.to_list(length=limit)
    
    return [
        WorkerProfile(
            profile_id=worker["profile_id"], user_id=worker["user_id"],
            trade_codes=worker["trade_codes"], hourly_rate=worker["hourly_rate"],
            years_experience=worker["years_experience"], bio=worker.get("bio"),
            location=worker["location"], rating=worker.get("rating", 0.0),
            is_active=worker["is_active"], created_at=worker["created_at"]
        )
        for worker in workers
    ]


@router.post("", response_model=WorkerProfile)
async def create_worker_profile(profile_data: WorkerProfileCreate, current_user: User = Depends(get_current_user)):
    existing_profile = await db.worker_profiles.find_one({"user_id": current_user.user_id})
    if existing_profile:
        raise HTTPException(status_code=400, detail="Worker profile already exists")
    
    profile_id = str(uuid.uuid4())
    profile_doc = {
        "profile_id": profile_id, "user_id": current_user.user_id,
        "trade_codes": profile_data.trade_codes, "hourly_rate": profile_data.hourly_rate,
        "years_experience": profile_data.years_experience, "bio": profile_data.bio,
        "location": profile_data.location, "rating": 0.0,
        "is_active": True, "created_at": datetime.utcnow()
    }
    
    await db.worker_profiles.insert_one(profile_doc)
    return WorkerProfile(**profile_doc)


@router.put("/{profile_id}", response_model=WorkerProfile)
async def update_worker_profile(profile_id: str, profile_data: WorkerProfileCreate, current_user: User = Depends(get_current_user)):
    profile = await db.worker_profiles.find_one({"profile_id": profile_id})
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    if profile["user_id"] != current_user.user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    update_data = {
        "trade_codes": profile_data.trade_codes, "hourly_rate": profile_data.hourly_rate,
        "years_experience": profile_data.years_experience, "bio": profile_data.bio,
        "location": profile_data.location
    }
    
    await db.worker_profiles.update_one({"profile_id": profile_id}, {"$set": update_data})
    updated_profile = await db.worker_profiles.find_one({"profile_id": profile_id})
    return WorkerProfile(**updated_profile)


@router.delete("/{profile_id}")
async def deactivate_worker_profile(profile_id: str, current_user: User = Depends(get_current_user)):
    profile = await db.worker_profiles.find_one({"profile_id": profile_id})
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    if profile["user_id"] != current_user.user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    await db.worker_profiles.update_one({"profile_id": profile_id}, {"$set": {"is_active": False}})
    return {"message": "Worker profile deactivated"}
