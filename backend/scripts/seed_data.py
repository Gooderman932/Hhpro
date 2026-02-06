"""
DEV ONLY - Seed database with sample data for development/testing.
WARNING: DO NOT run in production. Production users should only see
their own data and data from connected external APIs.
"""
import sys
sys.path.insert(0, '/app/backend')

from datetime import datetime, timedelta
from passlib.context import CryptContext
import uuid

from app.database import SessionLocal, Base, engine
from app.models.user import User, Tenant
from app.models.project import Project
from app.models.subscription import Subscription
from app.models.notification import NotificationPreference, NotificationLog

# Ensure all tables are created
Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_database():
    db = SessionLocal()
    try:
        # Create test tenant
        tenant = db.query(Tenant).filter(Tenant.name == "Test Organization").first()
        if not tenant:
            tenant = Tenant(name="Test Organization")
            db.add(tenant)
            db.flush()
            print(f"Created tenant: {tenant.name}")
        
        # Create Enterprise user
        enterprise_user = db.query(User).filter(User.email == "malcolmgoodmen@gmail.com").first()
        if not enterprise_user:
            enterprise_user = User(
                user_id=str(uuid.uuid4()),
                email="malcolmgoodmen@gmail.com",
                full_name="Malcolm Goodmen",
                hashed_password=pwd_context.hash("Test123!"),
                tenant_id=tenant.id,
                role="admin"
            )
            db.add(enterprise_user)
            db.flush()
            print(f"Created user: {enterprise_user.email}")
            
            # Create Enterprise subscription
            sub = Subscription(
                subscription_id=str(uuid.uuid4()),
                session_id=f"seed_{uuid.uuid4()}",
                user_id=enterprise_user.id,
                tier_id="enterprise",
                tier_name="Enterprise Platform",
                price=1999.00,
                status="active",
                expires_at=datetime.utcnow() + timedelta(days=365)
            )
            db.add(sub)
            print(f"Created enterprise subscription for {enterprise_user.email}")
        
        # Create Professional user
        pro_user = db.query(User).filter(User.email == "test@example.com").first()
        if not pro_user:
            pro_user = User(
                user_id=str(uuid.uuid4()),
                email="test@example.com",
                full_name="Test User",
                hashed_password=pwd_context.hash("test123"),
                tenant_id=tenant.id
            )
            db.add(pro_user)
            db.flush()
            print(f"Created user: {pro_user.email}")
            
            # Create Professional subscription
            sub = Subscription(
                subscription_id=str(uuid.uuid4()),
                session_id=f"seed_{uuid.uuid4()}",
                user_id=pro_user.id,
                tier_id="professional",
                tier_name="Professional Suite",
                price=799.00,
                status="active",
                expires_at=datetime.utcnow() + timedelta(days=365)
            )
            db.add(sub)
            print(f"Created professional subscription for {pro_user.email}")
        
        # Create sample projects
        existing_projects = db.query(Project).count()
        if existing_projects < 10:
            sample_projects = [
                {"title": "Downtown Office Complex", "sector": "Commercial", "value": 15000000, "city": "Austin", "state": "TX", "status": "bidding"},
                {"title": "Riverside Apartments Phase 2", "sector": "Residential", "value": 8500000, "city": "Houston", "state": "TX", "status": "awarded"},
                {"title": "Memorial Hospital Expansion", "sector": "Healthcare", "value": 45000000, "city": "Dallas", "state": "TX", "status": "planning"},
                {"title": "Tech Campus Building A", "sector": "Commercial", "value": 28000000, "city": "Phoenix", "state": "AZ", "status": "bidding"},
                {"title": "Sunset Mall Renovation", "sector": "Retail", "value": 12000000, "city": "Miami", "state": "FL", "status": "awarded"},
                {"title": "Industrial Park Warehouse", "sector": "Industrial", "value": 6500000, "city": "Tampa", "state": "FL", "status": "bidding"},
                {"title": "Community Center Project", "sector": "Public", "value": 4200000, "city": "Denver", "state": "CO", "status": "planning"},
                {"title": "Data Center Build-Out", "sector": "Industrial", "value": 35000000, "city": "Reno", "state": "NV", "status": "bidding"},
                {"title": "Luxury Condos Oceanview", "sector": "Residential", "value": 22000000, "city": "San Diego", "state": "CA", "status": "awarded"},
                {"title": "School District Upgrade", "sector": "Education", "value": 9800000, "city": "Atlanta", "state": "GA", "status": "planning"},
                {"title": "Highway Overpass Repair", "sector": "Infrastructure", "value": 5200000, "city": "Nashville", "state": "TN", "status": "bidding"},
                {"title": "Senior Living Facility", "sector": "Healthcare", "value": 18000000, "city": "Scottsdale", "state": "AZ", "status": "planning"},
                {"title": "Mixed-Use Development", "sector": "Commercial", "value": 42000000, "city": "Seattle", "state": "WA", "status": "bidding"},
                {"title": "Retail Strip Center", "sector": "Retail", "value": 7800000, "city": "Orlando", "state": "FL", "status": "awarded"},
                {"title": "Manufacturing Plant", "sector": "Industrial", "value": 25000000, "city": "Columbus", "state": "OH", "status": "planning"},
            ]
            
            for proj_data in sample_projects:
                project = Project(
                    title=proj_data["title"],
                    description=f"Sample project: {proj_data['title']}",
                    project_type="opportunity",
                    sector=proj_data["sector"],
                    value=proj_data["value"],
                    city=proj_data["city"],
                    state=proj_data["state"],
                    status=proj_data["status"],
                    tenant_id=tenant.id
                )
                db.add(project)
            
            print(f"Created {len(sample_projects)} sample projects")
        
        db.commit()
        print("Database seeding complete!")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
