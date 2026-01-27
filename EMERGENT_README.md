# Construction Intelligence Platform - Emergent Setup

## 🚀 Quick Start

Your Construction Intelligence Platform is now set up on Emergent! 

### One-Command Setup
```bash
bash /app/scripts/quick-setup.sh
```

This script will:
- Install PostgreSQL and Redis
- Set up the database
- Install all dependencies
- Seed sample data

### Login Credentials
- **Email**: demo@example.com
- **Password**: demo123

### Access Your App
🌐 **Frontend**: https://market-data-migrate.preview.emergentagent.com

📡 **API Docs**: https://market-data-migrate.preview.emergentagent.com/api/docs

## 📋 Manual Commands

### Start/Stop Services
```bash
# Restart all services
bash /app/scripts/restart.sh

# Or use supervisor directly
supervisorctl restart backend frontend
supervisorctl status
```

### Check Service Logs
```bash
# Backend logs
tail -f /var/log/supervisor/backend.err.log

# Frontend logs
tail -f /var/log/supervisor/frontend.err.log
```

### Database Operations
```bash
# Access PostgreSQL
psql -U buildintel_user -d buildintel_db -h localhost

# Reset database (WARNING: Deletes all data!)
cd /app && python scripts/setup_db.py
cd /app && python scripts/seed_data.py
```

## 🎯 Features Available

### ✅ Project Management
- Track construction opportunities, permits, and tenders
- Advanced filtering by sector, location, value
- Status management and updates

### ✅ Analytics Dashboard
- Real-time metrics and KPIs
- Sector distribution charts
- Regional analysis
- Trend visualization

### ✅ Competitive Intelligence
- Competitor tracking and analysis
- Win rate calculations
- Market share visualization
- Company relationship mapping

### ✅ AI/ML Capabilities
- Win probability predictions
- Demand forecasting (6-month outlook)
- Opportunity scoring
- Entity extraction from documents

### ✅ Multi-Tenant Architecture
- Organization-level data isolation
- User management
- Role-based access control

## 🔧 Configuration

### Environment Variables
Backend config: `/app/backend/.env`
Frontend config: `/app/frontend/.env`

### Key Settings
- **Database**: PostgreSQL on localhost:5432
- **Cache**: Redis on localhost:6379
- **Backend Port**: 8001 (internal)
- **Frontend Port**: 5173 (internal)
- **External URL**: Via Emergent proxy

## 📊 API Endpoints

### Authentication
- `POST /api/v1/auth/token` - Login
- `POST /api/v1/auth/register` - Register
- `GET /api/v1/auth/me` - Current user

### Projects
- `GET /api/v1/projects/` - List projects
- `GET /api/v1/projects/{id}` - Get project
- `POST /api/v1/projects/` - Create project
- `PUT /api/v1/projects/{id}` - Update project
- `DELETE /api/v1/projects/{id}` - Delete project

### Analytics
- `GET /api/v1/analytics/summary` - Dashboard summary
- `GET /api/v1/analytics/trends` - Project trends
- `GET /api/v1/analytics/regions` - Regional analysis

### Intelligence
- `GET /api/v1/intelligence/competitors` - Competitor data
- `GET /api/v1/intelligence/market-share` - Market share
- `GET /api/v1/intelligence/relationships` - Relationship graph

## 💰 Monetization Features (Coming Soon)

### Planned Additions
- ✨ Stripe payment integration
- ✨ Subscription tiers (Free, Pro, Enterprise)
- ✨ Usage tracking and limits
- ✨ Admin dashboard for billing
- ✨ API credit system
- ✨ White-label options

## 🐛 Troubleshooting

### Backend Not Starting
```bash
# Check logs
tail -50 /var/log/supervisor/backend.err.log

# Restart PostgreSQL
service postgresql restart

# Restart backend
supervisorctl restart backend
```

### Frontend Not Loading
```bash
# Check logs
tail -50 /var/log/supervisor/frontend.err.log

# Restart frontend
supervisorctl restart frontend
```

### Database Connection Issues
```bash
# Check PostgreSQL is running
service postgresql status

# Restart PostgreSQL
service postgresql restart
```

### Port Conflicts
```bash
# Kill conflicting processes
pkill -f uvicorn
pkill -f vite

# Restart services
supervisorctl restart all
```

## 📚 Documentation

- **Full Documentation**: `/app/README.md`
- **Project Overview**: `/app/PROJECT_OVERVIEW.md`
- **Quick Start Guide**: `/app/QUICKSTART.md`
- **Deployment Guide**: `/app/DEPLOYMENT.md`
- **Security Guide**: `/app/SECURITY.md`

## 🔐 Security Notes

⚠️ **Important**: Before production deployment:
1. Change SECRET_KEY in `/app/backend/.env`
2. Use strong database passwords
3. Enable HTTPS
4. Configure proper CORS origins
5. Set ENVIRONMENT=production
6. Review `/app/SECURITY.md`

## 🎉 What's Working

✅ Backend API with FastAPI
✅ Frontend with React + TypeScript + Vite
✅ PostgreSQL database
✅ Redis caching
✅ User authentication
✅ Project management
✅ Analytics dashboard
✅ Competitive intelligence
✅ ML/AI predictions
✅ Sample data loaded

## 📞 Support

For issues or questions:
- Check logs in `/var/log/supervisor/`
- Review documentation in `/app/docs/`
- Inspect database: `psql -U buildintel_user -d buildintel_db`

---

**Built with**: Python, TypeScript, React, FastAPI, PostgreSQL, Docker
**Status**: ✅ Development Ready
**License**: Proprietary (Poor Dude Holdings LLC)
