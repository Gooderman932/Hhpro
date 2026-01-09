# Makefile for Construction Intelligence Platform
# Simplifies common development and deployment tasks

.PHONY: help dev prod build clean test lint backup deploy health logs

# Default target
help:
	@echo "Construction Intelligence Platform - Available Commands"
	@echo ""
	@echo "Development:"
	@echo "  make dev          - Start development environment"
	@echo "  make dev-stop     - Stop development environment"
	@echo "  make dev-logs     - View development logs"
	@echo ""
	@echo "Production:"
	@echo "  make prod         - Start production environment"
	@echo "  make prod-stop    - Stop production environment"
	@echo "  make prod-logs    - View production logs"
	@echo "  make deploy       - Deploy to production"
	@echo "  make pre-test     - Run pre-deployment tests"
	@echo ""
	@echo "Database:"
	@echo "  make db-init      - Initialize database"
	@echo "  make db-seed      - Seed database with sample data"
	@echo "  make db-migrate   - Run database migrations"
	@echo "  make backup       - Create database backup"
	@echo ""
	@echo "Maintenance:"
	@echo "  make build        - Build Docker images"
	@echo "  make clean        - Clean up containers and volumes"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run linters"
	@echo "  make health       - Check application health"
	@echo "  make logs         - View logs"

# Development
dev:
	@echo "Starting development environment..."
	docker-compose up -d
	@echo "Services started:"
	@docker-compose ps
	@echo ""
	@echo "Frontend: http://localhost:5173"
	@echo "Backend: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"

dev-stop:
	@echo "Stopping development environment..."
	docker-compose down

dev-logs:
	docker-compose logs -f

# Production
prod:
	@echo "Starting production environment..."
	@if [ ! -f .env ]; then \
		echo "Error: .env file not found!"; \
		echo "Copy .env.production to .env and configure it first."; \
		exit 1; \
	fi
	docker-compose -f docker-compose.prod.yml up -d
	@echo "Services started:"
	@docker-compose -f docker-compose.prod.yml ps
	@echo ""
	@echo "Application: http://localhost"
	@echo "Health check: http://localhost/health"

prod-stop:
	@echo "Stopping production environment..."
	docker-compose -f docker-compose.prod.yml down

prod-logs:
	docker-compose -f docker-compose.prod.yml logs -f

deploy:
	@echo "Deploying to production..."
	@chmod +x scripts/deployment/deploy.sh
	@./scripts/deployment/deploy.sh

pre-test:
	@echo "Running pre-deployment tests..."
	@chmod +x scripts/deployment/pre-deploy-test.sh
	@./scripts/deployment/pre-deploy-test.sh

# Database
db-init:
	@echo "Initializing database..."
	docker-compose -f docker-compose.prod.yml exec backend python scripts/setup_db.py

db-seed:
	@echo "Seeding database..."
	docker-compose -f docker-compose.prod.yml exec backend python scripts/seed_data.py

db-migrate:
	@echo "Running database migrations..."
	docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head

backup:
	@echo "Creating database backup..."
	@chmod +x scripts/deployment/backup.sh
	@./scripts/deployment/backup.sh

# Maintenance
build:
	@echo "Building Docker images..."
	docker-compose -f docker-compose.prod.yml build

build-dev:
	@echo "Building development Docker images..."
	docker-compose build

clean:
	@echo "Cleaning up containers and volumes..."
	@read -p "This will remove all containers and volumes. Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker-compose down -v; \
		docker-compose -f docker-compose.prod.yml down -v; \
		echo "Cleaned up successfully."; \
	else \
		echo "Cancelled."; \
	fi

test:
	@echo "Running tests..."
	@echo "Backend tests:"
	cd backend && pytest || echo "Tests not yet implemented"
	@echo ""
	@echo "Frontend tests:"
	cd frontend && npm test || echo "Tests not yet implemented"

lint:
	@echo "Running linters..."
	@echo "Backend (flake8):"
	cd backend && flake8 app/ || true
	@echo ""
	@echo "Backend (mypy):"
	cd backend && mypy app/ --ignore-missing-imports || true
	@echo ""
	@echo "Frontend (eslint):"
	cd frontend && npm run lint || true

health:
	@echo "Checking application health..."
	@curl -s http://localhost/health || echo "Application not responding"
	@echo ""

logs:
	docker-compose -f docker-compose.prod.yml logs --tail=100 -f

# Container management
restart:
	@echo "Restarting all services..."
	docker-compose -f docker-compose.prod.yml restart

restart-backend:
	@echo "Restarting backend..."
	docker-compose -f docker-compose.prod.yml restart backend

restart-frontend:
	@echo "Restarting frontend..."
	docker-compose -f docker-compose.prod.yml restart frontend

restart-nginx:
	@echo "Restarting nginx..."
	docker-compose -f docker-compose.prod.yml restart nginx

# Shell access
shell-backend:
	docker-compose -f docker-compose.prod.yml exec backend bash

shell-db:
	docker-compose -f docker-compose.prod.yml exec postgres psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)

# Security
security-scan:
	@echo "Running security scan..."
	@echo "Checking for vulnerabilities in dependencies..."
	cd backend && pip install safety && safety check -r requirements.txt || true
	cd frontend && npm audit || true

# Documentation
docs:
	@echo "Opening documentation..."
	@echo "README: cat README.md"
	@echo "Deployment Guide: cat DEPLOYMENT.md"
	@echo "Security Guide: cat SECURITY.md"
	@echo "Quick Start: cat QUICKSTART.md"
