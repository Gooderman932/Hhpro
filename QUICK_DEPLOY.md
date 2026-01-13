# 🚀 Quick Production Deployment Guide

**TL;DR**: Get your Construction Intelligence Platform running in production in under 30 minutes.

## ⚡ Prerequisites

- Ubuntu 20.04+ server with Docker & Docker Compose
- Domain name pointing to your server
- 4GB RAM, 2 CPU cores, 50GB storage minimum

## 🎯 5-Minute Setup (Without SSL)

Perfect for internal networks or testing:

```bash
# 1. Clone repository
git clone https://github.com/Gooderman932/market-data.git
cd market-data

# 2. Configure environment
cp .env.production .env
nano .env
# Change SECRET_KEY, POSTGRES_PASSWORD, REDIS_PASSWORD, ADMIN_PASSWORD

# 3. Deploy
./scripts/deployment/deploy.sh

# 4. Initialize database
make db-init
make db-seed  # Optional: sample data

# Done! Access at http://localhost
```

## 🔒 Full Production Setup (With SSL)

For public-facing production deployment:

### Step 1: Server Setup (5 min)

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Configure firewall
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### Step 2: Get the Code (2 min)

```bash
git clone https://github.com/Gooderman932/market-data.git
cd market-data
```

### Step 3: Configure (5 min)

```bash
# Copy environment template
cp .env.production .env

# Generate secrets
export SECRET_KEY=$(openssl rand -hex 32)
export POSTGRES_PASSWORD=$(openssl rand -base64 32)
export REDIS_PASSWORD=$(openssl rand -base64 32)

# Edit configuration
nano .env
# Update: SECRET_KEY, passwords, domain names, admin credentials
```

### Step 4: SSL Certificates (5 min)

```bash
# Install certbot
sudo apt-get install certbot

# Get certificates (replace with your domain)
sudo certbot certonly --standalone \
  -d yourdomain.com \
  --email you@example.com \
  --agree-tos

# Copy certificates
mkdir -p nginx/ssl
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem nginx/ssl/
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem nginx/ssl/
sudo cp /etc/letsencrypt/live/yourdomain.com/chain.pem nginx/ssl/
sudo chmod 644 nginx/ssl/*.pem
sudo chown $USER:$USER nginx/ssl/*.pem
```

### Step 5: Configure Nginx for HTTPS (3 min)

```bash
# Edit nginx config
nano nginx/nginx.conf

# Uncomment the HTTPS server block and update server_name to your domain
# Uncomment the HTTP to HTTPS redirect
```

### Step 6: Deploy (5 min)

```bash
# Deploy application
./scripts/deployment/deploy.sh

# Initialize database
make db-init
make db-seed  # Optional

# Verify health
./scripts/deployment/health-check.sh
```

### Step 7: Verify (5 min)

```bash
# Test HTTP redirect
curl -I http://yourdomain.com

# Test HTTPS
curl -I https://yourdomain.com

# Check all services
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

## 📋 Post-Deployment

### Set Up Automated Backups

```bash
# Set up daily backups at 2 AM
crontab -e
# Add: 0 2 * * * cd /path/to/market-data && ./scripts/deployment/backup.sh
```

### Enable Monitoring

```bash
# Add health check monitoring
crontab -e
# Add: */5 * * * * cd /path/to/market-data && ./scripts/deployment/health-check.sh >> /var/log/health-check.log 2>&1
```

### Set Up SSL Auto-Renewal

```bash
# Verify certbot timer is enabled
sudo systemctl status certbot.timer

# If not enabled:
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

## 🔧 Common Commands

```bash
# View logs
make logs

# Restart services
make restart

# Check health
./scripts/deployment/health-check.sh

# Create backup
make backup

# Update application
git pull origin main
./scripts/deployment/deploy.sh

# Access database
make shell-db
```

## 📊 Default Credentials

After seeding database:
- **Email**: demo@example.com
- **Password**: demo123

**⚠️ Change admin password immediately in production!**

## 🎯 Accessing Your Application

- **Frontend**: https://yourdomain.com
- **Backend API**: https://yourdomain.com/api/v1
- **Health Check**: https://yourdomain.com/health

## 🆘 Troubleshooting

### Services won't start
```bash
docker-compose -f docker-compose.prod.yml logs
```

### SSL certificate errors
```bash
# Verify certificates
ls -l nginx/ssl/
openssl x509 -in nginx/ssl/fullchain.pem -text -noout
```

### Database connection issues
```bash
docker-compose -f docker-compose.prod.yml exec postgres pg_isready
```

### High memory/CPU usage
```bash
docker stats
```

## 📚 Detailed Guides

- **Full deployment**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **SSL setup**: [SSL_SETUP.md](SSL_SETUP.md)
- **Security**: [SECURITY.md](SECURITY.md)
- **Checklist**: [PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md)

## 💡 Tips

1. **Always test in staging first** - Don't deploy directly to production
2. **Back up before updates** - Run `make backup` before deploying changes
3. **Monitor logs** - Check logs regularly: `make logs`
4. **Keep secrets secure** - Never commit .env files
5. **Update regularly** - Keep system and dependencies updated

## 🔐 Security Essentials

Before going live:
- [ ] Changed all default passwords
- [ ] Configured HTTPS with valid certificate
- [ ] Updated CORS origins
- [ ] Enabled firewall
- [ ] Set up backups
- [ ] Configured monitoring

## 📞 Need Help?

- Check documentation in `/docs`
- Review logs: `make logs`
- Run health check: `./scripts/deployment/health-check.sh`

---

**Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.**
