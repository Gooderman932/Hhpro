# 🚀 Production Deployment Guide

This guide provides step-by-step instructions for deploying the Construction Intelligence Platform to production.

## 📋 Prerequisites

Before deploying to production, ensure you have:

- [ ] A server with Docker and Docker Compose installed (Ubuntu 20.04+ recommended)
- [ ] Domain name configured with DNS pointing to your server
- [ ] SSL/TLS certificates (Let's Encrypt recommended)
- [ ] Minimum 4GB RAM, 2 CPU cores, 50GB storage
- [ ] PostgreSQL 16 compatible environment
- [ ] Access to OpenAI API (optional, for ML features)

## 🔐 Security Checklist

Before deployment:

- [ ] Generate a strong SECRET_KEY (at least 32 characters)
- [ ] Set secure passwords for PostgreSQL and Redis
- [ ] Configure firewall rules (allow only 80, 443, and SSH)
- [ ] Set up SSL/TLS certificates
- [ ] Review and update CORS_ORIGINS
- [ ] Change default admin credentials
- [ ] Enable rate limiting in nginx
- [ ] Configure backup strategy
- [ ] Set up monitoring and alerting

## 📦 Deployment Steps

### 1. Clone Repository

```bash
git clone https://github.com/Gooderman932/market-data.git
cd market-data
```

### 2. Configure Environment

```bash
# Copy production environment template
cp .env.production .env

# Edit the configuration file
nano .env
```

**Required Configuration:**
```bash
# Generate a secure secret key
SECRET_KEY=$(openssl rand -hex 32)

# Set strong passwords
POSTGRES_PASSWORD=$(openssl rand -base64 32)
REDIS_PASSWORD=$(openssl rand -base64 32)

# Configure your domain
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
FRONTEND_URL=https://yourdomain.com
BACKEND_URL=https://api.yourdomain.com
VITE_API_URL=https://api.yourdomain.com

# Set admin credentials
ADMIN_EMAIL=admin@yourdomain.com
ADMIN_PASSWORD=$(openssl rand -base64 16)
```

### 3. Configure SSL/TLS

#### Option A: Let's Encrypt (Recommended)

```bash
# Install certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificates
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Copy certificates
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem nginx/ssl/
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem nginx/ssl/
sudo cp /etc/letsencrypt/live/yourdomain.com/chain.pem nginx/ssl/
```

#### Option B: Self-Signed (Development Only)

```bash
# Generate self-signed certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/privkey.pem \
  -out nginx/ssl/fullchain.pem
```

### 4. Update Nginx Configuration

Uncomment the HTTPS server block in `nginx/nginx.conf` and update `server_name`:

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    # ... rest of SSL configuration
}
```

### 5. Deploy Application

```bash
# Make deployment script executable (if not already)
chmod +x scripts/deployment/deploy.sh

# Run deployment
./scripts/deployment/deploy.sh
```

The script will:
1. Validate environment configuration
2. Build Docker images
3. Start all services
4. Run database migrations
5. Verify health checks

### 6. Initialize Database

```bash
# Run database setup
docker-compose -f docker-compose.prod.yml exec backend python scripts/setup_db.py

# Seed sample data (optional)
docker-compose -f docker-compose.prod.yml exec backend python scripts/seed_data.py
```

### 7. Verify Deployment

Check that all services are running:

```bash
docker-compose -f docker-compose.prod.yml ps
```

Test the health endpoint:

```bash
curl http://localhost/health
# Should return: healthy
```

Access the application:
- Frontend: https://yourdomain.com
- Backend API: https://api.yourdomain.com
- API Docs: https://api.yourdomain.com/api/docs (if DEBUG=true)

## 🔄 Updates and Maintenance

### Updating the Application

```bash
# Run the deployment script
./scripts/deployment/deploy.sh
```

### Database Backups

Set up automated backups:

```bash
# Make backup script executable
chmod +x scripts/deployment/backup.sh

# Run manual backup
./scripts/deployment/backup.sh

# Set up cron job for daily backups
crontab -e
# Add: 0 2 * * * cd /path/to/market-data && ./scripts/deployment/backup.sh
```

### Viewing Logs

```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f frontend
docker-compose -f docker-compose.prod.yml logs -f nginx
```

### Restarting Services

```bash
# Restart all services
docker-compose -f docker-compose.prod.yml restart

# Restart specific service
docker-compose -f docker-compose.prod.yml restart backend
```

## 📊 Monitoring

### Health Checks

The application includes health check endpoints:

- Main health: `http://localhost/health`
- Backend health: `http://localhost:8000/health`

### Resource Monitoring

```bash
# Container resource usage
docker stats

# Disk usage
docker system df
```

### Database Monitoring

```bash
# Connect to PostgreSQL
docker-compose -f docker-compose.prod.yml exec postgres psql -U buildintel_user -d construction_intel

# Check database size
\l+

# Check table sizes
\dt+
```

## 🔒 Security Hardening

### Firewall Configuration

```bash
# Ubuntu UFW
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### Regular Updates

```bash
# Update Docker images
docker-compose -f docker-compose.prod.yml pull

# Update system packages
sudo apt-get update && sudo apt-get upgrade
```

### SSL Certificate Renewal

```bash
# Renew Let's Encrypt certificates
sudo certbot renew

# Set up auto-renewal (certbot usually does this automatically)
sudo systemctl enable certbot.timer
```

## 🆘 Troubleshooting

### Services Won't Start

```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs

# Check individual service
docker-compose -f docker-compose.prod.yml logs backend
```

### Database Connection Issues

```bash
# Check if PostgreSQL is running
docker-compose -f docker-compose.prod.yml exec postgres pg_isready

# Verify credentials in .env
cat .env | grep POSTGRES
```

### SSL Certificate Issues

```bash
# Verify certificate files exist
ls -l nginx/ssl/

# Check nginx configuration
docker-compose -f docker-compose.prod.yml exec nginx nginx -t
```

### High Memory Usage

```bash
# Check container memory usage
docker stats

# Restart memory-heavy services
docker-compose -f docker-compose.prod.yml restart backend
```

## 📞 Support

For issues or questions:
- Review logs: `docker-compose -f docker-compose.prod.yml logs`
- Check documentation in `/docs` directory
- Contact support: support@yourdomain.com

## 📄 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)

---

**Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.**
