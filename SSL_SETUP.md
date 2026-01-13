# SSL/TLS Certificate Setup Guide

This guide covers setting up SSL/TLS certificates for the Construction Intelligence Platform.

## 🔒 Overview

SSL/TLS certificates are **required** for production deployment to:
- Encrypt data in transit
- Enable HTTPS
- Build user trust
- Meet security compliance

## 🎯 Options

### Option 1: Let's Encrypt (Recommended for Production)

**Pros:**
- Free
- Automated renewal
- Trusted by all browsers
- Easy setup with certbot

**Cons:**
- Requires a public domain
- 90-day validity (auto-renews)

### Option 2: Commercial Certificate

**Pros:**
- Extended validation available
- Longer validity periods
- Premium support

**Cons:**
- Costs money
- Manual renewal process

### Option 3: Self-Signed (Development Only)

**Pros:**
- Free
- No domain required
- Quick setup

**Cons:**
- Browser warnings
- Not trusted
- Only for testing

## 🚀 Let's Encrypt Setup (Recommended)

### Prerequisites

- Public domain name pointing to your server
- Ports 80 and 443 accessible from the internet
- Email address for renewal notifications

### Step 1: Install Certbot

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install certbot

# CentOS/RHEL
sudo yum install certbot
```

### Step 2: Obtain Certificates

**Standalone Mode (services must be stopped):**

```bash
# Stop nginx if running
docker-compose -f docker-compose.prod.yml stop nginx

# Obtain certificate
sudo certbot certonly --standalone \
  -d yourdomain.com \
  -d www.yourdomain.com \
  --email your-email@example.com \
  --agree-tos \
  --non-interactive
```

**Webroot Mode (services can keep running):**

```bash
# Create webroot directory
sudo mkdir -p /var/www/certbot

# Obtain certificate
sudo certbot certonly --webroot \
  -w /var/www/certbot \
  -d yourdomain.com \
  -d www.yourdomain.com \
  --email your-email@example.com \
  --agree-tos \
  --non-interactive
```

### Step 3: Copy Certificates

```bash
# Create SSL directory
mkdir -p nginx/ssl

# Copy certificates
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem nginx/ssl/
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem nginx/ssl/
sudo cp /etc/letsencrypt/live/yourdomain.com/chain.pem nginx/ssl/

# Set permissions
sudo chmod 644 nginx/ssl/fullchain.pem
sudo chmod 600 nginx/ssl/privkey.pem
sudo chmod 644 nginx/ssl/chain.pem

# Change ownership (optional, for non-root access)
sudo chown $USER:$USER nginx/ssl/*
```

### Step 4: Configure Nginx

Edit `nginx/nginx.conf` and uncomment the HTTPS server block:

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL certificates
    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;
    ssl_trusted_certificate /etc/nginx/ssl/chain.pem;
    
    # ... rest of configuration
}
```

Also uncomment the HTTP to HTTPS redirect:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    location / {
        return 301 https://$host$request_uri;
    }
}
```

### Step 5: Restart Services

```bash
# Restart nginx
docker-compose -f docker-compose.prod.yml restart nginx

# Or restart all services
docker-compose -f docker-compose.prod.yml restart
```

### Step 6: Verify HTTPS

```bash
# Test HTTP to HTTPS redirect
curl -I http://yourdomain.com

# Test HTTPS
curl -I https://yourdomain.com

# Test SSL configuration
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com
```

### Step 7: Set Up Auto-Renewal

Certbot automatically installs a systemd timer for renewal. Verify it:

```bash
# Check renewal timer
sudo systemctl status certbot.timer

# Test renewal (dry run)
sudo certbot renew --dry-run
```

**Manual Cron Job (alternative):**

```bash
# Edit crontab
crontab -e

# Add renewal job (runs twice daily)
0 0,12 * * * /usr/bin/certbot renew --quiet --deploy-hook "docker-compose -f /path/to/market-data/docker-compose.prod.yml restart nginx"
```

## 🔨 Self-Signed Certificate (Development)

**⚠️ WARNING: Only use for development/testing!**

### Generate Self-Signed Certificate

```bash
# Create SSL directory
mkdir -p nginx/ssl

# Generate certificate (valid for 365 days)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/privkey.pem \
  -out nginx/ssl/fullchain.pem \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

# Create chain file (empty for self-signed)
touch nginx/ssl/chain.pem

# Set permissions
chmod 600 nginx/ssl/privkey.pem
chmod 644 nginx/ssl/fullchain.pem
```

### Configure for Self-Signed

When using self-signed certificates, browsers will show security warnings. You'll need to manually accept them.

## 💼 Commercial Certificate

### Step 1: Generate CSR

```bash
# Generate private key and CSR
openssl req -new -newkey rsa:2048 -nodes \
  -keyout nginx/ssl/privkey.pem \
  -out nginx/ssl/server.csr \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=yourdomain.com"
```

### Step 2: Purchase Certificate

Submit the CSR (`server.csr`) to your certificate authority (CA):
- DigiCert
- Comodo
- GeoTrust
- Others

### Step 3: Install Certificates

After receiving the certificates from your CA:

```bash
# Copy the certificate files
cp certificate.crt nginx/ssl/fullchain.pem
cp ca-bundle.crt nginx/ssl/chain.pem
# privkey.pem should already exist from step 1
```

### Step 4: Configure and Restart

Follow steps 4-6 from the Let's Encrypt setup.

## 🔍 Testing SSL Configuration

### Online Tools

- [SSL Labs Server Test](https://www.ssllabs.com/ssltest/)
- [SSL Checker](https://www.sslshopper.com/ssl-checker.html)

### Command Line

```bash
# Check certificate details
openssl x509 -in nginx/ssl/fullchain.pem -text -noout

# Test SSL connection
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com

# Check certificate expiration
openssl x509 -in nginx/ssl/fullchain.pem -noout -enddate

# Verify certificate chain
openssl verify -CAfile nginx/ssl/chain.pem nginx/ssl/fullchain.pem
```

## 🔄 Certificate Renewal

### Let's Encrypt (Automatic)

Certbot handles renewal automatically via systemd timer. Just ensure it's enabled:

```bash
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

### Manual Renewal

```bash
# Renew certificates
sudo certbot renew

# Copy renewed certificates
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem nginx/ssl/
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem nginx/ssl/
sudo cp /etc/letsencrypt/live/yourdomain.com/chain.pem nginx/ssl/

# Restart nginx
docker-compose -f docker-compose.prod.yml restart nginx
```

### Monitoring Expiration

Set up monitoring to alert before certificates expire:

```bash
# Check expiration date
openssl x509 -in nginx/ssl/fullchain.pem -noout -enddate

# Create monitoring script
cat > scripts/deployment/check-ssl-expiry.sh << 'EOF'
#!/bin/bash
CERT_FILE="nginx/ssl/fullchain.pem"
EXPIRY_DATE=$(openssl x509 -in "$CERT_FILE" -noout -enddate | cut -d= -f2)
EXPIRY_EPOCH=$(date -d "$EXPIRY_DATE" +%s)
NOW_EPOCH=$(date +%s)
DAYS_LEFT=$(( ($EXPIRY_EPOCH - $NOW_EPOCH) / 86400 ))

echo "SSL Certificate expires in $DAYS_LEFT days"

if [ $DAYS_LEFT -lt 30 ]; then
    echo "WARNING: Certificate expires soon!"
    # Send alert (email, Slack, etc.)
fi
EOF

chmod +x scripts/deployment/check-ssl-expiry.sh
```

## 🛡️ Security Best Practices

### Strong SSL Configuration

Already configured in `nginx/nginx.conf`:

```nginx
# Modern SSL protocols only
ssl_protocols TLSv1.2 TLSv1.3;

# Strong ciphers
ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';

# Prefer server ciphers
ssl_prefer_server_ciphers off;

# Session cache
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m;

# OCSP Stapling
ssl_stapling on;
ssl_stapling_verify on;

# HSTS
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

### Certificate Security

```bash
# Protect private keys
chmod 600 nginx/ssl/privkey.pem

# Public certificates can be readable
chmod 644 nginx/ssl/fullchain.pem
chmod 644 nginx/ssl/chain.pem
```

## 🆘 Troubleshooting

### "Certificate not trusted" errors

**Cause:** Self-signed certificate or incomplete certificate chain

**Solution:**
- Use Let's Encrypt or commercial CA for production
- Ensure chain.pem is correctly configured
- Verify certificate installation

### "Certificate expired" errors

**Cause:** Certificate has passed its validity period

**Solution:**
```bash
# Renew certificate
sudo certbot renew

# Update copied certificates
sudo cp /etc/letsencrypt/live/yourdomain.com/* nginx/ssl/

# Restart nginx
docker-compose -f docker-compose.prod.yml restart nginx
```

### Port 443 connection refused

**Cause:** Nginx not listening on 443 or firewall blocking

**Solution:**
```bash
# Check if nginx is listening
netstat -tlnp | grep 443

# Check firewall
sudo ufw status
sudo ufw allow 443/tcp

# Check nginx configuration
docker-compose -f docker-compose.prod.yml exec nginx nginx -t
```

## 📚 Additional Resources

- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
- [Certbot Documentation](https://certbot.eff.org/docs/)
- [SSL Labs Best Practices](https://github.com/ssllabs/research/wiki/SSL-and-TLS-Deployment-Best-Practices)

---

**Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.**
