#!/bin/bash
# Daily Maintenance Script for Construction Intelligence Platform
# Run this script once per day via cron

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BACKEND_URL="https://your-backend.up.railway.app"
FRONTEND_URL="https://your-app.vercel.app"
LOG_FILE="$HOME/maintenance/health-check-$(date +%Y%m%d).log"
EMAIL_ALERTS="your-email@example.com"  # Set your email for alerts

# Create log directory
mkdir -p "$HOME/maintenance"

# Function to log with timestamp
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Function to send alert (requires mailutils)
send_alert() {
    local subject="$1"
    local message="$2"
    
    # Uncomment if you have mailutils configured
    # echo "$message" | mail -s "$subject" "$EMAIL_ALERTS"
    
    # For now, just log
    log "ALERT: $subject - $message"
}

echo "" | tee -a "$LOG_FILE"
log "=========================================="
log "Construction Intelligence Platform"
log "Daily Health Check"
log "=========================================="

# 1. Check Backend Health
log ""
log "1. Checking Backend Health..."
BACKEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BACKEND_URL/health" 2>&1)

if [ "$BACKEND_STATUS" = "200" ]; then
    log "${GREEN}✓ Backend: Healthy (Status: 200)${NC}"
else
    log "${RED}✗ Backend: Unhealthy (Status: $BACKEND_STATUS)${NC}"
    send_alert "Backend Down" "Backend returned status $BACKEND_STATUS"
fi

# Get backend response time
BACKEND_TIME=$(curl -s -o /dev/null -w "%{time_total}" "$BACKEND_URL/health" 2>&1)
log "  Response time: ${BACKEND_TIME}s"

if (( $(echo "$BACKEND_TIME > 2" | bc -l) )); then
    log "${YELLOW}  Warning: Slow response time${NC}"
fi

# 2. Check Frontend
log ""
log "2. Checking Frontend..."
FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$FRONTEND_URL" 2>&1)

if [ "$FRONTEND_STATUS" = "200" ]; then
    log "${GREEN}✓ Frontend: Healthy (Status: 200)${NC}"
else
    log "${RED}✗ Frontend: Unhealthy (Status: $FRONTEND_STATUS)${NC}"
    send_alert "Frontend Down" "Frontend returned status $FRONTEND_STATUS"
fi

# 3. Check API Endpoints
log ""
log "3. Checking API Endpoints..."

# Test projects endpoint (should return 401 without auth)
PROJECTS_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BACKEND_URL/api/v1/projects/" 2>&1)

if [ "$PROJECTS_STATUS" = "401" ] || [ "$PROJECTS_STATUS" = "200" ]; then
    log "${GREEN}✓ Projects API: Accessible${NC}"
else
    log "${RED}✗ Projects API: Error (Status: $PROJECTS_STATUS)${NC}"
fi

# 4. Check SSL Certificates (expires soon?)
log ""
log "4. Checking SSL Certificates..."

# Extract domain from URL
BACKEND_DOMAIN=$(echo "$BACKEND_URL" | sed -e 's|^https\?://||' -e 's|/.*$||')
FRONTEND_DOMAIN=$(echo "$FRONTEND_URL" | sed -e 's|^https\?://||' -e 's|/.*$||')

# Check backend SSL
BACKEND_SSL_DAYS=$(echo | openssl s_client -servername "$BACKEND_DOMAIN" -connect "$BACKEND_DOMAIN:443" 2>/dev/null | openssl x509 -noout -dates | grep notAfter | cut -d= -f2)
log "  Backend SSL expires: $BACKEND_SSL_DAYS"

# Check frontend SSL
FRONTEND_SSL_DAYS=$(echo | openssl s_client -servername "$FRONTEND_DOMAIN" -connect "$FRONTEND_DOMAIN:443" 2>/dev/null | openssl x509 -noout -dates | grep notAfter | cut -d= -f2)
log "  Frontend SSL expires: $FRONTEND_SSL_DAYS"

# 5. Check Database Size (if using Supabase)
log ""
log "5. Database Check..."
log "  Check Supabase dashboard: https://app.supabase.com"
log "  Ensure database size < 500MB (free tier)"

# 6. Check Railway Resource Usage
log ""
log "6. Resource Usage Check..."
log "  Check Railway dashboard: https://railway.app/dashboard"
log "  Monitor: CPU, RAM, Disk usage"

# 7. Check for Recent Errors (if using Sentry)
log ""
log "7. Error Tracking..."
log "  Check Sentry dashboard: https://sentry.io"
log "  Review any new errors"

# 8. Backup Reminder
log ""
log "8. Backup Status..."
LAST_BACKUP_DATE=$(ls -t "$HOME/backups/construction-intel/" 2>/dev/null | head -1 | grep -oP '\d{8}')

if [ -n "$LAST_BACKUP_DATE" ]; then
    DAYS_SINCE_BACKUP=$(( ($(date +%s) - $(date -d "$LAST_BACKUP_DATE" +%s)) / 86400 ))
    log "  Last backup: $LAST_BACKUP_DATE ($DAYS_SINCE_BACKUP days ago)"
    
    if [ "$DAYS_SINCE_BACKUP" -gt 30 ]; then
        log "${YELLOW}  Warning: No backup in 30+ days${NC}"
        log "  Run: bash $HOME/maintenance/backup-db.sh"
    fi
else
    log "${YELLOW}  No backups found${NC}"
fi

# 9. Dependency Updates Check (weekly)
if [ "$(date +%u)" -eq 1 ]; then  # Monday
    log ""
    log "9. Weekly Tasks:"
    log "  - Check for dependency updates"
    log "  - Review security advisories"
    log "  - Check application metrics"
fi

# 10. Summary
log ""
log "=========================================="
log "Health Check Summary"
log "=========================================="

TOTAL_CHECKS=2
PASSED_CHECKS=0

if [ "$BACKEND_STATUS" = "200" ]; then
    ((PASSED_CHECKS++))
fi

if [ "$FRONTEND_STATUS" = "200" ]; then
    ((PASSED_CHECKS++))
fi

if [ "$PASSED_CHECKS" -eq "$TOTAL_CHECKS" ]; then
    log "${GREEN}All systems operational ($PASSED_CHECKS/$TOTAL_CHECKS)${NC}"
else
    log "${RED}Some systems need attention ($PASSED_CHECKS/$TOTAL_CHECKS)${NC}"
    send_alert "System Health Alert" "$PASSED_CHECKS/$TOTAL_CHECKS systems operational"
fi

# 11. Action Items
log ""
log "Action Items:"

if [ "$BACKEND_STATUS" != "200" ]; then
    log "  [ ] Investigate backend issues"
fi

if [ "$FRONTEND_STATUS" != "200" ]; then
    log "  [ ] Investigate frontend issues"
fi

if (( $(echo "$BACKEND_TIME > 2" | bc -l) )); then
    log "  [ ] Optimize backend performance"
fi

log ""
log "Check complete. Log saved to: $LOG_FILE"
log ""

# Clean up old logs (keep last 30 days)
find "$HOME/maintenance" -name "health-check-*.log" -mtime +30 -delete

exit 0
