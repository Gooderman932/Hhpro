# Developer Guide

Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Environment](#development-environment)
- [Running Tests](#running-tests)
- [Code Formatting and Linting](#code-formatting-and-linting)
- [Database Migrations](#database-migrations)
- [Pre-commit Hooks](#pre-commit-hooks)
- [Makefile Commands](#makefile-commands)
- [Development Workflow](#development-workflow)

## Getting Started

### Prerequisites

- **Docker & Docker Compose** (recommended) OR
- **Python 3.11+** and **Node.js 20+**
- **PostgreSQL 16** (if running locally without Docker)
- **Git**

### Initial Setup

#### Option 1: Using Docker (Recommended)

```bash
# 1. Clone repository
git clone https://github.com/Gooderman932/market-data.git
cd market-data

# 2. Create environment file
make setup
# Or manually: cp .env.example .env

# 3. Edit .env with your configuration
nano .env

# 4. Start development environment
make dev

# 5. Set up database (first time only)
docker-compose exec backend python ../scripts/setup_db.py
docker-compose exec backend python ../scripts/seed_data.py
```

#### Option 2: Local Development

```bash
# 1. Clone repository
git clone https://github.com/Gooderman932/market-data.git
cd market-data

# 2. Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Frontend setup
cd ../frontend
npm install

# 4. Set up PostgreSQL
# Install PostgreSQL 16 and create database
createdb construction_intel

# 5. Configure environment
export DATABASE_URL="postgresql://user:password@localhost:5432/construction_intel"
export SECRET_KEY="your-development-secret-key"

# 6. Run migrations
cd ../backend
alembic upgrade head

# 7. Seed data
python ../scripts/setup_db.py
python ../scripts/seed_data.py

# 8. Start services
# Terminal 1 - Backend
cd backend
uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### Accessing the Application

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Alternative API Docs: http://localhost:8000/redoc

### Default Credentials

After seeding the database:
- Email: demo@example.com
- Password: demo123

## Development Environment

### Using Makefile Commands

The repository includes a comprehensive Makefile for common development tasks.

```bash
# Show all available commands
make help

# Start development environment
make dev

# View logs
make dev-logs

# Stop environment
make dev-stop
```

### Environment Variables

Development `.env` file:
```bash
APP_NAME="Construction Intelligence Platform"
DEBUG=True
SECRET_KEY=dev-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/construction_intel
OPENAI_API_KEY=sk-your-key-optional
```

## Running Tests

### Backend Tests

```bash
# Run all backend tests
make test-backend

# Run with coverage report
make test-coverage

# Run in watch mode
make test-watch

# Run specific test file
cd backend
pytest tests/test_main.py -v

# Run tests matching pattern
pytest tests/ -k "test_health" -v
```

### Frontend Tests

```bash
# Run frontend build test
make test-frontend

# Type checking
cd frontend
npx tsc --noEmit

# Lint
npm run lint
```

### Running All Tests

```bash
# Run all tests (backend + frontend)
make test

# Run CI checks locally
make ci
```

## Code Formatting and Linting

### Backend

```bash
# Run all backend linters
make lint-backend

# Format code
make format-backend

# Individual tools
cd backend
flake8 app/
black app/
isort app/
mypy app/ --ignore-missing-imports
```

### Frontend

```bash
# Run frontend linter
make lint-frontend

# Auto-fix issues
make format-frontend

# Or directly
cd frontend
npm run lint
npm run lint -- --fix
```

### Run All

```bash
# Lint everything
make lint

# Format everything
make format
```

## Database Migrations

### Creating Migrations

```bash
# Using Makefile
make migrate-create msg="add user table"

# Or with docker-compose
docker-compose exec backend alembic revision --autogenerate -m "add user table"

# Or locally
cd backend
alembic revision --autogenerate -m "add user table"
```

### Running Migrations

```bash
# Apply all pending migrations
make migrate

# Or directly
docker-compose exec backend alembic upgrade head
```

### Migration Commands

```bash
# View migration history
make migrate-history

# Show current revision
make migrate-current

# Rollback last migration
make migrate-rollback

# Rollback to specific revision
docker-compose exec backend alembic downgrade <revision>
```

### Database Management

```bash
# Reset database (WARNING: destroys all data!)
make db-reset

# Open database shell
make db-shell

# Create backup
make backup
```

## Pre-commit Hooks

### Installation

```bash
# Install pre-commit hooks
make install-hooks

# Or manually
pip install pre-commit
pre-commit install
```

### Usage

```bash
# Hooks run automatically on git commit

# Run manually on all files
pre-commit run --all-files

# Run specific hook
pre-commit run black --all-files

# Skip hooks (not recommended)
git commit --no-verify
```

### Configured Hooks

- **Python**: black, isort, flake8, mypy, bandit
- **General**: trailing whitespace, EOF fixer, YAML/JSON checks
- **Security**: detect-secrets
- **Docker**: hadolint

## Makefile Commands

### Development

```bash
make dev              # Start development environment
make dev-logs         # Show logs
make dev-stop         # Stop environment
make dev-restart      # Restart environment
make setup            # Initial project setup
```

### Testing

```bash
make test             # Run all tests
make test-backend     # Run backend tests
make test-frontend    # Run frontend tests
make test-watch       # Run tests in watch mode
make test-coverage    # Generate coverage report
```

### Code Quality

```bash
make lint             # Run all linters
make lint-backend     # Run backend linters
make lint-frontend    # Run frontend linters
make format           # Format all code
make format-backend   # Format backend code
make format-frontend  # Format frontend code
make type-check       # Run type checking
```

### Database

```bash
make migrate          # Run migrations
make migrate-create   # Create new migration
make migrate-rollback # Rollback last migration
make migrate-history  # Show migration history
make migrate-current  # Show current migration
make db-reset         # Reset database
make db-shell         # Open database shell
```

### Docker

```bash
make build            # Build Docker images
make build-prod       # Build production images
make up               # Start all services
make down             # Stop all services
make logs             # Show logs
make logs-backend     # Show backend logs
make logs-frontend    # Show frontend logs
make ps               # Show running containers
make shell-backend    # Open backend shell
make shell-frontend   # Open frontend shell
```

### CI/CD

```bash
make ci               # Run CI checks locally
make security-scan    # Run security scans
```

### Utilities

```bash
make clean            # Clean up caches
make install-hooks    # Install pre-commit hooks
make backup           # Create database backup
make health           # Check service health
make update-deps      # Update dependencies
```

## Development Workflow

### Standard Workflow

1. **Create a feature branch**
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. **Make your changes**
   - Write code
   - Add tests
   - Update documentation

3. **Run tests and linting**
   ```bash
   make lint
   make test
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add new feature"
   # Pre-commit hooks run automatically
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/my-new-feature
   # Create PR on GitHub
   ```

### Code Review Checklist

- [ ] Tests added and passing
- [ ] Code formatted with black/eslint
- [ ] Type hints added (Python)
- [ ] Documentation updated
- [ ] No secrets committed
- [ ] CI checks passing
- [ ] Security scans clean

### Best Practices

1. **Write tests**: Add tests for new features
2. **Keep commits small**: Make focused, atomic commits
3. **Follow conventions**: Use consistent naming and style
4. **Document changes**: Update docs when needed
5. **Security first**: Never commit secrets
6. **Review before push**: Run `make ci` locally

## Troubleshooting

### Docker Issues

```bash
# Rebuild containers
docker-compose down
docker-compose build
docker-compose up -d

# Clean Docker cache
docker system prune -a
```

### Database Issues

```bash
# Reset database
make db-reset

# Check database connection
make db-shell
```

### Port Conflicts

```bash
# Check what's using a port
lsof -i :8000
lsof -i :5173

# Change ports in docker-compose.yml or .env
```

### Permission Issues

```bash
# Fix file permissions
sudo chown -R $USER:$USER .
```

## Additional Resources

- [CI/CD Documentation](./CICD.md)
- [Deployment Guide](./DEPLOYMENT.md)
- [API Documentation](http://localhost:8000/docs)
- [GitHub Secrets](../.github/SECRETS.md)

## Need Help?

- Check logs: `make dev-logs`
- Review documentation in `docs/`
- Check GitHub Issues
- Contact the team

---

**Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.**
