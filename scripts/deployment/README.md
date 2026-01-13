# Deployment Scripts

This directory contains production deployment and maintenance scripts for the Construction Intelligence Platform.

## 📜 Scripts Overview

### 🚀 deploy.sh
**Purpose:** Main production deployment script

**What it does:**
- Validates environment configuration
- Pulls latest code from git
- Builds Docker images
- Stops old containers gracefully
- Starts new containers
- Waits for services to become healthy
- Runs database migrations
- Verifies deployment success

**Usage:**
```bash
./scripts/deployment/deploy.sh
```

**Or via Makefile:**
```bash
make deploy
```

**Prerequisites:**
- `.env` file configured
- Docker and Docker Compose installed
- Git repository initialized

---

### 💾 backup.sh
**Purpose:** Automated database backup

**What it does:**
- Creates compressed PostgreSQL dump
- Timestamps backup file
- Stores in `backups/` directory
- Cleans up old backups (30 days retention by default)
- Shows backup size and recent backups

**Usage:**
```bash
./scripts/deployment/backup.sh
```

**Or via Makefile:**
```bash
make backup
```

**Configuration:**
- Backup directory: `./backups`
- Retention: 30 days (configurable in script)
- Format: `backup_YYYYMMDD_HHMMSS.sql.gz`

**Automation:**
```bash
# Set up daily backups at 2 AM
crontab -e
# Add: 0 2 * * * cd /path/to/market-data && ./scripts/deployment/backup.sh
```

---

### 🏥 health-check.sh
**Purpose:** Comprehensive health monitoring

**What it checks:**
- Container status (postgres, redis, backend, frontend, nginx)
- Endpoint health (main app, backend API)
- System resources (disk space, memory)
- Overall system health

**Usage:**
```bash
./scripts/deployment/health-check.sh
```

**Or via Makefile:**
```bash
make health
```

**Exit Codes:**
- `0` - All systems healthy
- `1` - One or more issues detected

**Automation:**
```bash
# Monitor health every 5 minutes
crontab -e
# Add: */5 * * * * cd /path/to/market-data && ./scripts/deployment/health-check.sh >> /var/log/health-check.log 2>&1
```

---

### 🧪 pre-deploy-test.sh
**Purpose:** Pre-deployment validation

**What it checks:**
- Prerequisites (Docker, Git, Curl, OpenSSL)
- Configuration (.env file, required variables)
- Docker files (docker-compose, Dockerfiles)
- Deployment scripts (existence and executability)
- Documentation completeness
- Security issues (secrets in git)
- SSL certificates (if present)
- Docker Compose configuration validity

**Usage:**
```bash
./scripts/deployment/pre-deploy-test.sh
```

**Or via Makefile:**
```bash
make pre-test
```

**When to use:**
- Before first deployment
- After configuration changes
- Before major updates
- As part of CI/CD pipeline

**Exit Codes:**
- `0` - All checks passed, ready to deploy
- `1` - Issues found, fix before deploying

---

## 🔄 Typical Deployment Workflow

### Initial Deployment

```bash
# 1. Run pre-deployment tests
make pre-test

# 2. Deploy application
make deploy

# 3. Initialize database
make db-init

# 4. Verify health
make health

# 5. Set up automated backups
crontab -e
# Add: 0 2 * * * cd /path/to/market-data && make backup
```

### Regular Updates

```bash
# 1. Create backup
make backup

# 2. Run pre-deployment tests
make pre-test

# 3. Deploy update
make deploy

# 4. Check health
make health
```

### Emergency Rollback

```bash
# 1. Stop current version
docker-compose -f docker-compose.prod.yml down

# 2. Checkout previous version
git checkout <previous-commit>

# 3. Deploy
make deploy

# 4. Restore database if needed
# See backup.sh for restoration steps
```

## 📊 Monitoring Setup

### Daily Health Checks

```bash
# Add to crontab
crontab -e

# Run health check every 5 minutes
*/5 * * * * cd /path/to/market-data && ./scripts/deployment/health-check.sh >> /var/log/health-check.log 2>&1

# Send alert on failure
*/5 * * * * cd /path/to/market-data && ./scripts/deployment/health-check.sh || echo "Health check failed" | mail -s "Alert" admin@example.com
```

### Automated Backups

```bash
# Daily backup at 2 AM
0 2 * * * cd /path/to/market-data && ./scripts/deployment/backup.sh

# Weekly backup with notification
0 2 * * 0 cd /path/to/market-data && ./scripts/deployment/backup.sh && echo "Weekly backup completed" | mail -s "Backup" admin@example.com
```

## 🔧 Script Configuration

### Environment Variables

Scripts use environment variables from `.env` file:

```bash
# Required
POSTGRES_USER=buildintel_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=construction_intel
SECRET_KEY=your_secret_key

# Optional
BACKUP_RETENTION_DAYS=30
LOG_LEVEL=INFO
```

### Customization

To modify script behavior, edit the scripts directly:

**backup.sh:**
- `RETENTION_DAYS` - Days to keep backups (default: 30)
- `BACKUP_DIR` - Backup location (default: ./backups)

**health-check.sh:**
- `MAX_RETRIES` - Number of retries for endpoint checks (default: 3)
- `RETRY_DELAY` - Seconds between retries (default: 5)

**deploy.sh:**
- Deployment steps can be customized based on your workflow

## 🆘 Troubleshooting

### deploy.sh Issues

**Problem:** "Error: .env file not found"
```bash
# Solution
cp .env.production .env
nano .env  # Configure values
```

**Problem:** "Error: SECRET_KEY not configured"
```bash
# Solution
openssl rand -hex 32 > .tmp
nano .env  # Add the generated key
```

### backup.sh Issues

**Problem:** Permission denied
```bash
# Solution
chmod +x scripts/deployment/backup.sh
sudo chown $USER:$USER backups/
```

**Problem:** Backup fails
```bash
# Check if database is accessible
docker-compose -f docker-compose.prod.yml exec postgres pg_isready
```

### health-check.sh Issues

**Problem:** All checks failing
```bash
# Check if services are running
docker-compose -f docker-compose.prod.yml ps

# Check logs
docker-compose -f docker-compose.prod.yml logs
```

## 📚 Related Documentation

- **Quick Deploy**: `../QUICK_DEPLOY.md` - 30-minute setup
- **Full Deployment**: `../DEPLOYMENT.md` - Complete guide
- **Security**: `../SECURITY.md` - Security hardening
- **Checklist**: `../PRODUCTION_CHECKLIST.md` - Pre-deployment verification

## 🔐 Security Notes

- Scripts require appropriate file permissions (755)
- Never commit `.env` file or backups to git
- Store backups in secure location
- Encrypt backups if they contain sensitive data
- Rotate credentials regularly
- Review logs for security issues

## 📝 Maintenance

### Weekly Tasks
- Review backup logs
- Check disk space in backup directory
- Verify health check logs

### Monthly Tasks
- Test backup restoration
- Review and update scripts
- Check for script updates in repository
- Audit deployment logs

---

**Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.**

For support, see main repository documentation or contact your system administrator.
