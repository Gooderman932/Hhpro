# API Integration Guide

**BuildIntel Pro - Third-Party Developer Documentation**

Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.

Version: 1.0.0  
Last Updated: January 2025

---

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Authentication](#authentication)
- [Core Endpoints](#core-endpoints)
- [Code Examples](#code-examples)
- [Rate Limiting](#rate-limiting)
- [Error Handling](#error-handling)
- [Webhooks](#webhooks)
- [Best Practices](#best-practices)
- [Support](#support)

---

## Overview

### Introduction

The BuildIntel Pro API provides programmatic access to construction market intelligence data. This RESTful API allows you to:

- Retrieve project data
- Access analytics and insights
- Integrate with your existing systems
- Automate data workflows
- Build custom applications

### Base URLs

**Production:**
```
https://api.buildintel.com
```

**Staging:**
```
https://api-staging.buildintel.com
```

**Development (Local):**
```
http://localhost:8000
```

### API Version

Current version: **v1**

All endpoints are prefixed with `/api/v1/`

### Authentication Methods

- **JWT Bearer Tokens** (Primary method)
- **API Keys** (Enterprise plans)
- **OAuth 2.0** (Third-party applications)

### API Documentation

Interactive API documentation is available at:
- **Swagger UI**: `https://api.buildintel.com/api/docs`
- **ReDoc**: `https://api.buildintel.com/api/redoc`

---

## Quick Start

### 1. Obtain API Credentials

#### For JWT Authentication:
1. Log in to your BuildIntel Pro account
2. Navigate to **Settings > API Access**
3. Click **"Generate API Key"**
4. Save your credentials securely

#### For OAuth 2.0:
1. Go to **Settings > Developer Apps**
2. Click **"Create Application"**
3. Configure redirect URIs
4. Note your Client ID and Client Secret

### 2. Get an Access Token

**Request:**
```bash
curl -X POST "https://api.buildintel.com/api/v1/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=your_email@example.com&password=your_password"
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### 3. Make Your First API Call

**Request:**
```bash
curl -X GET "https://api.buildintel.com/api/v1/projects" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "items": [
    {
      "id": 1,
      "title": "Commercial Office Building",
      "sector": "commercial",
      "value": 5000000,
      "status": "active",
      "city": "New York",
      "state": "NY"
    }
  ],
  "total": 142,
  "page": 1,
  "per_page": 10
}
```

---

## Authentication

### JWT Bearer Token Authentication

#### Obtaining a Token

**Endpoint:** `POST /api/v1/auth/token`

**Request:**
```json
{
  "username": "user@example.com",
  "password": "your_password"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyQGV4YW1wbGUuY29tIiwiZXhwIjoxNjQwOTk1MjAwfQ.signature",
  "token_type": "bearer",
  "expires_in": 1800
}
```

**Token Expiration:**
- Access tokens expire after **30 minutes**
- Refresh tokens expire after **7 days**

#### Using the Token

Include the token in the `Authorization` header:

```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

#### Refreshing Tokens

**Endpoint:** `POST /api/v1/auth/refresh`

**Request:**
```json
{
  "refresh_token": "your_refresh_token"
}
```

**Response:**
```json
{
  "access_token": "new_access_token",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### API Key Authentication (Enterprise)

**Using API Keys:**

Include your API key in the `X-API-Key` header:

```
X-API-Key: your_api_key_here
```

**Example:**
```bash
curl -X GET "https://api.buildintel.com/api/v1/projects" \
  -H "X-API-Key: sk_live_abc123xyz789"
```

### OAuth 2.0 (Third-Party Apps)

#### Authorization Code Flow

1. **Redirect user to authorization URL:**
```
https://api.buildintel.com/oauth/authorize?
  client_id=YOUR_CLIENT_ID&
  redirect_uri=YOUR_REDIRECT_URI&
  response_type=code&
  scope=read:projects write:projects
```

2. **Exchange authorization code for token:**
```bash
curl -X POST "https://api.buildintel.com/oauth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code" \
  -d "code=AUTHORIZATION_CODE" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET" \
  -d "redirect_uri=YOUR_REDIRECT_URI"
```

3. **Use access token:**
```bash
curl -X GET "https://api.buildintel.com/api/v1/projects" \
  -H "Authorization: Bearer ACCESS_TOKEN"
```

---

## Core Endpoints

### Projects

#### List Projects

**Endpoint:** `GET /api/v1/projects`

**Query Parameters:**
- `sector` (string): Filter by sector (commercial, residential, infrastructure, industrial)
- `status` (string): Filter by status (active, awarded, completed, cancelled)
- `state` (string): Filter by state (e.g., "NY", "CA")
- `city` (string): Filter by city
- `min_value` (number): Minimum project value
- `max_value` (number): Maximum project value
- `page` (number): Page number (default: 1)
- `per_page` (number): Items per page (default: 10, max: 100)

**Example Request:**
```bash
curl -X GET "https://api.buildintel.com/api/v1/projects?sector=commercial&status=active&min_value=1000000&page=1&per_page=20" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**
```json
{
  "items": [
    {
      "id": 1,
      "title": "Downtown Office Tower",
      "description": "50-story mixed-use development",
      "project_type": "opportunity",
      "sector": "commercial",
      "status": "active",
      "value": 125000000,
      "estimated_start_date": "2025-06-01T00:00:00Z",
      "estimated_completion_date": "2027-12-31T00:00:00Z",
      "address": "123 Main Street",
      "city": "New York",
      "state": "NY",
      "zip_code": "10001",
      "latitude": 40.7128,
      "longitude": -74.0060,
      "created_at": "2025-01-01T10:00:00Z",
      "updated_at": "2025-01-09T15:30:00Z"
    }
  ],
  "total": 142,
  "page": 1,
  "per_page": 20,
  "total_pages": 8
}
```

#### Get Project Details

**Endpoint:** `GET /api/v1/projects/{project_id}`

**Example Request:**
```bash
curl -X GET "https://api.buildintel.com/api/v1/projects/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "title": "Downtown Office Tower",
  "description": "50-story mixed-use development with retail, office, and residential space",
  "project_type": "opportunity",
  "sector": "commercial",
  "status": "active",
  "value": 125000000,
  "estimated_start_date": "2025-06-01T00:00:00Z",
  "estimated_completion_date": "2027-12-31T00:00:00Z",
  "address": "123 Main Street",
  "city": "New York",
  "state": "NY",
  "zip_code": "10001",
  "country": "USA",
  "latitude": 40.7128,
  "longitude": -74.0060,
  "source": "Construction Permits DB",
  "source_url": "https://example.com/permit/12345",
  "is_verified": true,
  "participations": [
    {
      "company_id": 5,
      "company_name": "ABC Construction",
      "role": "general_contractor",
      "status": "bidding"
    }
  ],
  "opportunity_score": {
    "overall_score": 0.85,
    "value_score": 0.90,
    "fit_score": 0.80,
    "competition_score": 0.75
  },
  "created_at": "2025-01-01T10:00:00Z",
  "updated_at": "2025-01-09T15:30:00Z"
}
```

#### Create Project

**Endpoint:** `POST /api/v1/projects`

**Request Body:**
```json
{
  "title": "New Residential Complex",
  "description": "200-unit apartment building",
  "project_type": "opportunity",
  "sector": "residential",
  "value": 25000000,
  "estimated_start_date": "2025-09-01",
  "city": "Los Angeles",
  "state": "CA",
  "zip_code": "90001"
}
```

**Response:**
```json
{
  "id": 143,
  "title": "New Residential Complex",
  "status": "active",
  "created_at": "2025-01-09T16:00:00Z",
  "message": "Project created successfully"
}
```

### Analytics

#### Get Market Summary

**Endpoint:** `GET /api/v1/analytics/summary`

**Query Parameters:**
- `start_date` (string): Start date (ISO 8601 format)
- `end_date` (string): End date (ISO 8601 format)
- `sector` (string): Filter by sector
- `state` (string): Filter by state

**Example Request:**
```bash
curl -X GET "https://api.buildintel.com/api/v1/analytics/summary?start_date=2024-01-01&end_date=2025-01-01&sector=commercial" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**
```json
{
  "period": {
    "start_date": "2024-01-01",
    "end_date": "2025-01-01"
  },
  "summary": {
    "total_projects": 1247,
    "total_value": 3450000000,
    "average_value": 2767221,
    "median_value": 1500000,
    "active_projects": 342,
    "awarded_projects": 567,
    "completed_projects": 338
  },
  "by_sector": {
    "commercial": {
      "count": 456,
      "total_value": 1890000000
    },
    "residential": {
      "count": 523,
      "total_value": 980000000
    },
    "infrastructure": {
      "count": 268,
      "total_value": 580000000
    }
  }
}
```

#### Get Trend Analysis

**Endpoint:** `GET /api/v1/analytics/trends`

**Query Parameters:**
- `metric` (string): Metric to analyze (count, value, average_value)
- `period` (string): Time period (daily, weekly, monthly)
- `start_date` (string): Start date
- `end_date` (string): End date
- `sector` (string): Filter by sector (optional)

**Example Request:**
```bash
curl -X GET "https://api.buildintel.com/api/v1/analytics/trends?metric=count&period=monthly&start_date=2024-01-01&end_date=2025-01-01" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**
```json
{
  "metric": "count",
  "period": "monthly",
  "data": [
    {
      "date": "2024-01",
      "value": 87,
      "change_percent": 5.2
    },
    {
      "date": "2024-02",
      "value": 92,
      "change_percent": 5.7
    },
    {
      "date": "2024-03",
      "value": 103,
      "change_percent": 11.9
    }
  ]
}
```

### Intelligence

#### Get Competitor Analysis

**Endpoint:** `GET /api/v1/intelligence/competitors`

**Query Parameters:**
- `company_id` (number): Specific company to analyze
- `sector` (string): Filter by sector
- `state` (string): Filter by state
- `start_date` (string): Analysis start date
- `end_date` (string): Analysis end date

**Example Request:**
```bash
curl -X GET "https://api.buildintel.com/api/v1/intelligence/competitors?sector=commercial&state=NY" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**
```json
{
  "competitors": [
    {
      "company_id": 25,
      "company_name": "ABC Construction",
      "project_count": 45,
      "total_value": 234000000,
      "win_rate": 0.67,
      "average_project_value": 5200000,
      "sectors": ["commercial", "industrial"],
      "top_regions": ["NY", "NJ", "CT"]
    },
    {
      "company_id": 18,
      "company_name": "XYZ Builders",
      "project_count": 38,
      "total_value": 198000000,
      "win_rate": 0.71,
      "average_project_value": 5210526,
      "sectors": ["commercial", "residential"],
      "top_regions": ["NY", "PA"]
    }
  ],
  "market_insights": {
    "total_competitors": 127,
    "market_concentration": 0.34,
    "average_win_rate": 0.58
  }
}
```

#### Get Market Share

**Endpoint:** `GET /api/v1/intelligence/market-share`

**Query Parameters:**
- `sector` (string): Sector to analyze
- `region` (string): Geographic region
- `start_date` (string): Analysis start date
- `end_date` (string): Analysis end date
- `metric` (string): count or value (default: value)

**Example Request:**
```bash
curl -X GET "https://api.buildintel.com/api/v1/intelligence/market-share?sector=commercial&region=NY&metric=value" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**
```json
{
  "sector": "commercial",
  "region": "NY",
  "metric": "value",
  "market_share": [
    {
      "rank": 1,
      "company_id": 25,
      "company_name": "ABC Construction",
      "share_percent": 18.5,
      "total_value": 456000000
    },
    {
      "rank": 2,
      "company_id": 18,
      "company_name": "XYZ Builders",
      "share_percent": 14.2,
      "total_value": 350000000
    },
    {
      "rank": 3,
      "company_id": 42,
      "company_name": "BuildCorp Inc",
      "share_percent": 11.8,
      "total_value": 291000000
    }
  ],
  "total_market_value": 2465000000
}
```

---

## Code Examples

### Python

```python
import requests
from typing import Optional, Dict, Any

class BuildIntelAPI:
    """BuildIntel Pro API Client"""
    
    def __init__(self, email: str, password: str, base_url: str = "https://api.buildintel.com"):
        self.base_url = base_url
        self.email = email
        self.password = password
        self.access_token: Optional[str] = None
        self.authenticate()
    
    def authenticate(self) -> None:
        """Obtain access token"""
        response = requests.post(
            f"{self.base_url}/api/v1/auth/token",
            data={"username": self.email, "password": self.password}
        )
        response.raise_for_status()
        data = response.json()
        self.access_token = data["access_token"]
    
    def _get_headers(self) -> Dict[str, str]:
        """Get authentication headers"""
        return {"Authorization": f"Bearer {self.access_token}"}
    
    def get_projects(self, **filters) -> Dict[str, Any]:
        """Get list of projects with optional filters"""
        response = requests.get(
            f"{self.base_url}/api/v1/projects",
            headers=self._get_headers(),
            params=filters
        )
        response.raise_for_status()
        return response.json()
    
    def get_project(self, project_id: int) -> Dict[str, Any]:
        """Get details of a specific project"""
        response = requests.get(
            f"{self.base_url}/api/v1/projects/{project_id}",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def create_project(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new project"""
        response = requests.post(
            f"{self.base_url}/api/v1/projects",
            headers=self._get_headers(),
            json=project_data
        )
        response.raise_for_status()
        return response.json()
    
    def get_analytics_summary(self, start_date: str, end_date: str, **filters) -> Dict[str, Any]:
        """Get market analytics summary"""
        params = {"start_date": start_date, "end_date": end_date, **filters}
        response = requests.get(
            f"{self.base_url}/api/v1/analytics/summary",
            headers=self._get_headers(),
            params=params
        )
        response.raise_for_status()
        return response.json()

# Usage example
if __name__ == "__main__":
    # Initialize client
    client = BuildIntelAPI(
        email="your_email@example.com",
        password="your_password"
    )
    
    # Get commercial projects in NY
    projects = client.get_projects(
        sector="commercial",
        state="NY",
        status="active",
        min_value=1000000
    )
    
    print(f"Found {projects['total']} projects")
    for project in projects['items']:
        print(f"  - {project['title']}: ${project['value']:,}")
    
    # Get market summary
    summary = client.get_analytics_summary(
        start_date="2024-01-01",
        end_date="2025-01-01",
        sector="commercial"
    )
    
    print(f"\nMarket Summary:")
    print(f"  Total Projects: {summary['summary']['total_projects']}")
    print(f"  Total Value: ${summary['summary']['total_value']:,}")
```

### JavaScript/Node.js

```javascript
const axios = require('axios');

class BuildIntelAPI {
  constructor(email, password, baseURL = 'https://api.buildintel.com') {
    this.baseURL = baseURL;
    this.email = email;
    this.password = password;
    this.accessToken = null;
  }

  async authenticate() {
    const response = await axios.post(`${this.baseURL}/api/v1/auth/token`, 
      new URLSearchParams({
        username: this.email,
        password: this.password
      })
    );
    this.accessToken = response.data.access_token;
  }

  getHeaders() {
    return {
      'Authorization': `Bearer ${this.accessToken}`
    };
  }

  async getProjects(filters = {}) {
    const response = await axios.get(`${this.baseURL}/api/v1/projects`, {
      headers: this.getHeaders(),
      params: filters
    });
    return response.data;
  }

  async getProject(projectId) {
    const response = await axios.get(
      `${this.baseURL}/api/v1/projects/${projectId}`,
      { headers: this.getHeaders() }
    );
    return response.data;
  }

  async createProject(projectData) {
    const response = await axios.post(
      `${this.baseURL}/api/v1/projects`,
      projectData,
      { headers: this.getHeaders() }
    );
    return response.data;
  }

  async getAnalyticsSummary(startDate, endDate, filters = {}) {
    const response = await axios.get(
      `${this.baseURL}/api/v1/analytics/summary`,
      {
        headers: this.getHeaders(),
        params: { start_date: startDate, end_date: endDate, ...filters }
      }
    );
    return response.data;
  }
}

// Usage example
(async () => {
  // Initialize client
  const client = new BuildIntelAPI(
    'your_email@example.com',
    'your_password'
  );
  
  // Authenticate
  await client.authenticate();
  
  // Get projects
  const projects = await client.getProjects({
    sector: 'commercial',
    state: 'NY',
    status: 'active',
    min_value: 1000000
  });
  
  console.log(`Found ${projects.total} projects`);
  projects.items.forEach(project => {
    console.log(`  - ${project.title}: $${project.value.toLocaleString()}`);
  });
  
  // Get analytics
  const summary = await client.getAnalyticsSummary(
    '2024-01-01',
    '2025-01-01',
    { sector: 'commercial' }
  );
  
  console.log('\nMarket Summary:');
  console.log(`  Total Projects: ${summary.summary.total_projects}`);
  console.log(`  Total Value: $${summary.summary.total_value.toLocaleString()}`);
})();
```

### cURL Examples

```bash
# Get access token
curl -X POST "https://api.buildintel.com/api/v1/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=your_email@example.com&password=your_password"

# Store token in variable
TOKEN="your_access_token_here"

# List projects with filters
curl -X GET "https://api.buildintel.com/api/v1/projects?sector=commercial&state=NY&status=active&min_value=1000000&page=1&per_page=20" \
  -H "Authorization: Bearer $TOKEN"

# Get specific project
curl -X GET "https://api.buildintel.com/api/v1/projects/1" \
  -H "Authorization: Bearer $TOKEN"

# Create new project
curl -X POST "https://api.buildintel.com/api/v1/projects" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Office Building",
    "description": "20-story office complex",
    "project_type": "opportunity",
    "sector": "commercial",
    "value": 45000000,
    "city": "Boston",
    "state": "MA"
  }'

# Get analytics summary
curl -X GET "https://api.buildintel.com/api/v1/analytics/summary?start_date=2024-01-01&end_date=2025-01-01&sector=commercial" \
  -H "Authorization: Bearer $TOKEN"

# Get competitor analysis
curl -X GET "https://api.buildintel.com/api/v1/intelligence/competitors?sector=commercial&state=NY" \
  -H "Authorization: Bearer $TOKEN"
```

---

## Rate Limiting

### Rate Limits by Plan

| Plan | Requests/Minute | Requests/Hour | Requests/Day |
|------|-----------------|---------------|--------------|
| Free Trial | 30 | 500 | 5,000 |
| Professional | 60 | 1,000 | 10,000 |
| Enterprise | 120 | 5,000 | 50,000 |

### Rate Limit Headers

Every API response includes rate limit information:

```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 57
X-RateLimit-Reset: 1640995200
```

### Handling Rate Limits

When rate limit is exceeded, you'll receive a `429 Too Many Requests` response:

```json
{
  "error": "rate_limit_exceeded",
  "message": "Rate limit exceeded. Please wait 45 seconds before retrying.",
  "retry_after": 45
}
```

**Best Practice:**
```python
import time
import requests

def make_api_request(url, headers):
    response = requests.get(url, headers=headers)
    
    if response.status_code == 429:
        retry_after = int(response.headers.get('Retry-After', 60))
        print(f"Rate limited. Waiting {retry_after} seconds...")
        time.sleep(retry_after)
        return make_api_request(url, headers)  # Retry
    
    return response
```

---

## Error Handling

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Invalid or expired token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 422 | Unprocessable Entity - Validation error |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error |
| 503 | Service Unavailable |

### Error Response Format

All errors follow this format:

```json
{
  "error": "error_code",
  "message": "Human-readable error message",
  "details": {
    "field": "Additional context"
  }
}
```

### Common Errors

#### Authentication Error (401)
```json
{
  "error": "invalid_token",
  "message": "Access token is invalid or expired"
}
```

#### Validation Error (422)
```json
{
  "error": "validation_error",
  "message": "Request validation failed",
  "details": [
    {
      "field": "value",
      "message": "value must be a positive number"
    },
    {
      "field": "sector",
      "message": "sector must be one of: commercial, residential, infrastructure, industrial"
    }
  ]
}
```

#### Not Found Error (404)
```json
{
  "error": "not_found",
  "message": "Project with id 999 not found"
}
```

### Error Handling Example

```python
import requests

try:
    response = requests.get(
        "https://api.buildintel.com/api/v1/projects/999",
        headers={"Authorization": f"Bearer {token}"}
    )
    response.raise_for_status()
    project = response.json()
    
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 401:
        print("Authentication failed. Please refresh your token.")
    elif e.response.status_code == 404:
        print("Project not found.")
    elif e.response.status_code == 422:
        errors = e.response.json()
        print(f"Validation errors: {errors['details']}")
    elif e.response.status_code == 429:
        print("Rate limit exceeded. Please wait before retrying.")
    else:
        print(f"API error: {e.response.status_code}")
        
except requests.exceptions.RequestException as e:
    print(f"Network error: {e}")
```

---

## Webhooks (Enterprise)

### Overview

Webhooks allow you to receive real-time notifications when events occur in BuildIntel Pro.

**Available for:** Enterprise plans only

### Setting Up Webhooks

1. Go to **Settings > Webhooks**
2. Click **"Add Webhook"**
3. Configure:
   - **Endpoint URL**: Your webhook receiver URL
   - **Events**: Select events to subscribe to
   - **Secret**: Generate signing secret
4. Save configuration

### Supported Events

- `project.created` - New project added
- `project.updated` - Project modified
- `project.deleted` - Project removed
- `project.status_changed` - Project status changed
- `competitor.activity` - Competitor activity detected
- `alert.triggered` - Custom alert triggered

### Webhook Payload Format

```json
{
  "event": "project.created",
  "timestamp": "2025-01-09T16:30:00Z",
  "data": {
    "project_id": 143,
    "title": "New Commercial Project",
    "sector": "commercial",
    "value": 5000000
  },
  "signature": "sha256=abc123..."
}
```

### Verifying Webhook Signatures

```python
import hashlib
import hmac

def verify_webhook_signature(payload, signature, secret):
    """Verify webhook signature"""
    expected_signature = hmac.new(
        secret.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(
        f"sha256={expected_signature}",
        signature
    )

# Usage
@app.route('/webhook', methods=['POST'])
def handle_webhook():
    payload = request.get_data(as_text=True)
    signature = request.headers.get('X-Webhook-Signature')
    
    if not verify_webhook_signature(payload, signature, WEBHOOK_SECRET):
        return 'Invalid signature', 401
    
    event = request.json
    # Process event
    print(f"Received event: {event['event']}")
    
    return 'OK', 200
```

### Testing Webhooks

Use the webhook testing tool:
1. Go to **Settings > Webhooks**
2. Click **"Test Webhook"**
3. Select event type
4. Send test payload

---

## Best Practices

### 1. Caching

Cache API responses to reduce requests:

```python
import time
from functools import lru_cache

@lru_cache(maxsize=128)
def get_project_cached(project_id, cache_time):
    """Cache project data for specified time"""
    # cache_time is used to bust cache periodically
    return client.get_project(project_id)

# Use with cache bust every 5 minutes
cache_key = int(time.time() // 300)
project = get_project_cached(1, cache_key)
```

### 2. Pagination

Always use pagination for large datasets:

```python
def get_all_projects(client, **filters):
    """Get all projects across all pages"""
    all_projects = []
    page = 1
    
    while True:
        response = client.get_projects(page=page, per_page=100, **filters)
        all_projects.extend(response['items'])
        
        if page >= response['total_pages']:
            break
        
        page += 1
    
    return all_projects
```

### 3. Error Handling

Implement retry logic with exponential backoff:

```python
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
):
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

# Usage
session = requests_retry_session()
response = session.get(
    'https://api.buildintel.com/api/v1/projects',
    headers=headers
)
```

### 4. Security

**Never expose credentials:**
- Use environment variables
- Don't commit tokens to git
- Rotate keys regularly
- Use HTTPS only

```python
import os
from dotenv import load_dotenv

load_dotenv()

client = BuildIntelAPI(
    email=os.getenv('BUILDINTEL_EMAIL'),
    password=os.getenv('BUILDINTEL_PASSWORD')
)
```

### 5. Monitoring

Track API usage and performance:

```python
import logging
import time

logger = logging.getLogger(__name__)

def monitored_api_call(func):
    """Decorator to monitor API calls"""
    def wrapper(*args, **kwargs):
        start = time.time()
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start
            logger.info(f"{func.__name__} completed in {duration:.2f}s")
            return result
        except Exception as e:
            duration = time.time() - start
            logger.error(f"{func.__name__} failed after {duration:.2f}s: {e}")
            raise
    return wrapper

@monitored_api_call
def get_projects(**filters):
    return client.get_projects(**filters)
```

---

## Support

### Developer Resources

**API Documentation**
- Interactive Docs: https://api.buildintel.com/api/docs
- ReDoc: https://api.buildintel.com/api/redoc
- Changelog: https://buildintel.com/changelog

**Code Examples**
- GitHub: https://github.com/buildintel/api-examples
- Postman Collection: Available in developer portal

**Community**
- Developer Forum: https://forum.buildintel.com
- Stack Overflow: Tag `buildintel`
- Discord: https://discord.gg/buildintel

### Getting Help

**Technical Support**
- Email: api-support@poorduceholdings.com
- Response Time:
  - Free Trial: 48 hours
  - Professional: 24 hours
  - Enterprise: 4 hours

**Bug Reports**
- Email: bugs@poorduceholdings.com
- Include:
  - API endpoint
  - Request/response
  - Error message
  - Timestamp

**Feature Requests**
- Email: features@poorduceholdings.com
- Community Forum: Vote on feature requests

**Emergency Support** (Enterprise)
- 24/7 Phone: 1-800-BUILD-INTEL
- Emergency Email: emergency@poorduceholdings.com

---

## Appendix

### Changelog

**v1.0.0** (January 2025)
- Initial API release
- Core endpoints for projects, analytics, intelligence
- JWT authentication
- Rate limiting
- Webhook support (Enterprise)

### Roadmap

**Q1 2025**
- GraphQL API
- Real-time subscriptions
- Batch operations
- Enhanced filtering

**Q2 2025**
- Machine learning predictions API
- Custom data exports
- Advanced analytics endpoints

### Terms of Service

By using the BuildIntel Pro API, you agree to our [Terms of Service](https://buildintel.com/terms) and [Privacy Policy](https://buildintel.com/privacy).

### API Limits

| Resource | Limit |
|----------|-------|
| Max request size | 10 MB |
| Max response size | 50 MB |
| Max items per page | 100 |
| Token expiration | 30 minutes |
| Webhook timeout | 30 seconds |

---

**Document Version**: 1.0.0  
**Last Updated**: January 2025  
**API Support**: api-support@poorduceholdings.com

---

*Happy Building with BuildIntel Pro API!*
