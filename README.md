# Construction Intelligence Platform

Enterprise SaaS platform for construction market intelligence, project discovery, and competitive analysis.

## 🏗️ Overview

A comprehensive platform that combines AI/ML capabilities with real-time construction market data to provide:
- **Project Discovery**: Track opportunities, permits, and tenders
- **Competitive Intelligence**: Analyze competitor activity and market share
- **Predictive Analytics**: Win probability models and demand forecasting
- **Market Insights**: Regional analysis and trend visualization

## 🚀 Tech Stack

### Backend
- **Framework**: Python 3.11+ with FastAPI
- **Database**: PostgreSQL 16
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT with bcrypt
- **ML/AI**: scikit-learn, OpenAI API
- **Migration**: Alembic

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **UI Components**: Custom components with Tailwind CSS
- **Charts**: Recharts
- **State Management**: TanStack Query (React Query)
- **Routing**: React Router v6

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **API Documentation**: FastAPI automatic OpenAPI/Swagger

## 📁 Project Structure

```
construction-intelligence-platform/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI app entry
│   │   ├── config.py               # Configuration
│   │   ├── database.py             # DB connection
│   │   ├── models/                 # SQLAlchemy models
│   │   │   ├── user.py
│   │   │   ├── company.py
│   │   │   ├── project.py
│   │   │   └── prediction.py
│   │   ├── api/                    # API endpoints
│   │   │   ├── auth.py
│   │   │   ├── projects.py
│   │   │   ├── analytics.py
│   │   │   └── intelligence.py
│   │   ├── services/               # Business logic
│   │   │   ├── data_ingestion.py
│   │   │   ├── enrichment.py
│   │   │   ├── classification.py
│   │   │   ├── prediction.py
│   │   │   └── scoring.py
│   │   ├── ml/                     # ML models
│   │   │   ├── win_probability.py
│   │   │   ├── demand_forecast.py
│   │   │   └── entity_extraction.py
│   │   └── utils/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── alembic/                    # DB migrations
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   ├── components/
│   │   │   ├── dashboard/
│   │   │   │   ├── ProjectRadar.tsx
│   │   │   │   ├── OpportunityList.tsx
│   │   │   │   └── Analytics.tsx
│   │   │   ├── intelligence/
│   │   │   │   ├── CompetitorMap.tsx
│   │   │   │   └── RelationshipGraph.tsx
│   │   │   ├── pricing/
│   │   │   │   └── DemandForecast.tsx
│   │   │   └── common/
│   │   │       ├── Navigation.tsx
│   │   │       └── DataTable.tsx
│   │   ├── services/
│   │   │   └── api.ts
│   │   ├── hooks/
│   │   │   └── useAuth.ts
│   │   └── types/
│   │       └── index.ts
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── data/
│   ├── seeds/                      # Sample data
│   └── schemas/                    # Data schemas
├── scripts/
│   ├── setup_db.py                 # Database setup
│   └── seed_data.py                # Data seeding
└── docker-compose.yml
```

## 🛠️ Setup & Installation

### Prerequisites
- Docker & Docker Compose (recommended)
- OR: Python 3.11+, Node.js 20+, PostgreSQL 16

### Option 1: Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/Gooderman932/market-data.git
cd market-data
```

2. Create environment file:
```bash
cat > .env << EOF
SECRET_KEY=your-secret-key-change-in-production
OPENAI_API_KEY=your-openai-api-key-optional
EOF
```

3. Start all services:
```bash
docker-compose up -d
```

4. Set up database (first time only):
```bash
docker-compose exec backend python scripts/setup_db.py
docker-compose exec backend python scripts/seed_data.py
```

5. Access the application:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Local Development

#### Backend Setup

1. Create virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
export DATABASE_URL="postgresql://user:password@localhost:5432/construction_intel"
export SECRET_KEY="your-secret-key"
```

4. Set up database:
```bash
# Make sure PostgreSQL is running
python ../scripts/setup_db.py
python ../scripts/seed_data.py
```

5. Run the backend:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Run development server:
```bash
npm run dev
```

3. Access at http://localhost:5173

## 🔐 Default Credentials

After seeding the database:
- **Email**: demo@example.com
- **Password**: demo123

## 📚 API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Key Endpoints

#### Authentication
- `POST /api/auth/token` - Login
- `POST /api/auth/register` - Register new user
- `GET /api/auth/me` - Get current user

#### Projects
- `GET /api/projects/` - List projects
- `GET /api/projects/{id}` - Get project details
- `POST /api/projects/` - Create project
- `PUT /api/projects/{id}` - Update project
- `DELETE /api/projects/{id}` - Delete project

#### Analytics
- `GET /api/analytics/summary` - Get dashboard summary
- `GET /api/analytics/trends` - Get project trends
- `GET /api/analytics/regions` - Get regional analysis

#### Intelligence
- `GET /api/intelligence/competitors` - Get competitor data
- `GET /api/intelligence/market-share` - Get market share analysis
- `GET /api/intelligence/relationships` - Get relationship graph

## 🎯 Key Features

### 1. Project Radar Dashboard
- Real-time project tracking
- Summary metrics and KPIs
- Recent project listings
- Status monitoring

### 2. Opportunity Discovery
- Advanced filtering and search
- Project categorization by sector
- Value and location tracking
- Status management

### 3. Analytics & Insights
- Sector distribution analysis
- Regional project mapping
- Trend visualization
- Custom date ranges

### 4. Competitive Intelligence
- Competitor tracking and analysis
- Win rate calculations
- Market share visualization
- Project participation history

### 5. Relationship Mapping
- Company relationship graphs
- Shared project identification
- Network visualization
- Partnership analysis

### 6. Demand Forecasting
- AI-powered predictions
- 6-month forecasts
- Confidence intervals
- Seasonal analysis

## 🔧 Configuration

### Environment Variables

**Backend** (.env or environment):
```bash
# Application
APP_NAME="Construction Intelligence Platform"
APP_VERSION="0.1.0"
DEBUG=False

# Database
DATABASE_URL="postgresql://user:password@localhost:5432/construction_intel"

# Authentication
SECRET_KEY="your-secret-key-change-in-production"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI (optional)
OPENAI_API_KEY="your-openai-api-key"

# CORS
CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]
```

**Frontend** (.env):
```bash
VITE_API_URL=http://localhost:8000
```

## 🧪 Development

### Database Migrations

Create a new migration:
```bash
cd backend
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback:
```bash
alembic downgrade -1
```

### Adding New Data

Use the data ingestion service:
```python
from app.services import DataIngestionService
from app.database import SessionLocal

db = SessionLocal()
service = DataIngestionService(db)

project_data = {
    "title": "New Project",
    "project_type": "opportunity",
    "sector": "Commercial",
    "value": 5000000,
    "city": "New York",
    "state": "NY"
}

project = service.ingest_project(project_data, tenant_id=1, source="manual")
```

## 🚢 Production Deployment

### Docker Production Build

1. Build production images:
```bash
docker-compose -f docker-compose.prod.yml build
```

2. Deploy with proper environment variables
3. Use a reverse proxy (nginx) for SSL/TLS
4. Set up database backups
5. Configure logging and monitoring

### Security Considerations

- Change default SECRET_KEY
- Use strong passwords
- Enable HTTPS in production
- Implement rate limiting
- Regular security updates
- Database encryption at rest
- Secure API key storage

## 📊 Data Models

### Core Entities

**Tenant**: Multi-tenancy support
- Organization/company isolation
- Subscription tier management

**User**: Authentication and authorization
- Email-based authentication
- JWT token-based sessions
- Role-based access control

**Project**: Construction opportunities
- Opportunities, permits, tenders
- Value tracking
- Location data
- Status management

**Company**: Market participants
- GCs, subcontractors, suppliers
- Historical performance
- Contact information

**ProjectParticipation**: Relationships
- Company-project associations
- Win/loss tracking
- Role definitions

**Prediction**: ML predictions
- Win probability
- Demand forecasts
- Confidence scores

**OpportunityScore**: Scoring engine
- Multi-factor scoring
- Value, fit, competition, timing, risk
- Reasoning explanations

## 🗺️ Roadmap

### Phase 1: Foundation ✓
- Database models and schemas
- Authentication and multi-tenancy
- Basic API structure
- Data ingestion pipeline
- Project classification service

### Phase 2: Intelligence ✓
- Entity extraction and enrichment
- Opportunity scoring engine
- Win probability models
- Competitive intelligence mapping
- Dashboard UI components

### Phase 3: Analytics (Planned)
- Advanced demand forecasting
- Pricing analytics
- Scenario analysis
- Enhanced visualizations
- White-label reporting

### Phase 4: Enterprise (Future)
- SSO integration
- API gateway for customers
- Export and integration tools
- Admin panel
- Billing and subscription management

---

Built with ❤️ for the construction industry
