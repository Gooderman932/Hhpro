# GitHub Secrets Configuration

This document describes all GitHub Secrets required for the CI/CD pipeline and deployment automation.

## Table of Contents
- [Required Secrets](#required-secrets)
- [Optional Secrets](#optional-secrets)
- [Setup Instructions](#setup-instructions)
- [Secret Management Best Practices](#secret-management-best-practices)

## Required Secrets

### Staging Environment

#### `DATABASE_URL_STAGING`
**Description:** PostgreSQL connection string for staging database

**Format:**
```
postgresql://username:password@host:5432/database_name
```

**Example:**
```
postgresql://buildintel_staging:SecurePass123@staging-db.example.com:5432/construction_intel_staging?sslmode=require
```

**Where to get:**
- Create PostgreSQL database on your hosting provider
- Use managed service (AWS RDS, Azure Database, GCP Cloud SQL)
- For testing, use local PostgreSQL with ngrok tunnel

---

#### `SECRET_KEY_STAGING`
**Description:** Secret key for JWT token signing and session management

**Format:** Random string (minimum 32 characters)

**Generate:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
# or
openssl rand -base64 32
```

**Example:**
```
8BYkEfBA6O2donzWlSihBXox7C0sKR6b
```

---

### Production Environment

#### `DATABASE_URL_PRODUCTION`
**Description:** PostgreSQL connection string for production database

**Format:** Same as staging, but for production database

**Security Notes:**
- Use strong password (20+ characters, mixed case, numbers, symbols)
- Enable SSL/TLS connection (`?sslmode=require`)
- Use managed database service with encryption at rest
- Enable automated backups
- Restrict network access (VPC, security groups)

---

#### `SECRET_KEY_PRODUCTION`
**Description:** Secret key for production environment

**Generate:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

**Security Notes:**
- Use different key than staging
- Minimum 64 characters for production
- Never reuse or expose
- Rotate periodically (e.g., every 90 days)

---

### API Keys

#### `OPENAI_API_KEY`
**Description:** OpenAI API key for AI/ML features

**Where to get:**
1. Sign up at https://platform.openai.com/
2. Go to API Keys section
3. Create new secret key
4. Copy key (shown only once)

**Format:**
```
sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Usage limits:**
- Set usage limits in OpenAI dashboard
- Monitor usage regularly
- Use different keys for staging/production if possible

---

#### `MONETIZATION_API_KEY`
**Description:** API key for monetization service

**Where to get:** From your monetization service provider

**Optional:** Only required if using external monetization service

---

### Docker Registry

#### `DOCKER_REGISTRY_TOKEN` (Optional)
**Description:** GitHub Container Registry uses GITHUB_TOKEN by default

**When needed:**
- Using external registry (Docker Hub, AWS ECR)
- Need special permissions

**For GitHub Container Registry:**
- Uses `${{ secrets.GITHUB_TOKEN }}` automatically
- No additional secret needed

---

### Notifications

#### `SLACK_WEBHOOK_URL` (Optional but recommended)
**Description:** Slack webhook for deployment and alert notifications

**Setup:**
1. Go to your Slack workspace
2. Create app: https://api.slack.com/apps
3. Enable Incoming Webhooks
4. Add webhook to channel
5. Copy webhook URL

**Format:**
```
https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXX
```

**Test:**
```bash
curl -X POST $SLACK_WEBHOOK_URL \
  -H 'Content-Type: application/json' \
  -d '{"text":"Test notification from CI/CD"}'
```

---

## Optional Secrets

### Code Coverage

#### `CODECOV_TOKEN`
**Description:** Token for uploading coverage reports to Codecov

**Where to get:**
1. Sign up at https://codecov.io/
2. Add repository
3. Copy token from repository settings

**Note:** Public repositories may not need this

---

### Monitoring & Error Tracking

#### `SENTRY_DSN`
**Description:** Sentry DSN for error tracking

**Where to get:**
1. Sign up at https://sentry.io/
2. Create project
3. Copy DSN from project settings

**Format:**
```
https://xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx@sentry.io/1234567
```

---

### Cloud Provider Credentials

Only needed if deploying to cloud providers:

#### `AWS_ACCESS_KEY_ID`
#### `AWS_SECRET_ACCESS_KEY`
**Description:** AWS credentials for deployment

**Where to get:**
1. AWS Console → IAM
2. Create deployment user
3. Attach necessary policies
4. Create access key

---

#### `AZURE_CREDENTIALS`
**Description:** Azure service principal credentials

**Format:** JSON object

```json
{
  "clientId": "xxx",
  "clientSecret": "xxx",
  "subscriptionId": "xxx",
  "tenantId": "xxx"
}
```

---

## Setup Instructions

### Adding Secrets to GitHub

**Via Web UI:**
1. Go to repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Enter name and value
5. Click **Add secret**

**Via GitHub CLI:**
```bash
# Set a secret
gh secret set SECRET_NAME

# Set from file
gh secret set SECRET_NAME < secret_file.txt

# Set with value
echo "secret_value" | gh secret set SECRET_NAME

# List secrets
gh secret list
```

**Via API:**
```bash
# Requires GitHub token with repo scope
curl -X PUT \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: token YOUR_GITHUB_TOKEN" \
  https://api.github.com/repos/OWNER/REPO/actions/secrets/SECRET_NAME \
  -d '{"encrypted_value":"ENCRYPTED_VALUE","key_id":"KEY_ID"}'
```

### Environment Secrets

For staging and production environments:

1. Go to **Settings** → **Environments**
2. Create environment (staging/production)
3. Add environment-specific secrets
4. Configure protection rules (approvers, wait timer)

### Organization Secrets

For secrets shared across repositories:

1. Go to organization **Settings** → **Secrets**
2. Add organization secret
3. Select which repositories can access

## Secret Management Best Practices

### Security

✅ **Do:**
- Use strong, randomly generated secrets
- Rotate secrets regularly (90 days)
- Use different secrets for each environment
- Store secrets in secure password manager
- Use environment-specific secrets
- Enable secret scanning on GitHub
- Use managed services when possible
- Encrypt secrets at rest

❌ **Don't:**
- Commit secrets to repository (even in .env files)
- Share secrets via chat/email
- Reuse secrets across projects
- Use weak or predictable secrets
- Give secrets broad permissions
- Store secrets in code comments
- Hard-code secrets in applications

### Access Control

- Limit who can access secrets
- Use role-based access control (RBAC)
- Audit secret access regularly
- Remove access when no longer needed
- Use service accounts for automation

### Monitoring

- Enable GitHub secret scanning
- Monitor for leaked secrets
- Set up alerts for unauthorized access
- Review audit logs regularly
- Track secret usage

### Rotation

Create a rotation schedule:

| Secret Type | Rotation Frequency |
|------------|-------------------|
| Database passwords | 90 days |
| API keys | 180 days |
| JWT secrets | 90 days |
| Service credentials | 90 days |
| Webhooks | As needed |

### Backup & Recovery

- Document all secrets (not values!)
- Keep encrypted backups
- Test recovery procedures
- Have emergency access plan
- Document secret dependencies

### Testing Secrets

**Never use production secrets in testing!**

For testing:
- Use test/sandbox API keys when available
- Generate temporary secrets for testing
- Use mocked services where possible
- Clear test secrets after use

## Troubleshooting

### Secret Not Working

1. **Check secret name** - Exact match required, case-sensitive
2. **Check format** - No leading/trailing whitespace
3. **Check environment** - Right secret for right environment?
4. **Check permissions** - Does workflow have access?
5. **Check expiration** - Some API keys expire

### Secret Scanning Alert

If GitHub detects a secret in your repository:

1. **Immediately rotate** the exposed secret
2. **Update** the secret in GitHub Secrets
3. **Review** commit history for other exposures
4. **Investigate** how secret was exposed
5. **Update processes** to prevent future exposures

### Workflow Can't Access Secret

Check:
- Secret exists in repository/organization
- Secret name matches exactly in workflow
- Workflow has proper permissions
- Environment protection rules allow access
- Organization allows repository access (if org secret)

## Additional Resources

- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
- [Security Hardening](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [Environment Protection Rules](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment)

## Support

For issues with secrets:
1. Check this documentation
2. Review GitHub Actions logs (secrets are masked)
3. Test locally with environment variables
4. Contact team lead or DevOps
