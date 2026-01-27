"""
Jobs routes
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, List
from datetime import datetime
import uuid

from db.mongo import db
from auth.deps import get_current_user
from models.schemas import Job, JobCreate, User

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])


@router.get("", response_model=List[Job])
async def list_jobs(
    trade_code: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 50,
    current_user: User = Depends(get_current_user)
):
    query = {}
    if trade_code:
        query["trade_codes"] = trade_code
    if status:
        query["status"] = status
    
    projection = {
        "job_id": 1, "title": 1, "description": 1, "trade_codes": 1,
        "location": 1, "budget": 1, "status": 1, "customer_id": 1,
        "created_at": 1, "updated_at": 1, "_id": 0,
    }
    jobs_cursor = db.jobs.find(query, projection).limit(limit)
    jobs = await jobs_cursor.to_list(length=limit)
    
    return [
        Job(
            job_id=job["job_id"], title=job["title"], description=job["description"],
            trade_codes=job["trade_codes"], location=job["location"],
            budget=job.get("budget"), status=job["status"], customer_id=job["customer_id"],
            created_at=job["created_at"], updated_at=job["updated_at"]
        )
        for job in jobs
    ]


@router.post("", response_model=Job)
async def create_job(job_data: JobCreate, current_user: User = Depends(get_current_user)):
    job_id = str(uuid.uuid4())
    now = datetime.utcnow()
    
    job_doc = {
        "job_id": job_id, "customer_id": current_user.user_id,
        "title": job_data.title, "description": job_data.description,
        "trade_codes": job_data.trade_codes, "location": job_data.location,
        "budget": job_data.budget, "status": job_data.status,
        "created_at": now, "updated_at": now
    }
    
    await db.jobs.insert_one(job_doc)
    return Job(**job_doc)


@router.put("/{job_id}", response_model=Job)
async def update_job(job_id: str, job_data: JobCreate, current_user: User = Depends(get_current_user)):
    job = await db.jobs.find_one({"job_id": job_id})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job["customer_id"] != current_user.user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    update_data = {
        "title": job_data.title, "description": job_data.description,
        "trade_codes": job_data.trade_codes, "location": job_data.location,
        "budget": job_data.budget, "status": job_data.status,
        "updated_at": datetime.utcnow()
    }
    
    await db.jobs.update_one({"job_id": job_id}, {"$set": update_data})
    updated_job = await db.jobs.find_one({"job_id": job_id})
    return Job(**updated_job)


@router.delete("/{job_id}")
async def close_job(job_id: str, current_user: User = Depends(get_current_user)):
    job = await db.jobs.find_one({"job_id": job_id})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job["customer_id"] != current_user.user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    await db.jobs.update_one(
        {"job_id": job_id},
        {"$set": {"status": "closed", "updated_at": datetime.utcnow()}}
    )
    
    return {"message": "Job closed successfully"}
