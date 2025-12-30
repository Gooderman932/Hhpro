"""
Seed database with sample data.

Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.
PROPRIETARY AND CONFIDENTIAL - Unauthorized use prohibited.
"""
import sys
import os
from datetime import datetime, timedelta
import random

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.database import SessionLocal
from backend.app.models import Tenant, User, Company, Project, ProjectParticipation
from backend.app.utils.auth_utils import get_password_hash


def seed_database():
    """Seed the database with sample data."""
    db = SessionLocal()
    
    try:
        print("Seeding database...")
        
        # Create tenant
        tenant = Tenant(
            name="Demo Construction Company",
            subdomain="demo",
            is_active=True,
            subscription_tier="enterprise"
        )
        db.add(tenant)
        db.commit()
        db.refresh(tenant)
        print(f"Created tenant: {tenant.name}")
        
        # Create user
        user = User(
            email="demo@example.com",
            hashed_password=get_password_hash("demo123"),
            full_name="Demo User",
            is_active=True,
            tenant_id=tenant.id
        )
        db.add(user)
        db.commit()
        print(f"Created user: {user.email} (password: demo123)")
        
        # Create sample companies
        companies = [
            Company(
                name="BuildCo Construction Inc",
                company_type="GC",
                industry="Commercial",
                city="New York",
                state="NY",
                tenant_id=tenant.id
            ),
            Company(
                name="Metro Contractors LLC",
                company_type="GC",
                industry="Infrastructure",
                city="Los Angeles",
                state="CA",
                tenant_id=tenant.id
            ),
            Company(
                name="Prime Builders Corp",
                company_type="subcontractor",
                industry="Residential",
                city="Chicago",
                state="IL",
                tenant_id=tenant.id
            ),
        ]
        
        for company in companies:
            db.add(company)
        db.commit()
        print(f"Created {len(companies)} companies")
        
        # Create sample projects
        sectors = ["Commercial", "Residential", "Infrastructure", "Healthcare", "Education"]
        cities = [
            ("New York", "NY"), ("Los Angeles", "CA"), ("Chicago", "IL"),
            ("Houston", "TX"), ("Phoenix", "AZ"), ("Philadelphia", "PA"),
            ("San Antonio", "TX"), ("San Diego", "CA"), ("Dallas", "TX"),
            ("San Jose", "CA")
        ]
        
        projects = []
        for i in range(30):
            city, state = random.choice(cities)
            sector = random.choice(sectors)
            
            project = Project(
                title=f"{sector} Project {i+1} - {city}",
                description=f"Sample {sector.lower()} construction project in {city}, {state}",
                project_type=random.choice(["opportunity", "permit", "tender"]),
                sector=sector,
                status=random.choice(["active", "active", "active", "awarded", "completed"]),
                value=random.randint(500_000, 50_000_000),
                city=city,
                state=state,
                country="USA",
                is_verified=random.choice([True, False]),
                tenant_id=tenant.id
            )
            projects.append(project)
            db.add(project)
        
        db.commit()
        print(f"Created {len(projects)} projects")
        
        # Create project participations
        for project in projects[:15]:
            # Add 1-3 companies to each project
            num_participants = random.randint(1, 3)
            participating_companies = random.sample(companies, min(num_participants, len(companies)))
            
            for company in participating_companies:
                participation = ProjectParticipation(
                    project_id=project.id,
                    company_id=company.id,
                    role=random.choice(["owner", "gc", "subcontractor"]),
                    status=random.choice(["bidding", "won", "lost"]),
                    won=random.choice([True, False, None])
                )
                db.add(participation)
        
        db.commit()
        print("Created project participations")
        
        print("\n✓ Database seeded successfully!")
        print("\nYou can now login with:")
        print("  Email: demo@example.com")
        print("  Password: demo123")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
