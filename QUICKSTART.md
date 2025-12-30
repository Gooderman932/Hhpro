# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Using Docker (Easiest)

1. **Clone and navigate to the project:**
   ```bash
   git clone https://github.com/Gooderman932/market-data.git
   cd market-data
   ```

2. **Start the services:**
   ```bash
   docker-compose up -d
   ```

3. **Initialize the database:**
   ```bash
   docker-compose exec backend python scripts/setup_db.py
   docker-compose exec backend python scripts/seed_data.py
   ```

4. **Access the application:**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

5. **Login with demo credentials:**
   - Email: `demo@example.com`
   - Password: `demo123`

### Manual Setup (Without Docker)

#### Backend

```bash
# Install Python dependencies
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up PostgreSQL database
createdb construction_intel

# Configure environment
export DATABASE_URL="postgresql://user:password@localhost:5432/construction_intel"
export SECRET_KEY="your-secret-key-here"

# Initialize database
python ../scripts/setup_db.py
python ../scripts/seed_data.py

# Start the backend
uvicorn app.main:app --reload
```

#### Frontend

```bash
# Install Node.js dependencies
cd frontend
npm install

# Start the development server
npm run dev
```

## 🎯 What to Try First

1. **Dashboard**: View project metrics and recent opportunities
2. **Opportunities**: Browse and filter construction projects
3. **Analytics**: Explore sector distribution and regional analysis
4. **Competitors**: Analyze competitor activity and win rates
5. **Forecasting**: View demand predictions and scenario analysis

## 📱 Main Features

### Project Management
- Create, update, and track construction projects
- Filter by sector, status, location, and value
- Import data from various sources

### Analytics & Intelligence
- Real-time market insights
- Competitor tracking and analysis
- Regional distribution and trends
- Win rate calculations

### AI/ML Capabilities
- Opportunity scoring
- Win probability predictions
- Demand forecasting
- Entity extraction from text

## 🔧 API Usage

### Authentication
```bash
# Get access token
curl -X POST http://localhost:8000/api/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=demo@example.com&password=demo123"

# Use token in subsequent requests
curl -X GET http://localhost:8000/api/projects/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Creating a Project
```bash
curl -X POST http://localhost:8000/api/projects/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Office Building",
    "project_type": "opportunity",
    "sector": "Commercial",
    "value": 5000000,
    "city": "San Francisco",
    "state": "CA",
    "status": "active"
  }'
```

## 🛠️ Development

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Quality
```bash
# Backend linting
cd backend
flake8 app/

# Frontend linting
cd frontend
npm run lint
```

## 📚 Next Steps

- Review the [full README](README.md) for detailed documentation
- Explore API endpoints at http://localhost:8000/docs
- Check out the [data schemas](data/schemas/) for data format reference
- Review [sample data](data/seeds/) for examples

## 🆘 Troubleshooting

### Port Already in Use
```bash
# Change ports in docker-compose.yml or stop conflicting services
lsof -i :8000  # Check what's using port 8000
lsof -i :5173  # Check what's using port 5173
```

### Database Connection Issues
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# View logs
docker-compose logs postgres
docker-compose logs backend
```

### Frontend Build Issues
```bash
# Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## 💡 Tips

- Use the API documentation at `/docs` to explore all endpoints
- The demo account has full access to all features
- Sample data includes 30 projects across multiple sectors
- All endpoints support pagination with `skip` and `limit` parameters
- Use filters to narrow down results by sector, status, location, etc.

---

Happy building! 🏗️
