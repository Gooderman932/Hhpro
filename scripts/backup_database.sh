#!/bin/bash
#
# Database Backup Script for Construction Intelligence Platform
#
# Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.
# PROPRIETARY AND CONFIDENTIAL - Unauthorized use prohibited.

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BACKUP_DIR="${BACKUP_DIR:-./backups}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="construction_intel_${TIMESTAMP}.sql.gz"
ENVIRONMENT="${ENVIRONMENT:-development}"

# Database connection details
DB_HOST="${POSTGRES_HOST:-localhost}"
DB_PORT="${POSTGRES_PORT:-5432}"
DB_NAME="${POSTGRES_DB:-construction_intel}"
DB_USER="${POSTGRES_USER:-user}"
PGPASSWORD="${POSTGRES_PASSWORD:-password}"

export PGPASSWORD

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}Construction Intelligence Platform${NC}"
echo -e "${BLUE}Database Backup${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""

# Create backup directory if it doesn't exist
if [ ! -d "${BACKUP_DIR}" ]; then
    echo -e "${YELLOW}Creating backup directory: ${BACKUP_DIR}${NC}"
    mkdir -p "${BACKUP_DIR}"
fi

# Check if pg_dump is available
if ! command -v pg_dump &> /dev/null; then
    echo -e "${RED}✗ pg_dump not found${NC}"
    echo "Please install PostgreSQL client tools"
    exit 1
fi

# Check database connection
echo -e "${YELLOW}Checking database connection...${NC}"
if psql -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d "${DB_NAME}" -c '\q' &> /dev/null; then
    echo -e "${GREEN}✓ Database connection successful${NC}"
else
    echo -e "${RED}✗ Cannot connect to database${NC}"
    echo "  Host: ${DB_HOST}:${DB_PORT}"
    echo "  Database: ${DB_NAME}"
    echo "  User: ${DB_USER}"
    exit 1
fi

# Create backup
echo ""
echo -e "${BLUE}Creating database backup...${NC}"
echo "  File: ${BACKUP_FILE}"
echo "  Environment: ${ENVIRONMENT}"

if pg_dump -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d "${DB_NAME}" \
    --clean --if-exists --create \
    --format=plain \
    --no-owner --no-privileges \
    | gzip > "${BACKUP_DIR}/${BACKUP_FILE}"; then
    
    # Get file size
    SIZE=$(du -h "${BACKUP_DIR}/${BACKUP_FILE}" | cut -f1)
    echo -e "${GREEN}✓ Backup created successfully${NC}"
    echo "  Size: ${SIZE}"
else
    echo -e "${RED}✗ Backup failed${NC}"
    exit 1
fi

# Create metadata file
METADATA_FILE="${BACKUP_DIR}/${BACKUP_FILE}.meta"
cat > "${METADATA_FILE}" << EOF
{
  "timestamp": "${TIMESTAMP}",
  "environment": "${ENVIRONMENT}",
  "database": "${DB_NAME}",
  "host": "${DB_HOST}",
  "backup_file": "${BACKUP_FILE}",
  "created_at": "$(date -Iseconds)"
}
EOF

echo -e "${GREEN}✓ Metadata saved${NC}"

# Clean up old backups
echo ""
echo -e "${YELLOW}Cleaning up old backups (retention: ${RETENTION_DAYS} days)...${NC}"

DELETED_COUNT=0
while IFS= read -r -d '' file; do
    if [ -f "${file}" ]; then
        rm -f "${file}"
        rm -f "${file}.meta"
        DELETED_COUNT=$((DELETED_COUNT + 1))
        echo "  Deleted: $(basename ${file})"
    fi
done < <(find "${BACKUP_DIR}" -name "construction_intel_*.sql.gz" -type f -mtime +${RETENTION_DAYS} -print0)

if [ ${DELETED_COUNT} -eq 0 ]; then
    echo -e "${GREEN}✓ No old backups to clean up${NC}"
else
    echo -e "${GREEN}✓ Deleted ${DELETED_COUNT} old backup(s)${NC}"
fi

# List recent backups
echo ""
echo -e "${BLUE}Recent backups:${NC}"
ls -lh "${BACKUP_DIR}"/construction_intel_*.sql.gz 2>/dev/null | tail -5 | awk '{print "  " $9 " (" $5 ")"}'

# Optional: Upload to cloud storage
if [ ! -z "${S3_BUCKET}" ]; then
    echo ""
    echo -e "${YELLOW}Uploading to S3...${NC}"
    
    if command -v aws &> /dev/null; then
        if aws s3 cp "${BACKUP_DIR}/${BACKUP_FILE}" "s3://${S3_BUCKET}/backups/${ENVIRONMENT}/${BACKUP_FILE}"; then
            echo -e "${GREEN}✓ Uploaded to S3${NC}"
            echo "  Bucket: ${S3_BUCKET}"
        else
            echo -e "${RED}✗ S3 upload failed${NC}"
        fi
    else
        echo -e "${YELLOW}⚠ AWS CLI not found, skipping S3 upload${NC}"
    fi
fi

# Optional: Upload to Google Cloud Storage
if [ ! -z "${GCS_BUCKET}" ]; then
    echo ""
    echo -e "${YELLOW}Uploading to Google Cloud Storage...${NC}"
    
    if command -v gsutil &> /dev/null; then
        if gsutil cp "${BACKUP_DIR}/${BACKUP_FILE}" "gs://${GCS_BUCKET}/backups/${ENVIRONMENT}/${BACKUP_FILE}"; then
            echo -e "${GREEN}✓ Uploaded to GCS${NC}"
            echo "  Bucket: ${GCS_BUCKET}"
        else
            echo -e "${RED}✗ GCS upload failed${NC}"
        fi
    else
        echo -e "${YELLOW}⚠ gsutil not found, skipping GCS upload${NC}"
    fi
fi

# Summary
echo ""
echo -e "${BLUE}============================================${NC}"
echo -e "${GREEN}✓ Backup completed successfully!${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""
echo "Backup file: ${BACKUP_DIR}/${BACKUP_FILE}"
echo "To restore: gunzip < ${BACKUP_DIR}/${BACKUP_FILE} | psql -h ${DB_HOST} -U ${DB_USER} ${DB_NAME}"
