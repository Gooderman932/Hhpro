"""
Database connection and structure verification script.

Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.
PROPRIETARY AND CONFIDENTIAL - Unauthorized use prohibited.
"""
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from sqlalchemy import create_engine, text, inspect
    from sqlalchemy.orm import sessionmaker
    SQLALCHEMY_AVAILABLE = True
except ImportError:
    SQLALCHEMY_AVAILABLE = False
    print("❌ SQLAlchemy not available. Install with: pip install sqlalchemy")
    sys.exit(1)


def print_header(text):
    """Print formatted header."""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)


def print_section(text):
    """Print formatted section."""
    print(f"\n{'─'*70}")
    print(f"  {text}")
    print(f"{'─'*70}")


def verify_connection(database_url):
    """Verify database connection."""
    print_section("🔌 Testing Database Connection")
    
    try:
        engine = create_engine(database_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            if result:
                print("✅ Database connection successful")
                return engine
            else:
                print("❌ Database connection failed")
                return None
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        return None


def get_tables(engine, database_url):
    """Get list of existing tables."""
    print_section("📋 Checking Database Tables")
    
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        if tables:
            print(f"Found {len(tables)} tables in database:")
            for table in sorted(tables):
                print(f"  ✅ {table}")
            return tables
        else:
            print("⚠️  No tables found in database")
            return []
    except Exception as e:
        print(f"❌ Error getting tables: {str(e)}")
        return []


def check_required_tables(existing_tables):
    """Check if all required tables exist."""
    print_section("🔍 Verifying Required Tables")
    
    required_tables = {
        "users": "User accounts and authentication",
        "tenants": "Multi-tenant organizations",
        "projects": "Construction projects and opportunities",
        "companies": "Companies and contractors",
        "project_participations": "Project-company relationships",
        "opportunity_scores": "ML-generated opportunity scores",
        "predictions": "ML predictions and forecasts"
    }
    
    all_exist = True
    missing_tables = []
    
    for table, description in required_tables.items():
        if table in existing_tables:
            print(f"  ✅ {table:30} - {description}")
        else:
            print(f"  ❌ {table:30} - {description} (MISSING)")
            all_exist = False
            missing_tables.append(table)
    
    return all_exist, missing_tables


def get_table_counts(engine, tables):
    """Get row counts for each table."""
    print_section("📊 Table Row Counts")
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        for table in sorted(tables):
            try:
                result = session.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.scalar()
                print(f"  {table:30} {count:>10} rows")
            except Exception as e:
                print(f"  {table:30} Error: {str(e)}")
    finally:
        session.close()


def test_write_capability(engine):
    """Test database write capabilities."""
    print_section("✍️  Testing Write Capabilities")
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Create a test table
        test_table_name = f"test_verification_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        session.execute(text(f"""
            CREATE TABLE {test_table_name} (
                id INTEGER PRIMARY KEY,
                test_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        print(f"  ✅ Created test table: {test_table_name}")
        
        # Insert test data
        session.execute(text(f"""
            INSERT INTO {test_table_name} (id, test_data) VALUES (1, 'test')
        """))
        session.commit()
        print("  ✅ Inserted test data")
        
        # Read test data
        result = session.execute(text(f"SELECT * FROM {test_table_name}"))
        row = result.fetchone()
        if row:
            print("  ✅ Read test data successfully")
        
        # Clean up
        session.execute(text(f"DROP TABLE {test_table_name}"))
        session.commit()
        print("  ✅ Cleaned up test table")
        
        print("\n  ✅ Write capabilities verified")
        return True
        
    except Exception as e:
        print(f"  ❌ Write test failed: {str(e)}")
        session.rollback()
        return False
    finally:
        session.close()


def print_migration_guide(missing_tables):
    """Print guide for running migrations."""
    print_section("🔧 Next Steps")
    
    if missing_tables:
        print("\n⚠️  Some required tables are missing. You need to run database migrations:")
        print("\n  Option 1: Using Alembic (recommended)")
        print("  ─────────────────────────────────────")
        print("  $ cd backend")
        print("  $ alembic upgrade head")
        print("\n  Option 2: Using init_db (for development)")
        print("  ─────────────────────────────────────")
        print("  $ cd backend")
        print("  $ python -c 'from app.database import init_db; init_db()'")
        print("\n  Option 3: Using setup script")
        print("  ─────────────────────────────────────")
        print("  $ cd scripts")
        print("  $ python setup_db.py")
    else:
        print("\n✅ Database is properly configured!")
        print("\n  You can start the application:")
        print("  $ cd backend")
        print("  $ uvicorn app.main:app --reload")
        print("\n  Or run the full stack:")
        print("  $ docker-compose up")


def main():
    """Main verification function."""
    print_header("🗄️  BuildIntel Pro - Database Verification")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Get database URL from environment
    database_url = os.getenv("DATABASE_URL", "sqlite:///./construction_intel.db")
    print(f"\nDatabase URL: {database_url}")
    
    # Verify connection
    engine = verify_connection(database_url)
    if not engine:
        print("\n❌ Cannot proceed without database connection")
        sys.exit(1)
    
    # Get tables
    existing_tables = get_tables(engine, database_url)
    
    # Check required tables
    all_exist, missing_tables = check_required_tables(existing_tables)
    
    # Get row counts if tables exist
    if existing_tables:
        get_table_counts(engine, existing_tables)
    
    # Test write capability
    write_ok = test_write_capability(engine)
    
    # Print migration guide if needed
    print_migration_guide(missing_tables)
    
    # Summary
    print_header("📝 Summary")
    print(f"  Database URL: {database_url}")
    print(f"  Connection: {'✅ OK' if engine else '❌ Failed'}")
    print(f"  Tables Found: {len(existing_tables)}")
    print(f"  Required Tables: {'✅ All present' if all_exist else f'❌ {len(missing_tables)} missing'}")
    print(f"  Write Access: {'✅ OK' if write_ok else '❌ Failed'}")
    print("="*70 + "\n")
    
    # Exit code
    if all_exist and write_ok:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
