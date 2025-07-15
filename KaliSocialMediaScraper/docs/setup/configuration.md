# Configuration Guide

This document covers all configuration options for the Kali OSINT Investigation Platform.

## Configuration Files

- `config/.env` - Environment variables and secrets
- `config/.env.example` - Example environment file template
- `config/alembic.ini` - Database migration configuration
- `config/proxy_config.json` - Proxy server configuration

## Environment Variables (.env)

### Database Configuration
```bash
# Database connection
DATABASE_URL=postgresql://user:password@localhost/kali_scraper
# Alternative: SQLite for development
DATABASE_URL=sqlite:///./kali_osint.db

# Redis for Celery
REDIS_URL=redis://localhost:6379
```

### Security Settings
```bash
# Application security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API settings
API_V1_STR=/api/v1
PROJECT_NAME=Kali Social Media Scraper
BACKEND_CORS_ORIGINS=["http://localhost:5173"]
```

### Scraping Configuration
```bash
# Rate limiting and delays
SCRAPING_DELAY=1.0
MAX_CONCURRENT_REQUESTS=5
PROXY_ROTATION=true

# Timeouts
REQUEST_TIMEOUT=30
BROWSER_TIMEOUT=60
```

### Open Source Tools Configuration
```bash
# Note: All tools work without API keys using public data sources
GITHUB_API_URL=https://api.github.com

# Social Media Scrapers
TWITTER_SCRAPER_ENABLED=true
INSTAGRAM_SCRAPER_ENABLED=true
FACEBOOK_SCRAPER_ENABLED=true
YOUTUBE_SCRAPER_ENABLED=true
REDDIT_SCRAPER_ENABLED=true
TELEGRAM_SCRAPER_ENABLED=true
DISCORD_SCRAPER_ENABLED=true

# Domain Analysis
WHOIS_SERVER=whois.iana.org
DNS_SERVERS=8.8.8.8,1.1.1.1
SSL_VERIFY=true
SUBDOMAIN_ENUMERATION_ENABLED=true
DNS_BRUTE_FORCE_ENABLED=true

# Threat Intelligence
THREAT_INTELLIGENCE_ENABLED=true
THREAT_SCORE_THRESHOLD=0.7
ANOMALY_DETECTION_ENABLED=true
DNSBL_CHECK_ENABLED=true
REPUTATION_CHECK_ENABLED=true
```

### Logging Configuration
```bash
# Logging levels
LOG_LEVEL=INFO
LOG_FORMAT=json
LOG_FILE=logs/app.log

# Debug settings
DEBUG=false
ENVIRONMENT=production
```

## Setup Instructions

### 1. Environment File Setup
```bash
# Copy example environment file
cp config/.env.example config/.env

# Edit with your configuration
nano config/.env
```

### 2. Database Configuration
```bash
# PostgreSQL setup
createdb kali_scraper
psql kali_scraper -c "CREATE USER kali_user WITH PASSWORD 'your_password';"
psql kali_scraper -c "GRANT ALL PRIVILEGES ON DATABASE kali_scraper TO kali_user;"

# Update DATABASE_URL in .env
DATABASE_URL=postgresql://kali_user:your_password@localhost/kali_scraper
```

### 3. Redis Configuration
```bash
# Start Redis service
brew services start redis  # macOS
sudo systemctl start redis  # Linux

# Test connection
redis-cli ping
```

### 4. Proxy Configuration
```bash
# Edit proxy configuration
nano config/proxy_config.json

# Example proxy configuration
{
  "proxies": [
    {
      "host": "proxy1.example.com",
      "port": 8080,
      "username": "user",
      "password": "pass"
    }
  ],
  "rotation": true,
  "timeout": 30
}
```

## Security Best Practices

### Environment Variables
- Never commit `.env` files to version control
- Use strong, unique secrets in production
- Rotate secrets regularly
- Use environment-specific configurations

### Database Security
- Use strong passwords for database users
- Limit database access to application servers only
- Enable SSL for database connections in production
- Regular backups with encryption

### API Security
- Implement rate limiting
- Use HTTPS in production
- Validate all input data
- Monitor for suspicious activity

### Proxy Security
- Use trusted proxy providers
- Rotate proxy credentials regularly
- Monitor proxy performance and reliability
- Implement fallback mechanisms

## Production Configuration

### Environment Variables for Production
```bash
# Production settings
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=WARNING

# Security
SECRET_KEY=your-very-long-random-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15

# Database
DATABASE_URL=postgresql://user:password@prod-db.example.com/kali_scraper
REDIS_URL=redis://prod-redis.example.com:6379

# CORS
BACKEND_CORS_ORIGINS=["https://yourdomain.com"]
```

### Docker Configuration
```bash
# Use environment variables in docker-compose.yml
environment:
  - DATABASE_URL=${DATABASE_URL}
  - REDIS_URL=${REDIS_URL}
  - SECRET_KEY=${SECRET_KEY}
```

## Troubleshooting

### Common Configuration Issues

1. **Database Connection Errors**
   ```bash
   # Check database status
   pg_isready -h localhost -p 5432
   
   # Test connection
   psql $DATABASE_URL -c "SELECT 1;"
   ```

2. **Redis Connection Issues**
   ```bash
   # Check Redis status
   redis-cli ping
   
   # Check Redis configuration
   redis-cli config get bind
   ```

3. **CORS Issues**
   ```bash
   # Ensure CORS origins are correctly formatted
   BACKEND_CORS_ORIGINS=["http://localhost:5173","https://yourdomain.com"]
   ```

4. **Proxy Configuration**
   ```bash
   # Test proxy connection
   curl --proxy proxy.example.com:8080 http://httpbin.org/ip
   ```

### Configuration Validation
```bash
# Validate environment configuration
python -c "from app.core.config import settings; print('Configuration loaded successfully')"

# Check database migrations
alembic current
alembic history
``` 