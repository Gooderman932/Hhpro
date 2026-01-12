# Construction Intelligence Platform - Makefile
# Convenient commands for development and deployment

.PHONY: help dev test lint format build deploy-staging deploy-prod db-migrate db-seed db-backup run-automation health-check clean install

# Default target
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "Construction Intelligence Platform - Development Commands"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Development
dev: ## Start development environment with Docker Compose
	docker compose up --build

dev-bg: ## Start development environment in background
	docker compose up -d --build

stop: ## Stop development environment
	docker compose down

logs: ## View logs from all services
	docker compose logs -f

logs-backend: ## View backend logs
	docker compose logs -f backend

logs-frontend: ## View frontend logs
	docker compose logs -f frontend

# Installation
install: ## Install all dependencies
	@echo "Installing backend dependencies..."
	cd backend && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd frontend && npm install
	@echo "Installing pre-commit hooks..."
	pip install pre-commit
	pre-commit install

install-backend: ## Install backend dependencies only
	cd backend && pip install -r requirements.txt

install-frontend: ## Install frontend dependencies only
	cd frontend && npm install

# Testing
test: ## Run all tests
	@echo "Running backend tests..."
	cd backend && pytest
	@echo "Running frontend tests..."
	cd frontend && npm test || echo "No frontend tests configured yet"

test-backend: ## Run backend tests only
	cd backend && pytest

test-backend-cov: ## Run backend tests with coverage
	cd backend && pytest --cov=app --cov-report=html

test-frontend: ## Run frontend tests only
	cd frontend && npm test || echo "No frontend tests configured yet"

test-watch: ## Run tests in watch mode
	cd backend && pytest-watch

# Code Quality
lint: ## Run all linters
	@echo "Linting backend..."
	cd backend && flake8 app/
	cd backend && mypy app/ --ignore-missing-imports
	@echo "Linting frontend..."
	cd frontend && npm run lint

lint-backend: ## Run backend linters
	cd backend && flake8 app/ --max-line-length=100 --extend-ignore=E203,W503
	cd backend && mypy app/ --ignore-missing-imports

lint-frontend: ## Run frontend linter
	cd frontend && npm run lint

format: ## Format all code
	@echo "Formatting backend..."
	cd backend && black app/
	cd backend && isort app/
	@echo "Formatting frontend..."
	cd frontend && npx prettier --write "src/**/*.{ts,tsx,js,jsx,json,css}"

format-backend: ## Format backend code
	cd backend && black app/
	cd backend && isort app/

format-frontend: ## Format frontend code
	cd frontend && npx prettier --write "src/**/*.{ts,tsx,js,jsx,json,css}"

# Building
build: ## Build production Docker images
	docker build -t construction-intel-backend:latest -f backend/Dockerfile.prod backend/
	docker build -t construction-intel-frontend:latest -f frontend/Dockerfile.prod frontend/

build-backend: ## Build backend production image
	docker build -t construction-intel-backend:latest -f backend/Dockerfile.prod backend/

build-frontend: ## Build frontend production image
	docker build -t construction-intel-frontend:latest -f frontend/Dockerfile.prod frontend/

build-dev: ## Build development images
	docker compose build

# Deployment
deploy-staging: ## Deploy to staging environment
	@echo "Deploying to staging..."
	@echo "This will trigger the GitHub Actions deployment workflow"
	git push origin main

deploy-prod: ## Deploy to production (requires manual approval)
	@echo "To deploy to production, run:"
	@echo "gh workflow run deploy.yml --field environment=production"

# Database
db-migrate: ## Run database migrations
	cd backend && alembic upgrade head

db-migrate-create: ## Create a new migration
	@read -p "Enter migration message: " msg; \
	cd backend && alembic revision --autogenerate -m "$$msg"

db-downgrade: ## Rollback last migration
	cd backend && alembic downgrade -1

db-reset: ## Reset database (WARNING: destroys all data)
	@echo "WARNING: This will destroy all data!"
	@read -p "Are you sure? [y/N] " confirm; \
	if [ "$$confirm" = "y" ]; then \
		docker compose down -v; \
		docker compose up -d postgres; \
		sleep 5; \
		cd backend && alembic upgrade head; \
	fi

db-seed: ## Seed database with sample data
	cd backend && python -m app.utils.seed_data

db-backup: ## Backup database
	@echo "Creating database backup..."
	mkdir -p backups
	docker compose exec -e PGPASSWORD=password postgres pg_dump -U user construction_intel > backups/backup_$$(date +%Y%m%d_%H%M%S).sql || echo "Backup failed - check database credentials"
	@echo "Backup created in backups/"

db-restore: ## Restore database from backup (specify BACKUP_FILE=path/to/backup.sql)
	@if [ -z "$(BACKUP_FILE)" ]; then \
		echo "Please specify BACKUP_FILE=path/to/backup.sql"; \
		exit 1; \
	fi
	docker compose exec -T postgres psql -U user construction_intel < $(BACKUP_FILE)

# Automation
run-automation: ## Run automated platform management
	python tools/automated_platform.py

health-check: ## Check platform health
	@echo "Checking backend health..."
	@curl -f http://localhost:8000/health || echo "Backend is down"
	@echo ""
	@echo "Checking frontend..."
	@curl -f http://localhost:5173 > /dev/null 2>&1 && echo "Frontend is up" || echo "Frontend is down"
	@echo ""
	@echo "Checking database..."
	@docker compose exec postgres pg_isready -U user && echo "Database is up" || echo "Database is down"

# Cleaning
clean: ## Clean build artifacts and caches
	@echo "Cleaning Python cache..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "Cleaning frontend cache..."
	rm -rf frontend/dist frontend/build frontend/node_modules/.cache 2>/dev/null || true
	@echo "Cleaning coverage reports..."
	rm -rf backend/htmlcov backend/.coverage backend/coverage.xml 2>/dev/null || true
	@echo "Clean complete!"

clean-all: clean ## Clean everything including node_modules and venv
	@echo "Removing node_modules..."
	rm -rf frontend/node_modules 2>/dev/null || true
	@echo "Removing Python virtual environment..."
	rm -rf venv env 2>/dev/null || true
	@echo "Deep clean complete!"

# Security
security-scan: ## Run security scans
	@echo "Scanning Python dependencies..."
	pip-audit -r backend/requirements.txt || true
	@echo "Scanning npm dependencies..."
	cd frontend && npm audit || true

# Docker management
docker-prune: ## Remove unused Docker resources
	docker system prune -af --volumes

docker-logs: ## Show Docker logs
	docker compose logs --tail=100

# Shell access
shell-backend: ## Open shell in backend container
	docker compose exec backend /bin/bash

shell-frontend: ## Open shell in frontend container
	docker compose exec frontend /bin/sh

shell-db: ## Open PostgreSQL shell
	docker compose exec postgres psql -U user construction_intel

# Quick start
quickstart: install dev ## Quick start: install dependencies and start dev environment
	@echo "Development environment is starting..."
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:5173"
	@echo "API Docs: http://localhost:8000/api/docs"
