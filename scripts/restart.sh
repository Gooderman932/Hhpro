#!/bin/bash
# Restart all services

echo "Restarting Construction Intelligence Platform..."

# Ensure PostgreSQL and Redis are running
service postgresql start 2>/dev/null
service redis-server start 2>/dev/null

# Restart backend and frontend via supervisor
supervisorctl restart backend frontend

echo "Services restarted!"
echo "Check status: supervisorctl status"
