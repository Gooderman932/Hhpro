# ================================================
# OPTION 3: CUSTOM SUBDOMAIN CONFIGURATION
# ================================================
#
# This guide explains how to connect a subdomain
# (like pro.hdrywallrepair.com) to your platform
# ================================================

## STEP 1: Choose Your Subdomain

Recommended options:
- pro.hdrywallrepair.com (for the full platform)
- jobs.hdrywallrepair.com (job-focused)
- hire.hdrywallrepair.com (contractor-focused)
- shop.hdrywallrepair.com (e-commerce focused)

## STEP 2: DNS Configuration

Add a CNAME record in your domain registrar (GoDaddy, Namecheap, Cloudflare, etc.):

```
Type: CNAME
Name: pro (or your chosen subdomain)
Value: job-trade-match.preview.emergentagent.com
TTL: 3600 (or Auto)
```

### Example for common registrars:

**GoDaddy:**
1. Go to DNS Management
2. Click "Add" under Records
3. Select "CNAME"
4. Host: pro
5. Points to: job-trade-match.preview.emergentagent.com
6. Save

**Cloudflare:**
1. Go to DNS settings
2. Click "Add Record"
3. Type: CNAME
4. Name: pro
5. Target: job-trade-match.preview.emergentagent.com
6. Proxy status: DNS only (gray cloud) initially
7. Save

**Namecheap:**
1. Domain List → Manage → Advanced DNS
2. Add New Record
3. Type: CNAME
4. Host: pro
5. Value: job-trade-match.preview.emergentagent.com
6. Save

## STEP 3: Verify DNS Propagation

After adding the CNAME, verify it's working:

```bash
# Check DNS propagation (may take 5-30 minutes)
nslookup pro.hdrywallrepair.com

# Or use online tools:
# https://dnschecker.org
# https://mxtoolbox.com/DNSLookup.aspx
```

## STEP 4: Connect Custom Domain in Emergent

1. Go to Emergent Dashboard
2. Navigate to your project settings
3. Find "Custom Domain" or "Domain Settings"
4. Add your subdomain: pro.hdrywallrepair.com
5. Follow prompts to verify ownership
6. SSL certificate will be auto-provisioned

## STEP 5: Update Environment Variables

Once your custom domain is active, update the backend CORS settings:

```env
# In /app/backend/.env
CORS_ORIGINS="https://pro.hdrywallrepair.com,https://hdrywallrepair.com,*"
```

## ALTERNATIVE: Redirect Configuration

If you want hdrywallrepair.com/jobs to redirect to the platform:

### Option A: Server-side redirect (Apache .htaccess)
```apache
RewriteEngine On
RewriteRule ^jobs/?$ https://pro.hdrywallrepair.com/jobs [R=301,L]
RewriteRule ^workers/?$ https://pro.hdrywallrepair.com/workers [R=301,L]
RewriteRule ^shop/?$ https://pro.hdrywallrepair.com/shop [R=301,L]
```

### Option B: Server-side redirect (Nginx)
```nginx
location /jobs {
    return 301 https://pro.hdrywallrepair.com/jobs;
}
location /workers {
    return 301 https://pro.hdrywallrepair.com/workers;
}
location /shop {
    return 301 https://pro.hdrywallrepair.com/shop;
}
```

### Option C: JavaScript redirect (if you can't access server config)
```html
<script>
// Add to pages where you want to redirect
if (window.location.pathname === '/jobs') {
    window.location.href = 'https://pro.hdrywallrepair.com/jobs';
}
</script>
```

## TIMELINE

- DNS propagation: 5 minutes to 48 hours (usually under 30 minutes)
- SSL certificate: 5-15 minutes after DNS verification
- Full setup: Usually complete within 1 hour

## TROUBLESHOOTING

**"DNS not found" error:**
- Wait longer for propagation
- Verify CNAME record is correct
- Check for typos in subdomain name

**SSL certificate errors:**
- Ensure DNS is fully propagated first
- Check domain verification in Emergent dashboard
- May need to re-trigger certificate generation

**CORS errors after custom domain:**
- Update CORS_ORIGINS in backend/.env
- Restart backend service
- Clear browser cache

## CURRENT PLATFORM URL

Your platform is currently accessible at:
https://job-trade-match.preview.emergentagent.com

All links in Option 2 use this URL. Once you set up a custom domain,
replace all instances of the preview URL with your custom domain.
