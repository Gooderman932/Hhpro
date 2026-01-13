# Construction Intelligence Platform - Makefile
#
# Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.
# PROPRIETARY AND CONFIDENTIAL - Unauthorized use prohibited.

.PHONY: help dev test lint format migrate deploy clean

# Default target
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

##@ General

help: ## Display this help message
	@echo "$(BLUE)Construction Intelligence Platform$(NC)"
	@echo "$(BLUE)Available commands:$(NC)"
	@awk 'BEGIN {FS = ":.*##"; printf "\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2 } /^##@/ { printf "\n$(YELLOW)%s$(NC)\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Development

dev: ## Start development environment
	@echo "$(BLUE)Starting development environment...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✓ Services started$(NC)"
	@echo "Frontend: http://localhost:5173"
	@echo "Backend: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"

dev-logs: ## Show development logs
	docker-compose logs -f

dev-stop: ## Stop development environment
	@echo "$(BLUE)Stopping development environment...$(NC)"
	docker-compose down
	@echo "$(GREEN)✓ Services stopped$(NC)"

dev-restart: dev-stop dev ## Restart development environment

setup: ## Initial project setup
	@echo "$(BLUE)Setting up project...$(NC)"
	@if [ ! -f .env ]; then \
		echo "Creating .env file from .env.example..."; \
		cp .env.example .env; \
	fi
	@echo "$(GREEN)✓ Project setup complete$(NC)"
	@echo "Update .env with your configuration and run 'make dev'"

##@ Testing

test: test-backend test-frontend ## Run all tests

test-backend: ## Run backend tests
	@echo "$(BLUE)Running backend tests...$(NC)"
	cd backend && pytest tests/ -v --cov=app --cov-report=term

test-frontend: ## Run frontend tests
	@echo "$(BLUE)Running frontend build test...$(NC)"
	cd frontend && npm run build

test-watch: ## Run backend tests in watch mode
	cd backend && pytest tests/ -v --cov=app -f

test-coverage: ## Generate test coverage report
	@echo "$(BLUE)Generating coverage report...$(NC)"
	cd backend && pytest tests/ -v --cov=app --cov-report=html --cov-report=term
	@echo "$(GREEN)✓ Coverage report generated in backend/htmlcov/$(NC)"

##@ Code Quality

lint: lint-backend lint-frontend ## Run all linters

lint-backend: ## Run backend linters
	@echo "$(BLUE)Running backend linters...$(NC)"
	cd backend && flake8 app/ --count --select=E9,F63,F7,F82 --show-source --statistics
	cd backend && flake8 app/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	cd backend && mypy app/ --ignore-missing-imports || true
	@echo "$(GREEN)✓ Backend linting complete$(NC)"

lint-frontend: ## Run frontend linter
	@echo "$(BLUE)Running frontend linter...$(NC)"
	cd frontend && npm run lint
	@echo "$(GREEN)✓ Frontend linting complete$(NC)"

format: format-backend format-frontend ## Format all code

format-backend: ## Format backend code
	@echo "$(BLUE)Formatting backend code...$(NC)"
	cd backend && black app/
	cd backend && isort app/
	@echo "$(GREEN)✓ Backend code formatted$(NC)"

format-frontend: ## Format frontend code
	@echo "$(BLUE)Formatting frontend code...$(NC)"
	cd frontend && npm run lint -- --fix || true
	@echo "$(GREEN)✓ Frontend code formatted$(NC)"

type-check: ## Run type checking
	@echo "$(BLUE)Running type checks...$(NC)"
	cd backend && mypy app/ --ignore-missing-imports
	cd frontend && npx tsc --noEmit

##@ Database

migrate: ## Run database migrations
	@echo "$(BLUE)Running database migrations...$(NC)"
	docker-compose exec backend alembic upgrade head
	@echo "$(GREEN)✓ Migrations complete$(NC)"

migrate-create: ## Create new migration (usage: make migrate-create msg="description")
	@if [ -z "$(msg)" ]; then \
		echo "$(RED)Error: Please provide a message$(NC)"; \
		echo "Usage: make migrate-create msg=\"your migration message\""; \
		exit 1; \
	fi
	@echo "$(BLUE)Creating migration: $(msg)$(NC)"
	docker-compose exec backend alembic revision --autogenerate -m "$(msg)"
	@echo "$(GREEN)✓ Migration created$(NC)"

migrate-rollback: ## Rollback last migration
	@echo "$(YELLOW)Rolling back last migration...$(NC)"
	docker-compose exec backend alembic downgrade -1
	@echo "$(GREEN)✓ Rollback complete$(NC)"

migrate-history: ## Show migration history
	docker-compose exec backend alembic history

migrate-current: ## Show current migration
	docker-compose exec backend alembic current

db-reset: ## Reset database (WARNING: destroys all data)
	@echo "$(RED)⚠️  WARNING: This will destroy all data!$(NC)"
	@read -p "Are you sure? (yes/no): " confirm; \
	if [ "$$confirm" = "yes" ]; then \
		docker-compose down -v; \
		docker-compose up -d postgres; \
		sleep 5; \
		docker-compose up -d backend; \
		sleep 5; \
		docker-compose exec backend python /app/../scripts/setup_db.py; \
		echo "$(GREEN)✓ Database reset complete$(NC)"; \
	else \
		echo "$(YELLOW)Cancelled$(NC)"; \
	fi

db-shell: ## Open database shell
	docker-compose exec postgres psql -U user -d construction_intel

##@ Docker

build: ## Build all Docker images
	@echo "$(BLUE)Building Docker images...$(NC)"
	docker-compose build
	@echo "$(GREEN)✓ Images built$(NC)"

build-prod: ## Build production Docker images
	@echo "$(BLUE)Building production images...$(NC)"
	docker-compose -f docker-compose.prod.yml build
	@echo "$(GREEN)✓ Production images built$(NC)"

up: ## Start all services
	docker-compose up -d

down: ## Stop all services
	docker-compose down

logs: ## Show logs from all services
	docker-compose logs -f

logs-backend: ## Show backend logs
	docker-compose logs -f backend

logs-frontend: ## Show frontend logs
	docker-compose logs -f frontend

logs-db: ## Show database logs
	docker-compose logs -f postgres

ps: ## Show running containers
	docker-compose ps

shell-backend: ## Open backend shell
	docker-compose exec backend /bin/bash

shell-frontend: ## Open frontend shell
	docker-compose exec frontend /bin/sh

##@ CI/CD

ci: lint test ## Run CI checks locally
	@echo "$(GREEN)✓ All CI checks passed$(NC)"

security-scan: ## Run security scans locally
	@echo "$(BLUE)Running security scans...$(NC)"
	cd backend && pip install bandit safety pip-audit
	cd backend && bandit -r app/ || true
	cd backend && safety check --file requirements.txt || true
	cd backend && pip-audit -r requirements.txt || true
	cd frontend && npm audit || true
	@echo "$(GREEN)✓ Security scans complete$(NC)"

##@ Deployment

deploy-staging: ## Deploy to staging (requires confirmation)
	@echo "$(YELLOW)Deploying to STAGING environment...$(NC)"
	@read -p "Continue? (yes/no): " confirm; \
	if [ "$$confirm" = "yes" ]; then \
		echo "$(BLUE)Deploying...$(NC)"; \
		gh workflow run deploy.yml -f environment=staging -f image_tag=develop; \
		echo "$(GREEN)✓ Deployment triggered$(NC)"; \
	else \
		echo "$(YELLOW)Cancelled$(NC)"; \
	fi

deploy-prod: ## Deploy to production (requires confirmation)
	@echo "$(RED)⚠️  Deploying to PRODUCTION environment...$(NC)"
	@read -p "Are you SURE? (yes/no): " confirm; \
	if [ "$$confirm" = "yes" ]; then \
		echo "$(BLUE)Deploying...$(NC)"; \
		gh workflow run deploy.yml -f environment=production -f image_tag=latest; \
		echo "$(GREEN)✓ Deployment triggered$(NC)"; \
	else \
		echo "$(YELLOW)Cancelled$(NC)"; \
	fi

##@ Utilities

clean: ## Clean up generated files and caches
	@echo "$(BLUE)Cleaning up...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	cd frontend && rm -rf dist/ build/ node_modules/.cache/ 2>/dev/null || true
	@echo "$(GREEN)✓ Cleanup complete$(NC)"

install-hooks: ## Install pre-commit hooks
	@echo "$(BLUE)Installing pre-commit hooks...$(NC)"
	pip install pre-commit
	pre-commit install
	@echo "$(GREEN)✓ Pre-commit hooks installed$(NC)"

backup: ## Create database backup
	@echo "$(BLUE)Creating database backup...$(NC)"
	./scripts/backup_database.sh
	@echo "$(GREEN)✓ Backup complete$(NC)"

health: ## Check service health
	@echo "$(BLUE)Checking service health...$(NC)"
	./scripts/health_check.sh

update-deps: ## Update dependencies
	@echo "$(BLUE)Updating dependencies...$(NC)"
	cd backend && pip install --upgrade -r requirements.txt
	cd frontend && npm update
	@echo "$(GREEN)✓ Dependencies updated$(NC)"
