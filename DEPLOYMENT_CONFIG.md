# HDrywall Pro - Deployment Configuration

## ✅ Changes Completed

All requested changes have been successfully implemented:

### 1. ✅ MongoDB Migration Complete
- **Backend migrated** from PostgreSQL to MongoDB using Motor (async driver)
- **Database name**: `test_database`
- **Collections created**:
  - `users` - with unique index on `email`
  - `jobs` - with indexes on `trade_codes`, `job_id`, `customer_id`
  - `worker_profiles` - with indexes on `profile_id`, `user_id`, `trade_codes`
  - `products` - with index on `category`
  - `orders` - with indexes on `order_id`, `user_id`
  - `payment_transactions` - with indexes on `transaction_id`, `order_id`
  - `user_sessions` - with indexes on `session_id`, `user_id`
  - `subscriptions` - with indexes on `subscription_id`, `user_id`

- **All IDs use string fields**: `user_id`, `job_id`, `profile_id`, `product_id`, etc.
- **All CRUD operations** updated to use MongoDB client
- **Authentication working**: register, login, get current user
- **Jobs API working**: create, list, update, close jobs
- **Worker profiles**: create, list, update, deactivate
- **Products/Shop**: list, create, update stock
- **Orders**: create, list orders
- **Payments**: create payment transactions

### 2. ✅ ML Dependencies Removed
- Removed heavy ML dependencies from `requirements.txt`:
  - scikit-learn, pandas, numpy, spacy, sentence-transformers
- Kept only lightweight packages
- **OpenAI integration ready** for external ML API calls if needed
- Current `requirements.txt` is lean and optimized for deployment

### 3. ✅ Supervisor Backend Command Fixed
- **Program name**: `backend`
- **Command**: `uvicorn server:app --host 0.0.0.0 --port 8001`
- **Directory**: `/app/backend`
- Configuration file: `/etc/supervisor/conf.d/supervisord.conf`
- **Status**: ✅ Running successfully

### 4. ✅ CORS Configuration Updated
- **Format**: Comma-separated string
- **Backend parsing**: Splits string into list at runtime
- **Current value**: `https://pro.hdrywallrepair.com,https://intel.hdrywallrepair.com,http://localhost:3000`
- **Production domains supported**: 
  - https://pro.hdrywallrepair.com
  - https://intel.hdrywallrepair.com
- **Local development**: http://localhost:3000

### 5. ✅ Vite Port Changed to 3000
- **Dev server port**: 3000
- **Configuration**: `vite.config.ts`
- **Dev URL**: http://localhost:3000
- **Frontend running**: ✅ Successfully on port 3000

---

## 🔧 Required Environment Variables

### For Deployment, Set These Environment Variables:

```bash
# MongoDB Connection
MONGO_URL=mongodb://localhost:27017
DB_NAME=test_database

# Application Security
SECRET_KEY=your-secret-key-change-in-production-minimum-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Origins (comma-separated)
CORS_ORIGINS=https://pro.hdrywallrepair.com,https://intel.hdrywallrepair.com,http://localhost:3000

# Environment
ENVIRONMENT=production
DEBUG=false

# Optional: External ML API (only if using ML features)
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4o
```

### Production Values (Copy-Paste Ready):

```bash
MONGO_URL=mongodb://localhost:27017
DB_NAME=test_database
SECRET_KEY=buildintel-secret-key-change-in-production-xyz123
CORS_ORIGINS=https://pro.hdrywallrepair.com,https://intel.hdrywallrepair.com,http://localhost:3000
ENVIRONMENT=production
DEBUG=false
```

---

## 📋 Service Configuration Details

### Backend Service (Supervisor)
```ini
[program:backend]
command=/root/.venv/bin/uvicorn server:app --host 0.0.0.0 --port 8001
directory=/app/backend
autostart=true
autorestart=true
```

**To restart backend:**
```bash
supervisorctl restart backend
```

**Check status:**
```bash
supervisorctl status backend
```

**View logs:**
```bash
tail -f /var/log/supervisor/backend.out.log
```

### Frontend Service (Supervisor)
```ini
[program:frontend]
command=yarn dev --port 3000 --host 0.0.0.0
directory=/app/frontend
autostart=true
autorestart=true
```

**To restart frontend:**
```bash
supervisorctl restart frontend
```

**Dev URL:** http://localhost:3000

### MongoDB Service
```bash
# Start MongoDB
supervisorctl start mongodb

# Check status
supervisorctl status mongodb
```

---

## 🧪 API Testing

### Health Check
```bash
curl http://localhost:8001/health
# Response: {"status":"healthy","service":"HDrywall Pro API"}
```

### Register User
```bash
curl -X POST http://localhost:8001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "full_name": "John Doe",
    "role": "customer"
  }'
```

### Login
```bash
curl -X POST http://localhost:8001/api/auth/token \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user@example.com",
    "password": "password123"
  }'
```

### Create Job (with auth token)
```bash
TOKEN="your-jwt-token-here"

curl -X POST http://localhost:8001/api/jobs \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Drywall Repair",
    "description": "Need drywall repair in living room",
    "trade_codes": ["drywall"],
    "location": "San Francisco, CA",
    "budget": 500.00,
    "status": "open"
  }'
```

### List Jobs
```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8001/api/jobs?limit=10
```

---

## 📊 Database Information

### Collections and Indexes

| Collection | Indexes | Purpose |
|------------|---------|---------|
| `users` | email (unique), user_id | User accounts |
| `jobs` | trade_codes, job_id, customer_id | Job postings |
| `worker_profiles` | profile_id, user_id, trade_codes | Worker profiles |
| `products` | category, product_id | Shop products |
| `orders` | order_id, user_id | Customer orders |
| `payment_transactions` | transaction_id, order_id | Payments |
| `user_sessions` | session_id, user_id | User sessions |
| `subscriptions` | subscription_id, user_id | Subscriptions |

### Initialize Database
```bash
cd /app
python scripts/init-mongodb.py
```

### Check Database
```bash
# Connect to MongoDB
mongo test_database

# List collections
show collections

# Count documents in users collection
db.users.count()

# View a sample user
db.users.findOne()
```

---

## 🚀 Deployment Checklist

- [x] MongoDB migration complete
- [x] ML dependencies removed
- [x] Supervisor command fixed (`server:app`)
- [x] CORS configuration updated (comma-separated)
- [x] Vite port changed to 3000
- [x] All services running successfully
- [x] API endpoints tested and working
- [x] Database initialized with indexes

### Next Steps for Emergent Deployment:

1. **Set environment variables** in Emergent dashboard
2. **Restart services** via supervisor
3. **Test endpoints** from production URLs
4. **Monitor logs** for any issues

---

## 🔗 Service URLs

### Local Development
- **Backend API**: http://localhost:8001
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8001/docs
- **MongoDB**: mongodb://localhost:27017

### Production (Update with actual domains)
- **Frontend**: https://pro.hdrywallrepair.com or https://intel.hdrywallrepair.com
- **Backend**: (will be proxied through frontend domain)

---

## 📝 Key Files Modified

### Backend
- `/app/backend/server.py` - New MongoDB-based API (complete rewrite)
- `/app/backend/requirements.txt` - Removed ML dependencies
- `/app/backend/.env` - Updated with MongoDB config and comma-separated CORS

### Frontend
- `/app/frontend/vite.config.ts` - Changed port to 3000
- `/app/frontend/.env` - Updated backend URL

### Configuration
- `/etc/supervisor/conf.d/supervisord.conf` - Fixed backend command to `server:app`

### Scripts
- `/app/scripts/init-mongodb.py` - Database initialization script

---

## ✅ Verification

All changes have been implemented and tested:

```bash
# ✅ Backend running on port 8001
curl http://localhost:8001/health

# ✅ Frontend running on port 3000
curl http://localhost:3000

# ✅ MongoDB running
supervisorctl status mongodb

# ✅ API authentication working
# (Registration and login tested successfully)

# ✅ CRUD operations working
# (Jobs creation and listing tested successfully)
```

---

## 💡 Important Notes

1. **No external ML dependencies**: All ML packages removed. If you need ML features, integrate via OpenAI API using the `OPENAI_API_KEY` environment variable.

2. **MongoDB is required**: Application will not start without MongoDB connection. Ensure MongoDB service is running.

3. **CORS is comma-separated**: Format must be: `domain1,domain2,domain3` (no spaces, no quotes in the env var)

4. **Supervisor manages services**: Use `supervisorctl` commands to control backend/frontend/mongodb services.

5. **Port 8001 for backend**: Backend runs on port 8001 (not 8000). Frontend Vite proxy is configured for this.

---

## 🆘 Troubleshooting

### Backend won't start
```bash
# Check MongoDB is running
supervisorctl status mongodb

# Check backend logs
tail -f /var/log/supervisor/backend.out.log

# Restart backend
supervisorctl restart backend
```

### Frontend won't load
```bash
# Check if running on port 3000
curl http://localhost:3000

# Check frontend logs
tail -f /var/log/supervisor/frontend.out.log

# Restart frontend
supervisorctl restart frontend
```

### CORS errors
- Verify `CORS_ORIGINS` is comma-separated (no spaces)
- Check frontend domain is included in CORS_ORIGINS
- Restart backend after changing CORS_ORIGINS

---

**All changes are complete and tested. Ready for deployment!** 🚀
