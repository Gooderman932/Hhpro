# 🔒 Security Hardening Guide

This document outlines security best practices and hardening steps for the Construction Intelligence Platform.

## 🎯 Quick Security Checklist

Before going to production:

- [ ] Change all default credentials
- [ ] Generate strong SECRET_KEY (32+ characters)
- [ ] Enable HTTPS/TLS with valid certificates
- [ ] Configure rate limiting
- [ ] Set up database backups
- [ ] Enable security headers
- [ ] Configure firewall rules
- [ ] Disable debug mode (ENVIRONMENT=production, DEBUG=false)
- [ ] Review CORS origins
- [ ] Set up monitoring and alerting
- [ ] Regular security updates
- [ ] Implement database encryption at rest (if handling sensitive data)
- [ ] Set up intrusion detection

## 🔐 Authentication & Authorization

### Secret Key Management

**Generate a secure SECRET_KEY:**
```bash
# Linux/Mac
openssl rand -hex 32

# Python
python -c "import secrets; print(secrets.token_hex(32))"
```

**Store securely:**
- Use environment variables, never commit to git
- Use secret management services (AWS Secrets Manager, HashiCorp Vault)
- Rotate keys periodically

### Password Security

**Default Configuration:**
- Minimum length: 8 characters
- Requires uppercase, lowercase, and digits
- Uses bcrypt for hashing

**Strengthen password requirements:**
```python
# In .env
PASSWORD_MIN_LENGTH=12
PASSWORD_REQUIRE_UPPERCASE=true
PASSWORD_REQUIRE_LOWERCASE=true
PASSWORD_REQUIRE_DIGIT=true
PASSWORD_REQUIRE_SPECIAL=true
```

### JWT Token Security

**Current settings:**
- Access tokens expire in 30 minutes
- Refresh tokens expire in 7 days
- HS256 algorithm

**Recommended for production:**
```bash
# Shorter token lifetimes for sensitive operations
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=1
```

## 🌐 Network Security

### HTTPS/TLS Configuration

**Minimum TLS version: 1.2**
```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
ssl_prefer_server_ciphers off;
```

**Certificate Management:**
- Use Let's Encrypt for free, automated certificates
- Set up auto-renewal with certbot
- Monitor certificate expiration

### CORS Configuration

**Production CORS settings:**
```bash
# Only allow your actual domains
CORS_ORIGINS=https://app.yourdomain.com,https://api.yourdomain.com

# Never use wildcard (*) in production
```

### Rate Limiting

**API endpoints:**
- 10 requests/second for general API
- 5 requests/minute for authentication
- 10 concurrent connections per IP

**Adjust in nginx.conf:**
```nginx
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=auth_limit:10m rate=5r/m;
```

### Firewall Rules

**Allow only necessary ports:**
```bash
# Ubuntu UFW
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp   # SSH (consider changing default port)
sudo ufw allow 80/tcp   # HTTP (for redirect to HTTPS)
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable

# CentOS/RHEL firewalld
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

## 🗄️ Database Security

### PostgreSQL Hardening

**Strong credentials:**
```bash
# Generate strong password
POSTGRES_PASSWORD=$(openssl rand -base64 32)
```

**Connection security:**
```bash
# Require SSL connections
DATABASE_URL="postgresql://user:pass@host:5432/db?sslmode=require"
```

**Access control:**
- Limit network access to database port
- Use separate credentials for different services
- Implement least privilege principle

### Redis Security

**Enable password authentication:**
```bash
REDIS_PASSWORD=$(openssl rand -base64 32)
```

**Configure in docker-compose.prod.yml:**
```yaml
redis:
  command: redis-server --requirepass ${REDIS_PASSWORD}
```

## 🛡️ Application Security

### Security Headers

**Configured in nginx.conf:**
```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
add_header Content-Security-Policy "default-src 'self' https:;" always;
```

### Input Validation

- FastAPI automatically validates input using Pydantic models
- SQLAlchemy ORM prevents SQL injection
- All user inputs are sanitized

### File Upload Security

**Current limits:**
```bash
MAX_UPLOAD_SIZE=10485760  # 10MB
ALLOWED_UPLOAD_EXTENSIONS=".pdf,.csv,.xlsx,.json,.docx"
```

**Recommendations:**
- Scan uploads for malware
- Store uploaded files outside web root
- Use cloud storage (S3) for production
- Implement virus scanning

### API Security

**API documentation:**
- Disable in production (set DEBUG=false)
- Or protect with authentication

**API versioning:**
- All endpoints under /api/v1
- Allows non-breaking updates

## 🔍 Monitoring & Logging

### Logging

**Configure log levels:**
```bash
# Production
LOG_LEVEL=INFO

# Debugging issues
LOG_LEVEL=DEBUG
```

**Log sensitive data:**
- Never log passwords or secrets
- Sanitize user data before logging
- Use structured logging (JSON)

### Error Tracking

**Sentry integration:**
```bash
SENTRY_DSN=https://your-sentry-dsn
SENTRY_ENVIRONMENT=production
SENTRY_TRACES_SAMPLE_RATE=0.1
```

### Security Monitoring

**Monitor for:**
- Failed authentication attempts
- Unusual API usage patterns
- Database connection errors
- File upload attempts
- Rate limit violations

**Set up alerts:**
```bash
# Example: Failed login attempts
docker-compose -f docker-compose.prod.yml logs backend | grep "Failed login"
```

## 🔄 Updates & Maintenance

### Regular Updates

**Schedule:**
- Security patches: As soon as available
- Minor updates: Monthly
- Major updates: Quarterly (with testing)

**Process:**
```bash
# Update system packages
sudo apt-get update && sudo apt-get upgrade

# Update Docker images
docker-compose -f docker-compose.prod.yml pull

# Update application
git pull origin main
./scripts/deployment/deploy.sh
```

### Dependency Management

**Backend (Python):**
```bash
# Check for vulnerabilities
pip install safety
safety check -r backend/requirements.txt

# Update dependencies
pip install --upgrade -r backend/requirements.txt
```

**Frontend (Node.js):**
```bash
# Check for vulnerabilities
cd frontend
npm audit

# Fix vulnerabilities
npm audit fix

# Update dependencies
npm update
```

## 🔐 Secret Management

### Environment Variables

**Never commit:**
- .env files
- Credentials
- API keys
- Secrets

**Use:**
- Environment-specific .env files
- Secret management services
- GitHub Secrets for CI/CD

### Backup Encryption

**Encrypt backups:**
```bash
# Backup with encryption
docker-compose -f docker-compose.prod.yml exec -T postgres pg_dump \
  -U $POSTGRES_USER -d $POSTGRES_DB | \
  gzip | \
  openssl enc -aes-256-cbc -salt -out backup_encrypted.gz
```

## 🚨 Incident Response

### Security Incident Checklist

1. **Identify**: Detect and confirm the incident
2. **Contain**: Isolate affected systems
3. **Investigate**: Determine scope and impact
4. **Remediate**: Fix vulnerabilities
5. **Recover**: Restore normal operations
6. **Review**: Document and improve

### Emergency Procedures

**Suspected breach:**
```bash
# 1. Stop services
docker-compose -f docker-compose.prod.yml down

# 2. Backup current state
./scripts/deployment/backup.sh

# 3. Review logs
docker-compose -f docker-compose.prod.yml logs > incident_logs.txt

# 4. Rotate credentials
# Change all passwords and secret keys

# 5. Restore from clean backup if needed
```

## 📋 Compliance

### Data Protection

- **GDPR**: Implement data deletion and export features
- **CCPA**: Provide data access and deletion rights
- **HIPAA**: Enable encryption at rest and in transit (if applicable)

### Audit Logging

**Enable audit logs for:**
- User authentication
- Data access
- Configuration changes
- Administrative actions

## 📞 Security Contacts

**Report security vulnerabilities:**
- Email: security@yourdomain.com
- Response time: 24 hours
- Bug bounty program: TBD

---

**Last Updated:** January 2026
**Review Schedule:** Quarterly

**Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.**
