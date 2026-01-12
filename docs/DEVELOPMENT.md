# Development Workflow

## Table of Contents
- [Local Development Setup](#local-development-setup)
- [Development Environment](#development-environment)
- [Testing Guidelines](#testing-guidelines)
- [Code Review Process](#code-review-process)
- [Git Workflow](#git-workflow)
- [Release Process](#release-process)

## Local Development Setup

### Prerequisites

**Required:**
- Python 3.11+
- Node.js 20+
- Docker & Docker Compose
- Git

**Optional:**
- pre-commit
- Make (for Makefile commands)

### Initial Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Gooderman932/market-data.git
   cd market-data
   ```

2. **Install dependencies:**
   ```bash
   make install
   # Or manually:
   cd backend && pip install -r requirements.txt
   cd ../frontend && npm install
   ```

3. **Install pre-commit hooks:**
   ```bash
   pip install pre-commit
   pre-commit install
   ```

4. **Copy environment file:**
   ```bash
   cp .env.example .env
   # Edit .env with your local settings
   ```

5. **Start development environment:**
   ```bash
   make dev
   # Or: docker compose up --build
   ```

6. **Access the application:**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/api/docs
   - Database: localhost:5432

## Development Environment

### Using Make Commands

```bash
# Development
make dev                    # Start dev environment
make dev-bg                 # Start in background
make stop                   # Stop services
make logs                   # View all logs
make logs-backend          # Backend logs only
make logs-frontend         # Frontend logs only

# Testing
make test                   # Run all tests
make test-backend          # Backend tests only
make test-backend-cov      # With coverage report
make test-frontend         # Frontend tests only

# Code Quality
make lint                   # Run all linters
make format                # Format all code
make security-scan         # Run security scans

# Database
make db-migrate            # Apply migrations
make db-migrate-create     # Create new migration
make db-seed               # Seed test data
make db-backup             # Backup database
make db-reset              # Reset database (WARNING: destroys data)

# Utilities
make shell-backend         # Open backend shell
make shell-frontend        # Open frontend shell
make shell-db              # Open PostgreSQL shell
make health-check          # Check all services
make clean                 # Clean build artifacts
```

### Backend Development

**Project Structure:**
```
backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration
│   ├── database.py          # Database connection
│   ├── models/              # SQLAlchemy models
│   ├── api/                 # API endpoints
│   ├── services/            # Business logic
│   ├── ml/                  # ML models
│   └── utils/               # Utilities
├── alembic/                 # Database migrations
├── requirements.txt         # Dependencies
└── pytest.ini              # Test configuration
```

**Running backend locally:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Code style:**
- Use Black for formatting (line length: 100)
- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for public functions

### Frontend Development

**Project Structure:**
```
frontend/
├── src/
│   ├── App.tsx             # Main application
│   ├── main.tsx            # Entry point
│   ├── components/         # React components
│   ├── hooks/              # Custom hooks
│   ├── services/           # API services
│   └── utils/              # Utilities
├── package.json            # Dependencies
└── vite.config.ts         # Vite configuration
```

**Running frontend locally:**
```bash
cd frontend
npm install
npm run dev
```

**Code style:**
- Use TypeScript strictly
- Follow React best practices
- Use functional components with hooks
- Use Tailwind CSS for styling

## Testing Guidelines

### Backend Testing

**Run tests:**
```bash
cd backend
pytest                      # All tests
pytest tests/test_api.py   # Specific file
pytest -k test_auth        # By keyword
pytest --cov=app           # With coverage
```

**Test structure:**
```python
def test_feature():
    """Test description"""
    # Arrange
    setup_data()
    
    # Act
    result = function_to_test()
    
    # Assert
    assert result == expected
```

**Coverage requirements:**
- Minimum 70% coverage (enforced in CI)
- Write tests for all new features
- Write tests for bug fixes

### Frontend Testing

Currently no frontend tests configured. To add:
```bash
cd frontend
npm install --save-dev vitest @testing-library/react
```

## Code Review Process

### Before Creating a PR

1. **Ensure all tests pass:**
   ```bash
   make test
   ```

2. **Run linters and formatters:**
   ```bash
   make format
   make lint
   ```

3. **Check for security issues:**
   ```bash
   make security-scan
   ```

4. **Update documentation if needed**

### Pull Request Guidelines

1. **Create feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes with good commit messages:**
   ```bash
   git commit -m "feat: add new feature"
   git commit -m "fix: resolve bug in authentication"
   ```

3. **Push and create PR:**
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Fill out PR template:**
   - Describe changes clearly
   - Link related issues
   - Add screenshots for UI changes
   - Check all checklist items

### Review Process

- **Required**: At least 1 approval
- **CI must pass**: All tests and checks
- **Code quality**: Linting, formatting
- **Documentation**: Updated as needed
- **Security**: No vulnerabilities introduced

## Git Workflow

### Branch Naming

```
feature/     - New features
fix/         - Bug fixes
hotfix/      - Urgent production fixes
docs/        - Documentation changes
refactor/    - Code refactoring
test/        - Test additions/changes
```

### Commit Message Format

Follow conventional commits:

```
<type>: <subject>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

**Examples:**
```bash
git commit -m "feat: add user authentication"
git commit -m "fix: resolve database connection issue"
git commit -m "docs: update deployment guide"
```

### Branching Strategy

```
main (production)
  ↑
  └── Pull Requests (reviewed & CI passed)
        ↑
        └── feature/* branches
```

**Workflow:**
1. Create feature branch from `main`
2. Develop and test locally
3. Push and create PR
4. Address review comments
5. Merge to `main` after approval

## Release Process

### Version Numbering

Follow Semantic Versioning (SemVer):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

Example: `1.2.3`

### Creating a Release

1. **Update version numbers:**
   - `backend/app/config.py`: `APP_VERSION`
   - `frontend/package.json`: `version`

2. **Create release branch:**
   ```bash
   git checkout -b release/v1.2.3
   ```

3. **Update CHANGELOG.md**

4. **Create PR and merge to main**

5. **Tag the release:**
   ```bash
   git tag -a v1.2.3 -m "Release version 1.2.3"
   git push origin v1.2.3
   ```

6. **Deploy to production:**
   ```bash
   gh workflow run deploy.yml --field environment=production
   ```

### Hotfix Process

For urgent production fixes:

1. **Create hotfix branch from main:**
   ```bash
   git checkout -b hotfix/critical-bug-fix
   ```

2. **Make minimal fix**

3. **Test thoroughly**

4. **Create PR with `hotfix` label**

5. **Fast-track review and merge**

6. **Deploy immediately to production**

## Best Practices

### General

- Write clean, readable code
- Follow DRY (Don't Repeat Yourself)
- Keep functions small and focused
- Use meaningful variable names
- Comment complex logic
- Handle errors properly

### Python

- Use type hints
- Follow PEP 8
- Use context managers for resources
- Prefer async/await for I/O operations
- Use Pydantic for data validation

### TypeScript/React

- Use strict TypeScript mode
- Prefer functional components
- Use hooks appropriately
- Memoize expensive computations
- Handle loading and error states

### Database

- Use migrations for schema changes
- Index frequently queried columns
- Avoid N+1 queries
- Use transactions appropriately
- Test migrations in staging first

### Security

- Never commit secrets
- Validate all user input
- Use parameterized queries
- Implement rate limiting
- Keep dependencies updated

## Getting Help

- **Documentation**: Check all docs in `/docs`
- **Issues**: Search existing issues or create new one
- **Code**: Read existing code for examples
- **Team**: Ask in team chat or during standups

## Additional Resources

- [Deployment Guide](./DEPLOYMENT.md)
- [Automation Documentation](./AUTOMATION.md)
- [GitHub Secrets Setup](./GITHUB_SECRETS.md)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
