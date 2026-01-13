# CI/CD Documentation

Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.

## Overview

This document describes the CI/CD pipeline for the Construction Intelligence Platform. The pipeline is built using GitHub Actions and provides automated testing, security scanning, building, and deployment capabilities.

## Workflows

### 1. CI Pipeline (`ci.yml` and `ci-cd.yml`)

**Purpose**: Validates code quality and runs tests

**Triggers**: Push to any branch, pull requests

**Key Features**:
- Backend: flake8, black, mypy, pytest with coverage
- Frontend: TypeScript compilation, ESLint, build test  
- PostgreSQL service container for integration tests
- Coverage report artifacts

### 2. Security Scanning (`security.yml`)

**Purpose**: Comprehensive security analysis

**Triggers**: Push to main/develop, PRs, weekly schedule, manual

**Scans**:
- CodeQL SAST (Python & JavaScript)
- Python: Bandit, Safety, pip-audit
- Node.js: npm audit
- Docker: Trivy vulnerability scanning

### 3. Docker Build & Push (`docker.yml`)

**Purpose**: Build and publish Docker images

**Triggers**: Push to main/develop, version tags, manual

**Features**:
- Multi-stage builds for backend and frontend
- SBOM generation
- Image vulnerability scanning
- Push to GitHub Container Registry

### 4. Database Migrations (`migrations.yml`)

**Purpose**: Apply database schema changes

**Triggers**: Manual dispatch only

**Options**:
- Dry run validation
- Upgrade/downgrade migrations
- Environment selection (staging/production)

### 5. Deployment (`deploy.yml`)

**Purpose**: Deploy to staging or production

**Triggers**: Manual dispatch only

**Features**:
- Pre-deployment checks
- Health checks
- Rollback on failure
- Environment-specific configurations

### 6. Scheduled Automation (`scheduled-automation.yml`)

**Purpose**: Run platform automation tasks

**Triggers**: Daily at 2 AM UTC, manual dispatch

**Executes**: `tools/automated_platform.py` for platform management

## Quick Reference

### Manual Workflow Triggers

```bash
# Using GitHub CLI
gh workflow run <workflow-name> -f <input>=<value>

# Examples:
gh workflow run deploy.yml -f environment=staging
gh workflow run migrations.yml -f environment=staging -f dry_run=true
```

### Viewing Logs

1. Go to Actions tab
2. Click on workflow run
3. Click on job name
4. Expand steps to see details

### Common Commands

```bash
# List workflows
gh workflow list

# View run details
gh run view <run-id>

# Download artifacts
gh run download <run-id>

# Cancel a run
gh run cancel <run-id>
```

## Required Secrets

See [.github/SECRETS.md](../.github/SECRETS.md) for complete list.

**Essential**:
- `SECRET_KEY` - Application secret
- `DATABASE_URL_STAGING` - Staging database
- `DATABASE_URL_PRODUCTION` - Production database
- `GITHUB_TOKEN` - Automatically provided

## Best Practices

1. **Always run dry-run first** for migrations
2. **Use staging environment** before production
3. **Monitor workflow logs** for issues
4. **Rotate secrets regularly**
5. **Review security scan results** in Security tab

## Troubleshooting

- **Secret not found**: Check repository settings > Secrets
- **Tests failing**: Review logs, check environment variables
- **Docker build fails**: Check Dockerfile syntax and paths
- **Deployment fails**: Verify health checks and rollback

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Deployment guide
- [DEVELOPER.md](./DEVELOPER.md) - Developer guide

---

For detailed workflow documentation and advanced usage, see the full CI/CD guide above.

**Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.**
