"""
API Documentation and Examples
"""

API_DESCRIPTION = """
# Kali OSINT Investigation Platform API

A comprehensive Open Source Intelligence (OSINT) investigation platform for professional security research and law enforcement.

## Features

- **Investigation Management**: Create, monitor, and manage OSINT investigations
- **Social Media Analysis**: Scrape and analyze social media profiles and posts
- **Domain Intelligence**: Comprehensive domain analysis and threat assessment
- **Network Analysis**: Generate relationship graphs and timeline analysis
- **Report Generation**: Export investigations in PDF, CSV, and JSON formats
- **Threat Assessment**: Advanced threat scoring and risk analysis

## Authentication

The API uses Bearer token authentication. Include your token in the Authorization header:

```
Authorization: Bearer your-token-here
```

## Rate Limiting

- **Investigation endpoints**: 10 requests per minute
- **Analysis endpoints**: 20 requests per minute
- **Export endpoints**: 5 requests per minute
- **Social media endpoints**: 30 requests per minute

## Error Handling

The API returns standard HTTP status codes:

- `200`: Success
- `400`: Bad Request
- `401`: Unauthorized
- `404`: Not Found
- `429`: Too Many Requests
- `500`: Internal Server Error

## Investigation Workflow

1. **Create Investigation**: POST `/api/v1/investigations/`
2. **Monitor Progress**: GET `/api/v1/investigations/{id}/status`
3. **View Findings**: GET `/api/v1/investigations/{id}/findings`
4. **Export Results**: POST `/api/v1/exports/investigation/{id}/pdf`

## Examples

### Create a GitHub Repository Investigation

```bash
curl -X POST "http://localhost:8000/api/v1/investigations/" \
  -H "Authorization: Bearer your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "target_type": "repository",
    "target_value": "https://github.com/username/repo",
    "analysis_depth": "comprehensive",
    "include_network_analysis": true,
    "include_timeline_analysis": true,
    "include_threat_assessment": true,
    "platforms": ["github"],
    "analysis_options": {
      "max_contributors": 100,
      "include_issues": true,
      "include_pull_requests": true
    }
  }'
```

### Analyze Social Media Profile

```bash
curl -X POST "http://localhost:8000/api/v1/social-media/scrape" \
  -H "Authorization: Bearer your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "twitter",
    "target": "username",
    "include_metadata": true,
    "include_media": false,
    "max_posts": 100
  }'
```

### Domain Analysis

```bash
curl -X POST "http://localhost:8000/api/v1/analysis/domain" \
  -H "Authorization: Bearer your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "domain": "example.com",
    "include_subdomains": true,
    "include_dns": true,
    "include_whois": true,
    "include_ssl": true
  }'
```

### Threat Assessment

```bash
curl -X POST "http://localhost:8000/api/v1/analysis/threat?target=suspicious-domain.com&analysis_type=comprehensive" \
  -H "Authorization: Bearer your-token"
```

## Data Models

### Investigation Request

```json
{
  "target_type": "domain|email|username|phone|ip_address|organization|person|repository",
  "target_value": "example.com",
  "analysis_depth": "basic|standard|deep|comprehensive",
  "platforms": ["github", "twitter", "instagram"],
  "include_network_analysis": true,
  "include_timeline_analysis": true,
  "include_threat_assessment": true,
  "analysis_options": {
    "max_depth": 3,
    "timeout": 300,
    "include_media": false
  }
}
```

### Investigation Response

```json
{
  "id": 1,
  "title": "Investigation: domain - example.com",
  "description": "OSINT investigation for domain: example.com",
  "target_type": "domain",
  "target_value": "example.com",
  "status": "running",
  "progress": 45,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:35:00Z"
}
```

### Threat Assessment

```json
{
  "target": "suspicious-domain.com",
  "threat_level": "high",
  "threat_score": 0.85,
  "indicators": [
    "Suspicious keyword detected: malware",
    "Recently registered domain"
  ],
  "risk_factors": [
    "Potential extremist content",
    "Suspicious data patterns"
  ],
  "recommendations": [
    "Enhanced monitoring recommended",
    "Review access controls",
    "Update security policies"
  ],
  "confidence": 0.8,
  "created_at": "2024-01-15T10:30:00Z"
}
```

## Endpoints Summary

### Investigations
- `POST /investigations/` - Create new investigation
- `GET /investigations/` - List investigations
- `GET /investigations/{id}` - Get investigation details
- `PUT /investigations/{id}` - Update investigation
- `DELETE /investigations/{id}` - Delete investigation
- `GET /investigations/{id}/status` - Get investigation status
- `GET /investigations/{id}/findings` - Get investigation findings
- `GET /investigations/statistics` - Get investigation statistics

### Social Media
- `POST /social-media/scrape` - Scrape social media data
- `GET /social-media/profiles` - List social media profiles
- `GET /social-media/profiles/{id}` - Get profile details
- `GET /social-media/profiles/{id}/posts` - Get profile posts
- `GET /social-media/high-threat` - Get high threat profiles
- `GET /social-media/verified` - Get verified profiles
- `GET /social-media/posts/recent` - Get recent posts
- `GET /social-media/posts/high-engagement` - Get high engagement posts
- `GET /social-media/statistics` - Get social media statistics

### Analysis
- `POST /analysis/threat` - Analyze threat level
- `GET /analysis/network/{entity_id}` - Get network graph
- `GET /analysis/timeline/{entity_id}` - Get timeline data
- `POST /analysis/domain` - Analyze domain
- `GET /analysis/domains` - List domain analyses
- `GET /analysis/domains/{id}` - Get domain analysis
- `GET /analysis/domains/high-threat` - Get high threat domains
- `GET /analysis/statistics` - Get analysis statistics

### Exports
- `POST /exports/investigation/{id}/pdf` - Export as PDF
- `POST /exports/investigation/{id}/csv` - Export as CSV
- `POST /exports/investigation/{id}/json` - Export as JSON
- `GET /exports/reports` - List reports
- `GET /exports/reports/{id}` - Get report details
- `GET /exports/reports/{id}/download` - Download report

## Security Considerations

- All API endpoints require authentication
- Rate limiting is enforced to prevent abuse
- Sensitive data is encrypted at rest
- Audit logging is enabled for all operations
- Input validation is performed on all requests
- CORS is configured for web client access

## Legal Compliance

- Respects platform terms of service
- Implements responsible scraping practices
- Only collects publicly available information
- Provides data retention controls
- Supports data deletion requests
- Complies with relevant privacy regulations

## Support

For API support and questions:
- Documentation: `/docs` (Swagger UI)
- Alternative docs: `/redoc` (ReDoc)
- Health check: `/health`
- API version: `/api/v1/`
""" 