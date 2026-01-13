# Platform Automation Documentation

## Table of Contents
- [Overview](#overview)
- [Automated Platform Manager](#automated-platform-manager)
- [Scheduled Tasks](#scheduled-tasks)
- [Platform Monitoring](#platform-monitoring)
- [Report Generation](#report-generation)
- [Alert Configuration](#alert-configuration)

## Overview

The Construction Intelligence Platform includes comprehensive automation capabilities through the `automated_platform_manager.py` script and GitHub Actions workflows.

### Automation Goals

- **Zero manual intervention** for routine tasks
- **Proactive monitoring** of platform health
- **Automated optimization** of AI models
- **Business intelligence** generation
- **Cost optimization** through automated monetization

## Automated Platform Manager

Location: `tools/automated_platform.py`

### Features

The automation script provides:

1. **Platform Health Monitoring**
   - Uptime tracking
   - Resource usage monitoring
   - Error rate tracking
   - Real-time metrics collection

2. **AI Model Optimization**
   - Performance metrics analysis
   - Training data statistics
   - Optimization recommendations
   - Automated model retraining triggers

3. **Monetization Automation**
   - Billing report generation
   - Subscription renewal processing
   - Revenue analytics
   - Customer retention metrics

4. **Business Insights Generation**
   - KPI tracking and analysis
   - Market trend identification
   - Competitive advantage assessment
   - Growth opportunity identification

### Usage

**Manual execution:**
```bash
python tools/automated_platform.py
```

**With custom configuration:**
```python
from tools.automated_platform import AutomatedPlatformManager, PlatformConfig

config = PlatformConfig(
    repo_path="/path/to/repo",
    api_key="your-api-key",
    model_endpoint="https://api.example.com/ml",
    monetization_endpoint="https://api.example.com/monetize"
)

manager = AutomatedPlatformManager(config)
summary = manager.run_automated_pipeline()
```

**Via GitHub Actions:**
The script runs automatically via scheduled workflows (see below).

### Database Integration

The automation script integrates with the existing database models:

- `User`: Active user tracking
- `Tenant`: Multi-tenancy support
- `Company`: Company analytics
- `Project`: Project tracking and analytics
- `Prediction`: AI model predictions
- `OpportunityScore`: Opportunity scoring

**Note:** Some features (billing, subscriptions) are stubbed until corresponding database tables are created. See code comments for implementation guidance.

## Scheduled Tasks

### Daily Tasks (2 AM UTC)

Configured in `.github/workflows/scheduled-tasks.yml`

**Automated Actions:**
1. Run automated platform manager
2. Generate health reports
3. Optimize AI models
4. Process monetization reports
5. Generate business insights
6. Archive reports to artifacts
7. Send summary notifications

**Execution:**
```yaml
schedule:
  - cron: '0 2 * * *'  # Every day at 2 AM UTC
```

**Manual trigger:**
```bash
gh workflow run scheduled-tasks.yml --field task_type=daily
```

### Weekly Tasks (Sundays 3 AM UTC)

**Automated Actions:**
1. Comprehensive platform health audit
2. Database optimization (VACUUM, ANALYZE)
3. Cleanup old data and logs
4. Generate weekly business reports
5. Archive weekly reports

**Execution:**
```yaml
schedule:
  - cron: '0 3 * * 0'  # Sundays at 3 AM UTC
```

**Manual trigger:**
```bash
gh workflow run scheduled-tasks.yml --field task_type=weekly
```

## Platform Monitoring

### Health Metrics

The automation system monitors:

**System Health:**
- Application uptime percentage
- Resource usage (CPU, memory, disk)
- Error rates (5m, 1h, 24h windows)

**Data Flow:**
- Active users count
- Projects tracked
- Companies in system
- API calls volume
- Predictions made

**Performance:**
- Response times
- Database query performance
- Cache hit rates

### Health Check Endpoints

Backend provides health check endpoints:

```bash
# Basic health check
curl http://localhost:8000/health

# Database connectivity (implement if needed)
curl http://localhost:8000/health/db

# Detailed status (implement if needed)
curl http://localhost:8000/health/detailed
```

**Response format:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "production",
  "timestamp": "2025-01-12T02:00:00Z"
}
```

## Report Generation

### Report Types

The automation system generates several report types:

#### 1. Health Reports

Location: `data/automated/reports/health_*.json`

Contains:
- Timestamp
- Uptime percentage
- Resource usage metrics
- Error rates
- Active data flows

#### 2. Model Optimization Reports

Location: `data/automated/reports/model_optimization_*.json`

Contains:
- Model performance metrics (accuracy, precision, recall, F1, AUC-ROC)
- Training data statistics
- Optimization recommendations
- Timestamp

#### 3. Monetization Reports

Location: `data/automated/reports/monetization_*.json`

Contains:
- Active subscriptions
- Revenue metrics
- Billing data
- Renewal information
- Revenue growth analysis

#### 4. Business Insights Reports

Location: `data/automated/reports/business_insights_*.json`

Contains:
- Platform KPIs
- Market trends analysis
- Competitive advantages
- Growth opportunities

### Report Access

**In GitHub Actions:**
Reports are archived as artifacts and can be downloaded from the Actions UI.

**Locally:**
```bash
# Run automation
python tools/automated_platform.py

# View reports
ls -la data/automated/reports/

# View specific report
cat data/automated/reports/business_insights_20250112_020000.json | jq
```

### Report Retention

- **Daily reports**: 30 days
- **Weekly reports**: 90 days
- **Production reports**: Stored in artifact storage

## Alert Configuration

### Notification Setup

Notifications can be sent via:

1. **Slack Webhooks**
2. **Email (SMTP)**
3. **Custom webhook endpoints**

### Configuring Slack Notifications

1. **Create Slack Webhook:**
   - Go to Slack API: https://api.slack.com/messaging/webhooks
   - Create incoming webhook for your channel
   - Copy webhook URL

2. **Add to GitHub Secrets:**
   ```bash
   # Add SLACK_WEBHOOK_URL to repository secrets
   gh secret set SLACK_WEBHOOK_URL
   ```

3. **Notification is automatic** in workflows

### Alert Conditions

Alerts are triggered for:

- **Critical errors**: Application failures
- **High error rates**: Error rate > 5%
- **Low uptime**: Uptime < 95%
- **Resource exhaustion**: CPU/memory > 90%
- **Failed deployments**: Deployment workflow failures
- **Security vulnerabilities**: Critical CVEs detected
- **Database issues**: Connection failures, migration errors

### Customizing Alerts

Edit workflow files to customize alert conditions:

```yaml
- name: Send alert on failure
  if: failure()
  run: |
    curl -X POST ${{ secrets.SLACK_WEBHOOK_URL }} \
      -H 'Content-Type: application/json' \
      -d '{
        "text": "🚨 Alert: Task failed",
        "channel": "#alerts",
        "username": "Platform Bot"
      }'
```

## Monitoring Setup

### Adding Custom Metrics

To add custom metrics to the automation:

1. **Add metric collection:**
   ```python
   # In tools/automated_platform.py
   def _collect_custom_metric(self):
       # Your metric collection logic
       return metric_value
   ```

2. **Include in health check:**
   ```python
   def monitor_platform_health(self):
       health_status = {
           # ... existing metrics
           "custom_metric": self._collect_custom_metric()
       }
       return health_status
   ```

3. **Update report schema if needed**

### Database Monitoring

For production environments, consider adding:

- **Query performance monitoring**
- **Connection pool metrics**
- **Slow query logging**
- **Index usage statistics**

### Application Monitoring

Integrate with monitoring services:

- **Sentry**: Error tracking and performance monitoring
- **Prometheus**: Metrics collection
- **Grafana**: Metrics visualization
- **DataDog**: Full-stack monitoring

## Best Practices

### Automation

- Keep scripts idempotent (safe to run multiple times)
- Add proper error handling and logging
- Test in staging before production
- Monitor automation execution
- Set up alerts for automation failures

### Monitoring

- Define clear SLAs and SLOs
- Set up proactive alerts
- Regular review of metrics
- Trend analysis for capacity planning
- Document baseline metrics

### Reporting

- Archive important reports
- Regular review of generated insights
- Act on optimization recommendations
- Share reports with stakeholders
- Automate report distribution

## Troubleshooting

### Automation Script Fails

```bash
# Check logs
python tools/automated_platform.py

# Verify database connection
# Check DATABASE_URL environment variable

# Verify dependencies
pip install -r backend/requirements.txt
```

### No Reports Generated

```bash
# Check permissions
ls -la data/automated/reports/

# Create directory if missing
mkdir -p data/automated/reports

# Run manually to see errors
python tools/automated_platform.py
```

### Scheduled Tasks Not Running

```bash
# Check workflow status
gh workflow list

# View workflow runs
gh run list --workflow=scheduled-tasks.yml

# Check cron syntax
# https://crontab.guru/
```

## Future Enhancements

Planned improvements:

- [ ] Real-time alerting system
- [ ] Advanced anomaly detection
- [ ] Predictive capacity planning
- [ ] Automated cost optimization
- [ ] Custom dashboard for metrics
- [ ] Integration with more monitoring tools
- [ ] Machine learning for predictive maintenance

## Additional Resources

- [Deployment Guide](./DEPLOYMENT.md)
- [Development Workflow](./DEVELOPMENT.md)
- [GitHub Secrets Setup](./GITHUB_SECRETS.md)
- [Automation Script Source](../tools/automated_platform.py)
