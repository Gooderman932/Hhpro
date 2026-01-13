# GitHub Secrets Configuration

Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.

This document describes all GitHub Secrets required for the CI/CD pipeline to function properly.

## Overview

GitHub Actions workflows use encrypted secrets to securely store sensitive information like API keys, database credentials, and deployment tokens. These secrets must be configured in your repository settings before running any workflows.

## How to Add Secrets

1. Go to your GitHub repository
2. Click on **Settings** > **Secrets and variables** > **Actions**
3. Click **New repository secret**
4. Enter the secret name and value
5. Click **Add secret**

## Required Secrets

### Application Secrets

#### `SECRET_KEY` (Required)
- **Description**: Secret key for JWT token generation and encryption
- **Used in**: All environments
- **Format**: Long random string (minimum 32 characters)
- **Example**: Generate with `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- **Workflows**: ci-cd.yml, scheduled-automation.yml

#### `OPENAI_API_KEY` (Optional)
- **Description**: OpenAI API key for AI/ML features
- **Used in**: Production, Staging (if using AI features)
- **Format**: `sk-...`
- **Get it from**: https://platform.openai.com/api-keys
- **Workflows**: ci-cd.yml, scheduled-automation.yml

### Database Secrets

#### `DATABASE_URL_STAGING` (Required for Staging)
- **Description**: PostgreSQL connection URL for staging environment
- **Format**: `postgresql://username:password@host:port/database`
- **Example**: `postgresql://staginguser:pass123@staging-db.example.com:5432/construction_intel`
- **Workflows**: migrations.yml, scheduled-automation.yml

#### `DATABASE_URL_PRODUCTION` (Required for Production)
- **Description**: PostgreSQL connection URL for production environment
- **Format**: `postgresql://username:password@host:port/database`
- **Example**: `postgresql://produser:securepass@prod-db.example.com:5432/construction_intel`
- **Workflows**: migrations.yml, scheduled-automation.yml
- **⚠️ Warning**: Ensure this uses a secure, backed-up production database

#### `POSTGRES_PASSWORD` (Required)
- **Description**: PostgreSQL database password
- **Used in**: Docker builds, deployments
- **Format**: Secure password string
- **Workflows**: deploy.yml, docker-compose.prod.yml

#### `REDIS_PASSWORD` (Required)
- **Description**: Redis cache password
- **Used in**: Production, Staging
- **Format**: Secure password string
- **Workflows**: deploy.yml, docker-compose.prod.yml

### Monetization & Platform Secrets

#### `MONETIZATION_API_KEY` (Optional)
- **Description**: API key for monetization platform integration
- **Used in**: scheduled-automation.yml
- **Format**: API key string
- **Workflows**: scheduled-automation.yml

### Container Registry Secrets

#### `GITHUB_TOKEN` (Automatically Available)
- **Description**: Automatically provided by GitHub for pushing to GitHub Container Registry
- **Used in**: Docker image builds
- **No action needed**: This is automatically available in workflows
- **Workflows**: ci-cd.yml, docker.yml

#### `DOCKERHUB_USERNAME` (Optional - if using Docker Hub)
- **Description**: Docker Hub username
- **Used in**: Pushing to Docker Hub (alternative to GitHub Container Registry)
- **Format**: Your Docker Hub username
- **Workflows**: ci-cd.yml (if modified to use Docker Hub)

#### `DOCKERHUB_TOKEN` (Optional - if using Docker Hub)
- **Description**: Docker Hub access token
- **Get it from**: https://hub.docker.com/settings/security
- **Workflows**: ci-cd.yml (if modified to use Docker Hub)

### Deployment Secrets

#### `DEPLOY_SSH_KEY` (Optional - if using SSH deployment)
- **Description**: Private SSH key for deployment to servers
- **Format**: Complete SSH private key including headers
- **Example**:
  ```
  -----BEGIN OPENSSH PRIVATE KEY-----
  [key content]
  -----END OPENSSH PRIVATE KEY-----
  ```
- **Generate with**: `ssh-keygen -t ed25519 -C "github-actions"`
- **Workflows**: deploy.yml (if modified for SSH deployment)

### Notification Secrets

#### `SLACK_WEBHOOK_URL` (Optional)
- **Description**: Slack webhook URL for notifications
- **Used in**: Failure notifications in workflows
- **Get it from**: Slack App > Incoming Webhooks
- **Format**: `https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXX`
- **Workflows**: scheduled-automation.yml, deploy.yml

## Environment-Specific Secrets

Some secrets can be configured per environment (staging/production):

### Staging Environment Secrets
Navigate to: **Settings** > **Environments** > **staging** > **Add secret**

- `DATABASE_URL_STAGING`
- `STAGING_API_URL`

### Production Environment Secrets
Navigate to: **Settings** > **Environments** > **production** > **Add secret**

- `DATABASE_URL_PRODUCTION`
- `PRODUCTION_API_URL`

## Security Best Practices

1. **Never commit secrets to code**: Always use GitHub Secrets
2. **Rotate secrets regularly**: Change passwords and keys periodically
3. **Use strong passwords**: Minimum 20 characters with mixed case, numbers, symbols
4. **Limit secret access**: Only give secrets to necessary environments
5. **Audit secret usage**: Review which workflows use which secrets
6. **Use environment protection rules**: Require approval for production deployments

## Validation

To verify your secrets are configured correctly:

1. Go to **Actions** tab
2. Run the workflow manually
3. Check the logs (secrets will be masked as `***`)

## Troubleshooting

### Secret Not Found Error
- Verify the secret name matches exactly (case-sensitive)
- Check the secret is in the correct environment
- Ensure the workflow has permission to access the secret

### Secret Value Not Working
- Check for extra spaces or newlines when pasting
- Verify the secret format matches the required format
- Try regenerating the secret and updating it

### Permission Denied
- Check repository settings for secret access
- Verify environment protection rules
- Ensure workflow has necessary permissions

## Need Help?

Contact the platform team or refer to:
- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Repository README](../README.md)
- [CI/CD Documentation](../docs/CICD.md)
