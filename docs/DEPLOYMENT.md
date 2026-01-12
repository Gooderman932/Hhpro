# Deployment Guide

## Table of Contents
- [Architecture Overview](#architecture-overview)
- [Environment Setup](#environment-setup)
- [CI/CD Pipeline](#cicd-pipeline)
- [Manual Deployment](#manual-deployment)
- [Rollback Procedures](#rollback-procedures)
- [Troubleshooting](#troubleshooting)

## Architecture Overview

The Construction Intelligence Platform uses a containerized microservices architecture:

```
┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │
│    Frontend     │────▶│    Backend      │
│  (React/Nginx)  │     │  (FastAPI)      │
│                 │     │                 │
└─────────────────┘     └────────┬────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
               ┌────▼─────┐            ┌────▼────┐
               │PostgreSQL│            │  Redis  │
               │ Database │            │  Cache  │
               └──────────┘            └─────────┘
```

### Components
- **Frontend**: React SPA served by Nginx
- **Backend**: FastAPI REST API with Python 3.11
- **Database**: PostgreSQL 16 for persistent storage
- **Cache**: Redis for session management and caching
- **Registry**: GitHub Container Registry (ghcr.io)

## Environment Setup

### Prerequisites
- Docker & Docker Compose
- GitHub account with repository access
- Access to deployment environments (staging/production)

### GitHub Secrets Configuration

Required secrets in GitHub repository settings:

**Staging:**
- `DATABASE_URL_STAGING`: PostgreSQL connection string
- `SECRET_KEY_STAGING`: Application secret key
- `OPENAI_API_KEY`: OpenAI API key

**Production:**
- `DATABASE_URL_PRODUCTION`: PostgreSQL connection string
- `SECRET_KEY_PRODUCTION`: Application secret key
- `MONETIZATION_API_KEY`: Monetization service API key

See [GITHUB_SECRETS.md](./GITHUB_SECRETS.md) for detailed setup.

### Local Development

```bash
# Clone and setup
git clone https://github.com/your-org/construction-intel.git
cd construction-intel
cp .env.example .env

# Start services
make dev

# Access
# - Frontend: http://localhost:5173
# - Backend: http://localhost:8000
# - API Docs: http://localhost:8000/api/docs
```

## CI/CD Pipeline

### Workflows

1. **CI (ci.yml)**: Tests on every PR/push
2. **Deploy (deploy.yml)**: Staging (auto) / Production (manual)
3. **Migrations (migrations.yml)**: Auto database migrations
4. **Scheduled (scheduled-tasks.yml)**: Daily/weekly automation
5. **Security (security.yml)**: Weekly security scans

See `.github/workflows/` for implementation details.

## Manual Deployment

### Build Images
```bash
make build
```

### Deploy to Staging
```bash
git push origin main  # Auto-deploys to staging
```

### Deploy to Production
```bash
gh workflow run deploy.yml --field environment=production
# Then approve in GitHub Actions UI
```

### Database Migrations
```bash
make db-migrate              # Apply migrations
make db-migrate-create      # Create new migration
make db-downgrade           # Rollback last migration
```

## Rollback Procedures

### Application Rollback
```bash
# Redeploy previous version
export TAG=previous-sha
docker compose -f docker-compose.prod.yml up -d
```

### Database Rollback
```bash
cd backend && alembic downgrade -1

# Or restore from backup
make db-restore BACKUP_FILE=backups/backup_20250112.sql
```

## Troubleshooting

### Health Checks
```bash
make health-check
curl http://localhost:8000/health
```

### View Logs
```bash
make logs
make logs-backend
make logs-frontend
```

### Common Issues
- **Database connection**: Check `DATABASE_URL` and PostgreSQL status
- **Build failures**: Clear Docker cache with `docker builder prune -af`
- **Migration issues**: Check `alembic current` and `alembic history`

For detailed troubleshooting, see full documentation above.

## Additional Resources
- [Development Workflow](./DEVELOPMENT.md)
- [Automation Documentation](./AUTOMATION.md)
- [GitHub Secrets Setup](./GITHUB_SECRETS.md)
