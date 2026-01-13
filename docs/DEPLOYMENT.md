# Deployment Guide

Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.

## Overview

This guide covers deploying the Construction Intelligence Platform to staging and production environments.

## Prerequisites

- Docker and Docker Compose installed
- Access to GitHub Container Registry
- Required secrets configured (see `.github/SECRETS.md`)
- Database instances provisioned

## Deployment Environments

### Staging
- **Purpose**: Testing and QA
- **URL**: https://staging.construction-intel.com (configure as needed)
- **Branch**: `develop`
- **Auto-deploy**: Yes (on push to develop)

### Production
- **Purpose**: Live customer-facing environment
- **URL**: https://construction-intel.com (configure as needed)
- **Branch**: `main`
- **Auto-deploy**: No (manual approval required)

## Deployment Methods

### Method 1: GitHub Actions (Recommended)

#### Deploy to Staging

```bash
# Automatic on push to develop
git push origin develop

# Or manually trigger
gh workflow run deploy.yml -f environment=staging -f image_tag=develop
```

#### Deploy to Production

```bash
# 1. Create a release
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# 2. Manually trigger deployment (requires approval)
gh workflow run deploy.yml -f environment=production -f image_tag=v1.0.0 -f run_migrations=true
```

### Method 2: Using Helper Script

```bash
# Deploy to staging
./scripts/deploy.sh staging latest false

# Deploy to production (with migrations)
./scripts/deploy.sh production latest true
```

### Method 3: Manual Docker Compose

```bash
# 1. Set environment variables
export IMAGE_TAG=v1.0.0
export SECRET_KEY=your-secret-key
export DATABASE_URL=postgresql://...
export POSTGRES_PASSWORD=...
export REDIS_PASSWORD=...

# 2. Pull images
docker-compose -f docker-compose.prod.yml pull

# 3. Run migrations (if needed)
docker-compose -f docker-compose.prod.yml run --rm backend alembic upgrade head

# 4. Start services
docker-compose -f docker-compose.prod.yml up -d

# 5. Check health
./scripts/health_check.sh
```

## Database Migrations

### Running Migrations

**Via GitHub Actions** (Recommended):
```bash
# Dry run first
gh workflow run migrations.yml \
  -f environment=staging \
  -f action=upgrade \
  -f dry_run=true

# Apply migrations
gh workflow run migrations.yml \
  -f environment=staging \
  -f action=upgrade \
  -f dry_run=false \
  -f revision=head
```

**Via Docker Compose**:
```bash
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

### Creating Migrations

```bash
# Using Makefile
make migrate-create msg="add user table"

# Or directly
docker-compose exec backend alembic revision --autogenerate -m "add user table"
```

### Rolling Back Migrations

```bash
# Rollback one revision
gh workflow run migrations.yml \
  -f environment=staging \
  -f action=downgrade \
  -f revision=-1 \
  -f dry_run=false
```

## Post-Deployment

### Health Checks

```bash
# Run health check script
./scripts/health_check.sh

# Or manually check endpoints
curl https://your-domain.com/health
curl https://your-domain.com/
```

### Verify Deployment

1. Check service status:
   ```bash
   docker-compose -f docker-compose.prod.yml ps
   ```

2. View logs:
   ```bash
   docker-compose -f docker-compose.prod.yml logs -f
   ```

3. Test API:
   ```bash
   curl https://your-domain.com/api/docs
   ```

4. Test frontend:
   ```bash
   curl https://your-domain.com/
   ```

## Rollback Procedures

### Automatic Rollback

The deployment workflow includes automatic rollback on health check failure.

### Manual Rollback

**Using GitHub Actions**:
```bash
# Deploy previous version
gh workflow run deploy.yml \
  -f environment=production \
  -f image_tag=v1.0.0
```

**Using Docker Compose**:
```bash
# 1. Stop current services
docker-compose -f docker-compose.prod.yml down

# 2. Set previous image tag
export IMAGE_TAG=v1.0.0

# 3. Start services
docker-compose -f docker-compose.prod.yml up -d
```

**Database Rollback**:
```bash
# Rollback one migration
docker-compose -f docker-compose.prod.yml exec backend alembic downgrade -1

# Or use GitHub Actions
gh workflow run migrations.yml \
  -f environment=production \
  -f action=downgrade \
  -f revision=-1
```

## Monitoring

### Logs

```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f backend

# Last 100 lines
docker-compose -f docker-compose.prod.yml logs --tail=100 backend

### Metrics

Access Prometheus metrics (if configured):
- http://your-domain.com/metrics

### Health Status

- Backend: http://your-domain.com/health
- Frontend: http://your-domain.com/

## Backup & Recovery

### Creating Backups

```bash
# Using backup script
./scripts/backup_database.sh

# Manual backup
docker-compose -f docker-compose.prod.yml exec postgres \
  pg_dump -U user construction_intel | gzip > backup.sql.gz
```

### Restoring from Backup

```bash
# Stop services
docker-compose -f docker-compose.prod.yml down

# Restore database
gunzip < backup.sql.gz | docker-compose -f docker-compose.prod.yml exec -T postgres \
```
  psql -U user construction_intel

# Start services
docker-compose -f docker-compose.prod.yml up -d
```

## Troubleshooting

### Common Issues

**Services not starting**:
```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs

# Check service status
docker-compose -f docker-compose.prod.yml ps
```

**Database connection issues**:
```bash
# Test database connection
docker-compose -f docker-compose.prod.yml exec postgres \
  psql -U user -c '\l'
```

**Image pull failures**:
```bash
# Login to registry
docker login ghcr.io -u $GITHUB_ACTOR -p $GITHUB_TOKEN

# Pull manually
docker pull ghcr.io/gooderman932/market-data-backend:latest
```

### Getting Help

1. Check logs first
2. Review health check output
3. Verify environment variables
4. Check GitHub Actions workflow logs
5. Contact platform team

## Security Considerations

1. **Secrets Management**: Never commit secrets to code
2. **HTTPS**: Always use HTTPS in production
3. **Firewall**: Restrict database access to backend only
4. **Updates**: Keep dependencies updated
5. **Backups**: Regular automated backups
6. **Monitoring**: Set up alerts for failures

## Best Practices

1. **Test in Staging First**: Always deploy to staging before production
2. **Use Tags**: Tag releases with semantic versioning
3. **Run Migrations Separately**: Run migrations before deploying code changes
4. **Monitor Deployments**: Watch logs during deployment
5. **Have a Rollback Plan**: Know how to quickly rollback
6. **Document Changes**: Update CHANGELOG.md for each release
7. **Health Checks**: Always verify health after deployment

## Additional Resources

- [CI/CD Documentation](./CICD.md)
- [Developer Guide](./DEVELOPER.md)
- [GitHub Secrets Configuration](../.github/SECRETS.md)
- [Docker Documentation](https://docs.docker.com/)

---

**Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.**
